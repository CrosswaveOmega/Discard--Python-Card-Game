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

class Piece:
    """Base Class for Creature and Leader pieces
    # NOTE: Creatures and Leaders will be Classes decended from this.
    """

    def __init__(self, player, name, hp, speed, move_style, position, img=None):
        #Img should be a PIL image object
        self.player=player #the player object this piece belongs to.
        self.name=name
        self.max_hp=hp
        self.damage=0
        #Current HP= max_hp - damage.
        self.speed=speed
        self.move_style=move_style #The multilined text
        self.move_limit=1
        #Speed is 1-100.
        self.position=Position(notation=position)
        self.display_image=img
        current_options={}
    def generate_options(self):
        #creates a new dictionary of all options.
        #Universal opitons are: MOVE, ... END.
        actions={}
        actions["MOVE"]=self.move_limit
        actions["END"]=1
        return actions

    async def do_move(self, game_ref):
        move_options=self.get_move_options(game_ref.get_grid())

        img=await game_ref.make_move_preview(move_options)
        sent_mess = await self.player.get_dpios().send_pil_image(img)
        option=await self.player.select_option(move_options)
        await sent_mess.delete()
        if(option!="back" and option!="timeout"):
            print(option)
            self.change_position(option)
            game_ref.set_update()
            await game_ref.send_user_updates()
            return True
        return False

    async def get_action(self, game_ref):#Add other args accordingly.
        self.player.gain_summon_points()
        options=self.generate_options()
        my_turn=True
        while my_turn:
            choices=[]
            for key, item in options.items():
                if item >0:
                    choices.append(key)
            await self.player.send_embed_to_user()
            action= await self.player.select_command(choices)
            my_turn, completed=await self.process_option(game_ref, action)
            if(completed):
                if action in options:
                    options[action]=options[action]-1



        await asyncio.sleep(0.4)
        print(self.name)
        return None
        #universal options.
    async def process_option(self, game_ref, action):
        my_turn=True
        print(action)
        completed=False
        if (action=="MOVE"):
            completed= await self.do_move(game_ref)
        elif (action=="END"):
            my_turn=False
        elif (action == "timeout"):
            print("Timeout")
            my_turn == False
        return my_turn, completed

    def get_move_options(self, grid): #Wip function.
        """supposed to split move style into list line by line."""
        lines=self.move_style.splitlines()
        move_options=[]
        for line in lines:
            move_options.extend(grid.get_all_movements_in_range(self.position, line))
        return move_options

    def get_hp(self):
        hp = self.max_hp - self.damage
        return hp
    def get_speed(self):
        return self.speed
    def set_image_by_url(self, url):
        self.image=url_to_PIL_image(url)

    def add_damage(self, damage_add=0):
        self.damage=self.damage+ damage_add
        print("Add Damage is incomplete.")
    def change_position(self, new_position_notation):
        self.position=Position(notation=new_position_notation)
    def get_image(self):
        return self.image
    def string_status(self):
        result="{},{}/{}".format(self.name, self.get_hp(), self.max_hp)
        return result

    #To Do- String Rep.  Rep will be Icon, Name, and Position


class Creature(Piece):
    """Creature class.  This is what all creatures will be summoned into."""

    def __init__(self, creature_card, player, position):
        # Gets the attributes from a passed in creature card
        self.name = creature_card.get_name()
        self.skill_1 = creature_card.get_skill_1()
        self.skill_2 = creature_card.get_skill_2()
        self.skill_3 = creature_card.get_skill_3()
        self.image = creature_card.get_Image()
        self.icon = creature_card.get_icon()
        self.summoncost_r = creature_card.get_summoncost_r()
        self.summoncost_b = creature_card.get_summoncost_b()
        self.summoncost_g = creature_card.get_summoncost_g()
        self.speed = creature_card.get_speed()
        self.move_style = creature_card.get_move_style()
        self.move_limit = creature_card.get_move_limit()
        self.max_hp = creature_card.get_hp()
        self.ID = creature_card.get_ID()
        self.type = creature_card.get_type()

        # Player and Position come from Piece class
        super().__init__(player, position)


class Leader(Piece):
    """Leader class.  This is the avatar of the players."""
    """Through the leader, the players will do most actions."""
    def __init__(self, player, name, position_notation):
        self.player=player #the player object this piece belongs to.
        self.name=name
        #Current HP= max_hp - damage.
        speed=50
        move_style="STEP 1" #The multilined text
        move_limit=1
        #Speed is 1-100.
        position=position_notation
        #Image is url
        super().__init__(player=player, name=name, hp=20, speed=speed, move_style=move_style, position=position_notation)

    def set_image(self):
        if self.player.get_PlayerType() == "Discord":
            url=self.player.get_avatar_url()
            self.image=url_to_PIL_image(url)

    def generate_options(self):
        #creates a new dictionary of all options.
        #Universal opitons are: MOVE, ... END.
        actions={}
        actions["MOVE"]=self.move_limit
        actions["DRAW"]=1
        actions["END"]=1
        return actions
    async def process_option(self, game_ref, action):
        my_turn=True
        print(action)
        completed=False
        if (action=="MOVE"):
            completed= await self.do_move(game_ref)
        elif (action=="DRAW"):
            self.player.draw_card()
            completed=True
            #Draw one card.  Add it to the hand.
        elif (action=="END"):
            my_turn=False

        elif (action == "timeout"):
            print("Timeout")
            my_turn == False
        return my_turn, completed

#Driver Code.
#if __name__ == "__main__":
#    print("MAIN.")
    #testPiece=Piece("LO", "MY_NAME", 5,5, "STEP 1", "B3")
    #print(testPiece.position.x_y())
