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


from .classes.imagemakingfunctions.imaging import *
from .classes.main.piece import *
from .classes.main.player import *
from .classes.main.GridClass import Grid
#from classes.main import *
#The main game.



from configparser import ConfigParser


configur=ConfigParser()
configur.read('config.ini')


class Card_Duel():
    """Where the game will be played."""
    def __init__(self, bot):
        dicti=vars(Grid())
        print(json.dumps(dicti))
        self.game_id=0
        self.val=0
        self.players=[]
        self.entity_list=[]
        self.bot = bot

        self.grid_message=None
        self.gridchange=True

        self.mode="Test" #the "mode" of the game.  a simplified setting.
        self.settings=None #Settings of the game.
        self.duel_helper=Card_Duel_Helper(self)
        self.grid = Grid(5,5,self.duel_helper)


        self.round=0
        self.log=[] #Log of everything that happened.
        self.game_is_active=False

    def apply_settings(self, settings=None):
        if settings!=None:
            self.settings=settings
    def addPlayer(self, player=None):
        if(player!=None):
            self.players.append(player)
    async def move_preview(self, spaces=[]):
        pilgrid=self.grid.grid_to_PIL_array(spaces)
        img=make_image_from_grid(pilgrid, self.grid.columns, self.grid.rows)
        return img
    def grid_updated(self):
        self.gridchange=True

    async def send_grid(self): #A WIP function.  it sends a grid to all players.
        pilgrid=self.grid.grid_to_PIL_array()
        img=make_image_from_grid(pilgrid, self.grid.columns, self.grid.rows)
        for player in self.players:
            if(player.get_PlayerType()=="Discord"):
                await player.get_dpios().send_pil_image(img)

    async def send_update(self, url): #A WIP function.  it sends a grid to all players.
        """UPDATE ALL DPIOS OF PLAYERS."""
        print(self.round)
        for player in self.players:
            if(player.get_PlayerType()=="Discord"):
                await player.get_dpios().update_grid_message(url, self.round)
    def add_piece(self, piece):
        self.entity_list.append(piece)
    def move_piece(self, piece):
        piece.get_move_options(self.grid)

    async def update_grid_image(self):
        #Refresh the grid image.
        checkGuild= self.bot.get_guild(int(configur.get("Default",'bts_server'))) #Behind The Scenes server
        image_channel= checkGuild.get_channel(int(configur.get("Default",'bts_game_images'))) #Customs Channel.
        if(self.gridchange):
            pilgrid=self.grid.grid_to_PIL_array()
            img=make_image_from_grid(pilgrid, self.grid.columns, self.grid.rows)
            with io.BytesIO() as image_binary:
                img.save(image_binary, 'PNG') #Returns pil object.
                image_binary.seek(0)
                image_msg=await image_channel.send(file=discord.File(fp=image_binary, filename='image.png'))
                self.grid_message=image_msg
            self.gridchange=False
        url="p"
        for attach in self.grid_message.attachments:
            url=attach.url
            print("url")
            await self.send_update(url)




    def turn_sort(self):
        def sortFunction(e): #this is python.  We can have nested functions.
            return e.get_speed()
        queue_list = self.entity_list
        queue_list.sort(key = sortFunction) #sort by lowest to highest speed
        return queue_list #list is also a stack with the highest speed at the end that can be called using pop()

    async def turn_queue(self, queue_list):
        #Might need to revise later.
        queue = []
        for i in queue_list:
            queue.append(i)
        stack = []
        for i in range(len(queue)):
            current_piece=queue.pop()
            stack.append(current_piece) #add to stack from queue the piece with the highest speed and perform its action one a time
            await stack[i].get_action(self.duel_helper)
        return stack #stack will now contain entity_list from highest to lowest speed

    async def start_game(self):
        #Game Loop is here.
        self.game_is_active=True
        while (self.game_is_active):
            print("PUT GAME LOOP HERE.")
            await self.turn_queue(self.turn_sort()) #not sure if this is correct
            self.round=self.round+1
            print(self.round)
            await self.update_grid_image()
            await asyncio.sleep(1)
            if(self.round>5):
                self.game_is_active=False
        print("TBD.")


class Card_Duel_Helper():
    #This class will help with processing game events game.
    def __init__(self, Duel):
        print("TBD.  Might do something.")
        self.__card_duel=Duel
    def get_entity_list(self):
        new_list=[]
        for v in self.__card_duel.entity_list:
            new_list.append(v)
        return new_list
    def get_grid(self):
        return self.__card_duel.grid
    async def make_move_preview(self, spaces):
        img=await self.__card_duel.move_preview(spaces)
        return img
    def set_update(self):
        self.__card_duel.grid_updated()
    def request_termination(self):
        print("To Be Completed.")
    async def send_user_updates(self):
        await self.__card_duel.update_grid_image()
