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

        self.current_actions = {}

        self.effects = {}
    def toggle_active(self):
        self.active=not self.active

    def add_effect(self, effect_name, time, context, function, arg, disable, disable_arg, level=0, description=""):
        print("added_effect")
        self.add_effect_direct(effect_name, Effect(time, context, function, arg, disable, disable_arg, level, description))

    def add_effect_direct(self, effect_name, effect):
        self.effects[effect_name]=effect

    async def check_effects(self, time, context, dictionary, game_ref):
        dicton=dictionary
        to_disable=[]
        for effect_name, effect in self.effects.items():
            if effect.check_trigger(time, context):
                dictionary=await effect.execute(dictionary, game_ref)
            if (time == 'after' and context=='turn'):
                effect.add_turn()
            if effect.disable_check():
                to_disable.append(effect_name)
                await game_ref.send_announcement("{} wore off.".format(effect_name))
            #print("Ok")
        #print("ok")
        for effect_name in to_disable:
            self.effects.pop(effect_name)
        return dictionary


    def get_effect_names(self):
        effectlist=""
        if(len(self.effects)<=0):
            return "Normal"
        for effect_name, effect in self.effects.items():
            effectlist=effectlist+effect_name+"\n"
        return effectlist

    def set_game_id(self, new_id):
        self.game_id = new_id
    def get_game_id(self):
        return self.game_id

    def get_name(self):
        return self.name

    def generate_commands(self, actions={}):
        # creates a new dictionary of all action options.
        # Universal opitons are: MOVE, ... END.
        actions["MOVE"] = self.move_limit
        actions["END"] = 1

        #check effects
        return actions


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
            await game_ref.send_announcement("Moved {} to {}".format(self.get_name(), option))
            return True
        return False

    async def do_auto_skills(self):
        pass

    async def get_action(self, game_ref):  # Add other args accordingly.
        """this does a piece's turn."""
        if(self.type=="Leader"):
            self.player.gain_summon_points()

        if(self.type=="Creature"):
            await self.do_auto_skills(game_ref)
        self.player.gain_fp()
        self.current_actions = self.generate_commands()
        #self.current_actions=await self.check_effects('before', 'command_setting', self.current_actions, None) #Check effects on self.
        my_turn = True
        await game_ref.send_announcement("{}'s turn".format(self.get_name()))
        await self.check_effects('before', 'turn', {'this_piece':self}, game_ref)
        while my_turn:
            choices = []
            for key, item in self.current_actions.items():
                if item > 0:
                    choices.append(key)
            await self.player.send_embed_to_user()
            await game_ref.update_all()
            action = await self.player.select_command(choices)
            my_turn, completed = await self.process_option(game_ref, action)
            if (completed):
                if action in self.current_actions:
                    self.current_actions[action] = self.current_actions[action] - 1
            await game_ref.update_all()

        #await asyncio.sleep(0.1)
        await game_ref.send_announcement("Turn end.")
        await self.check_effects('after', 'turn', {'this_piece':self}, game_ref)
        print("End OF TURN.")
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
            #await self.player.send_announcement("Ending Turn.")
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
        url_new=url
        if url_new=='':
            url_new="""https://media.discordapp.net/attachments/780514923075469313/783759517070131200/default.png"""
        self.image = url_to_PIL_image(url_new)

    def add_damage(self, damage_add=0):
        self.damage = self.damage + damage_add
        if self.damage > self.max_hp:
            self.damage = self.max_hp
        print("Damage added.")

    def heal_damage(self, damage_add=0):
        self.damage = self.damage - damage_add
        if (self.damage < 0):
            self.damage = 0
        print("Healed damage.")

    def change_position(self, new_position_notation):
        self.position = Position(notation=new_position_notation)

    def get_grid_card_icon(self):
        # Will need to optimize later.
        orig_img = self.get_image()
        return make_card_grid_icon(orig_img, self.player.team, self.hp_fraction(), self.active)

    def get_image(self):
        return self.image

    def compute_distance_to(self, other_pos, dist_type="Rectilinear"):
        thisposition=self.get_position()
        if(dist_type=="Rectilinear"):
            return thisposition.get_rectilinear_distance(other_pos)
        return 0

    def get_team(self):
        return self.player.get_team()

    def string_status(self):
        team=self.get_team()
        icons=['🟥', '🟦']
        icon=icons[team-1]
        result = "[{}|{}|HP:{}|SPD:{}]".format(icon,self.name, self.hp_fraction(), self.get_speed())
        return result

    def get_position(self):
        return self.position

    def get_embed(self):
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

    def generate_commands(self, actions={}):
        # creates a new dictionary of all options.
        # Universal opitons are: MOVE, ... END.
        actions["SKILL"] = 1
        actions = super().generate_commands(actions)
        return actions
    async def do_auto_skills(self, game_ref):
        #This command is for auto skills if available
        #Also fires the decr_cooldown method of each skill
        skill_list = []
        if (self.skill_1 != None):
            self.skill_1.decrement_cooldown()
            if (self.skill_1.trigger == "auto"):
                skill_list.append(self.skill_1)
        if (self.skill_2 != None):
            self.skill_2.decrement_cooldown()
            if (self.skill_2.trigger == "auto"):
                skill_list.append(self.skill_2)
        if (self.skill_3 != None):
            self.skill_3.decrement_cooldown()
            if (self.skill_3.trigger == "auto"):
                skill_list.append(self.skill_3)
        for skill in skill_list:
            target_list, amount, grouped = match_with_target_data(skill.get_target_data(), self, game_ref)
            print("ADD LATER.")
            selected_targets = []
            get_targets=True
            if (len(target_list) <= amount):
                #set selected_targets to the target_list if the amount
                #of targets is less than the amount.
                selected_targets= target_list
                get_targets=False
            if(get_targets):
                for i in range(0, amount):
                    target = await self.player.select_piece(target_list, "Select a target for {}.".format(skill.get_name()))
                    if (target == "back" or target == "timeout" or option=="invalidmessage"):
                        break
                    selected_targets.append(target)
            await skill.doSkill(self, selected_targets, game_ref)
            print("End of Skill")
            game_ref.set_update()
            await game_ref.send_user_updates()

    async def skill_option(self, game_ref):
        """Processing of skill."""

        skill_list = []
        fp=self.player.get_fp()
        if (self.skill_1 != None):
            if (self.skill_1.trigger == "command" and self.skill_1.can_use(fp) ):
                skill_list.append(self.skill_1.get_name())
        if (self.skill_2 != None):
            if (self.skill_2.trigger == "command" and self.skill_2.can_use(fp) ):
                skill_list.append(self.skill_2.get_name())
        if (self.skill_3 != None):
            if (self.skill_3.trigger == "command" and self.skill_3.can_use(fp) ):
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

        matched_list, amount, grouped = match_with_target_data(skill.get_target_data(), self, game_ref)
        target_list=matched_list
        if grouped:
            print("have player select group.")
            #Select group.

        selected_targets = []
        get_targets=True
        if (len(target_list) <= amount):
            #set selected_targets to the target_list if the amount
            #of targets is less than the amount.
            selected_targets= target_list
            get_targets=False

        if(get_targets):
            for i in range(0, amount):
                target = await self.player.select_piece(target_list, "Select a target.")
                if (target == "back" or target == "timeout" or option=="invalidmessage"):
                    return False
                selected_targets.append(target)
        await skill.doSkill(self, selected_targets, game_ref)
        self.player.sub_fp(skill.get_FP_cost())
        skill.limit_act()
        print("End of Skill")
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
        statuses=self.get_effect_names()
        embed.add_field(name="Statuses",
                        value=statuses, inline=True)
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

    def __init__(self, player, name, position_notation, speed=50):
        self.player = player  # the player object this piece belongs to.
        self.name = name
        # Current HP= max_hp - damage.
        #speed = 50
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
        elif self.player.get_PlayerType() == "Test":
            url = "https://media.discordapp.net/attachments/780514923075469313/783769376000049182/unknown.png"
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

    def generate_commands(self, actions={}):
        # creates a new dictionary of all options.
        # Universal opitons are: MOVE, ... END.

        #actions["MOVE"] = self.move_limit
        actions["DRAW"] = 1
        actions["SUMMON"] = 1
        actions["FOCUS"] = 1
        #actions["END"] = 1
        actions = super().generate_commands(actions)
        return actions

    async def process_option(self, game_ref, action):
        my_turn = True
        print(action)
        completed = False
        if (action == "DRAW"):
            feedbackstr=self.player.draw_card()
            await self.player.send_announcement(feedbackstr)
            completed = True
        elif (action == "FOCUS"):
            completed=await self.player.get_focus_action(game_ref)
        elif (action == "SUMMON"):
            completed = await self.player.get_summon_action(game_ref, self.get_summon_spaces(game_ref.get_grid()))
            if completed:
                my_turn = False
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

        spstr=self.player.get_summon_point_string()
        embed.set_footer(text=spstr)
        statuses=self.get_effect_names()
        embed.add_field(name="Status",
                        value=statuses, inline=True)


        return embed

# Driver Code.
# if __name__ == "__main__":
#    print("MAIN.")
# testPiece=Piece("LO", "MY_NAME", 5,5, "STEP 1", "B3")
# print(testPiece.position.x_y())
