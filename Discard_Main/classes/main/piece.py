import discord
import operator
import io
import json
import aiohttp
import asyncio
import csv
import datetime
import queue
from PIL import Image, ImageTk, ImageGrab, ImageDraw, ImageFont

from discord.ext import commands, tasks
from discord.utils import find
from discord import Webhook, AsyncWebhookAdapter

from .generic.position import Position
from ..Cards.card import CreatureCard
from ..imagemakingfunctions.imaging import *
from .target_matching import match_with_target_data

from .effect import Effect

class Piece:
    """Base Class for Creature and Leader pieces
    # NOTE: Creatures and Leaders will be Classes decended from this.
    """

    def __init__(self, player, name="", hp=1, speed=1, move_style="", position="", img=None):
        # Img should be a PIL image object
        self.player = player  # the player object this piece belongs to.
        self.name = name
        self.type="Default"
        self.game_id = 0

        self.active=False

        self.max_hp = hp
        self.damage = 0
        # Current HP= max_hp - damage.
        self.speed = speed
        self.move_style = move_style  # The multilined text
        self.move_limit = 1
        # Speed is 1-100.
        self.position = Position(notation=position)
        self.display_image = img
        self.image = None

        self.current_options = {}

        self.effects = {}
    def toggle_active(self):
        self.active=not self.active
    def add_effect(self, effect_name, time, context, function, arg, disable, disable_arg, level=0):
        print("added_effect")
        self.effects[effect_name]=Effect(time, context, function, arg, disable, disable_arg, level)

    async def check_effects(self, time, context, dictionary, game_ref):
        dicton=dictionary
        to_disable=[]
        for effect_name, effect in self.effects.items():
            if effect.check_trigger(time, context):
                dictionary=await effect.execute(dictionary, game_ref)
            if effect.disable_check():
                to_disable.append(effect_name)
                await game_ref.send_announcement("{} wore off.".format(effect_name))
            print("Ok")
        print("ok")
        for effect_name in to_disable:
            self.effects.pop(effect_name)
        return dictionary

    def set_game_id(self, new_id):
        self.game_id = new_id

    def generate_options(self):
        # creates a new dictionary of all options.
        # Universal opitons are: MOVE, ... END.
        actions = {}
        actions["MOVE"] = self.move_limit
        actions["END"] = 1
        return actions

    def get_name(self):
        return self.name

    async def do_move(self, game_ref):
        move_options = self.get_move_options(game_ref.get_grid())

        buffer = self.player.has_something_in_buffer()
        sent_mess = None
        if(not buffer):
            img = await game_ref.make_move_preview(move_options)
            if(self.player.PlayerType=="Discord"):
                sent_mess = await self.player.get_dpios().send_pil_image(img)

        option = await self.player.select_option(move_options)

        if(sent_mess != None):
            await sent_mess.delete()

        if (option != "back" and option != "timeout" and option!="invalidmessage"):
            print(option)
            self.change_position(option)
            game_ref.set_update()
            await game_ref.send_user_updates()
            await self.player.send_announcement("Moved {} to {}".format(self.get_name(), option))
            return True
        return False

    async def get_action(self, game_ref):  # Add other args accordingly.
        self.player.gain_summon_points()
        options = self.generate_options()
        my_turn = True
        await game_ref.send_announcement("{}'s turn".format(self.get_name()))
        while my_turn:
            choices = []
            for key, item in options.items():
                if item > 0:
                    choices.append(key)
            await self.player.send_embed_to_user()
            action = await self.player.select_command(choices)
            my_turn, completed = await self.process_option(game_ref, action)
            if (completed):
                if action in options:
                    options[action] = options[action] - 1

        await asyncio.sleep(0.1)
        await game_ref.send_announcement("Turn end.")
        return None
        # universal options.

    async def process_option(self, game_ref, action):
        #Universal actions
        my_turn = True
        print(action)
        completed = False
        if (action == "MOVE"):
            completed = await self.do_move(game_ref)
        elif (action == "END"):
            await self.player.send_announcement("Ending Turn.")
            my_turn = False
        elif (action=="invalidmessage"):
            await self.player.send_announcement("unrecognized input.  Try again.")
        elif (action == "timeout"):
            await self.player.send_announcement("Timeout.  Advancing turn.")
            my_turn = False
        else:
            my_turn, completed=await self.player.local_commands(action, game_ref)
        return my_turn, completed

    def get_move_options(self, grid):  # Wip function.
        """supposed to split move style into list line by line."""
        lines = self.move_style.splitlines()
        move_options = []
        for line in lines:
            move_options.extend(
                grid.get_all_movements_in_range(self.position, line))
        return move_options

    def get_hp(self):
        hp = self.max_hp - self.damage
        return hp

    def hp_fraction(self):
        # Returns current hp divided by max_hp
        return "{}/{}".format(self.get_hp(), self.max_hp)

    def get_speed(self):
        return self.speed

    def set_image_by_url(self, url):
        self.image = url_to_PIL_image(url)

    def add_damage(self, damage_add=0):
        self.damage = self.damage + damage_add
        print("Add Damage is incomplete.")

    def heal_damage(self, damage_add=0):
        self.damage = self.damage - damage_add
        if (self.damage < 0):
            self.damage = 0
        print("Add Damage is incomplete.")

    def change_position(self, new_position_notation):
        self.position = Position(notation=new_position_notation)

    def get_grid_card_icon(self):
        # Will need to optimize later.
        orig_img = self.get_image()
        return make_card_grid_icon(orig_img, self.player.team, self.hp_fraction(), self.active)

    def get_image(self):
        return self.image

    def get_team(self):
        return self.player.get_team()

    def string_status(self):
        result = "{},{}/{}".format(self.name, self.get_hp(), self.get_hp())
        return result

    def get_position(self):
        return self.position

    def get_embed():
        pass

    # To Do- String Rep.  Rep will be Icon, Name, and Position


class Creature(Piece):
    """Creature class.  This is what all creatures will be summoned into."""

    def __init__(self, creature_card, player, position):
        # Gets the attributes from a passed in creature card
        # Player and Position come from Piece class
        super().__init__(player=player, position=position, img=creature_card.get_image())
        self.name = creature_card.get_name()
        self.skill_1 = creature_card.get_skill_1()
        self.skill_2 = creature_card.get_skill_2()
        self.skill_3 = creature_card.get_skill_3()
        self.display_image = creature_card.get_image()
        self.icon = creature_card.get_icon()
        self.summoncost_r = creature_card.get_summoncost_r()
        self.summoncost_b = creature_card.get_summoncost_b()
        self.summoncost_g = creature_card.get_summoncost_g()
        self.speed = creature_card.get_speed()
        self.move_style = creature_card.get_move_style()
        self.move_limit = creature_card.get_move_limit()
        self.max_hp = creature_card.get_hp()
        self.ID = creature_card.get_ID()
        self.type = "Creature"

        self.card = creature_card
        print(self.display_image)
        self.set_image_by_url(self.display_image)

    def get_card(self):
        return self.card

    def generate_options(self):
        # creates a new dictionary of all options.
        # Universal opitons are: MOVE, ... END.
        actions = {}
        actions["MOVE"] = self.move_limit
        actions["SKILL"] = 1
        actions["END"] = 1
        return actions

    async def skill_option(self, game_ref):
        """Processing of skill."""

        skill_list = []
        if (self.skill_1 != None):
            if (self.skill_1.trigger == "command"):
                skill_list.append(self.skill_1.get_name())
        if (self.skill_2 != None):
            if (self.skill_2.trigger == "command"):
                skill_list.append(self.skill_2.get_name())
        if (self.skill_3 != None):
            if (self.skill_3.trigger == "command"):
                skill_list.append(self.skill_3.get_name())

        option = await self.player.select_option(skill_list, "Select a skill")
        if (option == "back" or option == "timeout" or option=="invalidmessage"):
            return False
        skill = None
        if(self.skill_1!=None):
            if (option == self.skill_1.get_name()):
                skill = self.skill_1
        if(self.skill_2!=None):
            if (option == self.skill_2.get_name()):
                skill = self.skill_2
        if(self.skill_3!=None):
            if (option == self.skill_3.get_name()):
                skill = self.skill_3

        target_list, amount = match_with_target_data(skill.get_target_data(), self, game_ref)
        if (len(target_list) <= amount):
            await skill.doSkill(self, target_list, game_ref)
            return True

        selected_targets = []
        for i in range(0, amount):
            target = await self.player.select_piece(target_list, "Select a target.")
            if (target == "back" or target == "timeout" or option=="invalidmessage"):
                return False
            selected_targets.append(target)
        await skill.doSkill(self, selected_targets, game_ref)
        game_ref.set_update()
        await game_ref.send_user_updates()
        return True

    async def process_option(self, game_ref, action):
        my_turn = True
        print(action)
        completed = False

        if (action == "SKILL"):
            completed = await self.skill_option(game_ref)
        else:
            my_turn, completed=await super().process_option(game_ref, action)

        return my_turn, completed

    def get_embed(self):
        embed = self.card.to_DiscordEmbed(use_image=False)
        HP="HP:{}".format(self.hp_fraction())
        Speed="Speed:{}".format(self.get_speed())
        pos="Position:{}".format(self.get_position().get_notation())
        desc="{}\n{}\n{}".format(HP, Speed, pos)
        embed.description = desc
        color=discord.Colour(0x7289da)
        if(self.get_team()==1):
            color=discord.Colour(0xff2e47)
        if(self.get_team()==2):
            color=discord.Colour(0x2305c2)
        embed.colour=color
        return embed


class Leader(Piece):
    """Leader class.  This is the avatar of the players."""
    """Through the leader, the players will do most actions."""

    def __init__(self, player, name, position_notation):
        self.player = player  # the player object this piece belongs to.
        self.name = name
        # Current HP= max_hp - damage.
        speed = 50
        move_style = "STEP 1"  # The multilined text
        move_limit = 1
        # Speed is 1-100.
        position = position_notation
        # Image is url
        super().__init__(player=player, name=name, hp=20, speed=speed, move_style=move_style,
                         position=position_notation)
        self.type="Leader"

    def set_image(self):
        if self.player.get_PlayerType() == "Discord":
            url = self.player.get_avatar_url()
            self.image = url_to_PIL_image(url)

    def get_summon_spaces(self, grid):  # Wip function.
        """uses a modified version of the move style to get summon spaces."""
        summonSpace = """
STEP 1
HOP X -1 Y -1
HOP X 1 Y -1
HOP X -1 Y 1
HOP X 1 Y 1"""
        lines = summonSpace.splitlines()
        summon_options = []
        for line in lines:
            summon_options.extend(
                grid.get_all_movements_in_range(self.position, line))
        return summon_options

    def generate_options(self):
        # creates a new dictionary of all options.
        # Universal opitons are: MOVE, ... END.
        actions = {}
        actions["MOVE"] = self.move_limit
        actions["DRAW"] = 1
        actions["SUMMON"] = 1
        actions["END"] = 1
        return actions

    async def process_option(self, game_ref, action):
        my_turn = True
        print(action)
        completed = False
        if (action == "DRAW"):
            feedbackstr=self.player.draw_card()
            await self.player.send_announcement(feedbackstr)
            completed = True
            # Draw one card.  Add it to the hand.
        elif (action == "SUMMON"):
            completed = await self.player.get_summon_action(game_ref, self.get_summon_spaces(game_ref.get_grid()))
            #summon a creature
        else:
            my_turn, completed=await super().process_option(game_ref, action)
        return my_turn, completed

    def get_embed(self):
        HP="HP:{}".format(self.hp_fraction())
        Speed="Speed:{}".format(self.get_speed())
        pos="Position:{}".format(self.get_position().get_notation())
        desc="{}\n{}\n{}".format(HP, Speed, pos)
        embed = discord.Embed(title="{}".format(self.get_name()), colour=discord.Colour(0x7289da),
                              description=desc)
        color=discord.Colour(0x7289da)
        if(self.get_team()==1):
            color=discord.Colour(0xff2e47)
        if(self.get_team()==2):
            color=discord.Colour(0x2305c2)
        embed.colour=color
        embed.set_thumbnail(url=self.player.get_avatar_url())

        return embed

# Driver Code.
# if __name__ == "__main__":
#    print("MAIN.")
# testPiece=Piece("LO", "MY_NAME", 5,5, "STEP 1", "B3")
# print(testPiece.position.x_y())
