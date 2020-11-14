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

class Card_Duel():
    """Where the game will be played."""
    def __init__(self):
        dicti=vars(Grid())
        print(json.dumps(dicti))
        self.game_id=0
        self.val=0
        self.players=[]
        self.entity_list=[]

        self.mode="Test" #the "mode" of the game.  a simplified setting.
        self.settings=None #Settings of the game.
        self.duel_helper=Card_Duel_Helper(self)
        self.grid=Grid(5,5,self.duel_helper)


        self.round=0
        self.log=[] #Log of everything that happened.
        self.game_is_active=False

    def apply_settings(self, settings=None):
        if settings!=None:
            self.settings=settings
    def addPlayer(self, player=None):
        if(player!=None):
            self.players.append(player)

    async def send_grid(self): #A WIP function.  it sends a grid to all players.
        pilgrid=self.grid.grid_to_PIL_array()
        img=make_image_from_grid(pilgrid, self.grid.columns, self.grid.rows)
        for player in self.players:
            if(player.get_PlayerType()=="Discord"):
                await player.get_dpios().send_pil_image(img)

    def add_piece(self, piece):
        self.entity_list.append(piece)
    def move_piece(self, piece):
        piece.get_move_options(self.grid)

    def turn_sort(self):
        def sortFunction(e): #this is python.  We can have nested functions.
            return e.get_speed()
        queue_list = self.entity_list
        queue_list.sort(key = sortFunction) #sort by lowest to highest speed
        return queue_list #list is also a stack with the highest speed at the end that can be called using pop()

    async def turn_queue(self, queue_list):
        queue = []
        for i in queue_list:
            queue.append(i)
        stack = []
        for i in range(len(queue)):
            stack.append(queue.pop()) #add to stack from queue the piece with the highest speed and perform its action one a time
            await stack[i].get_action()
        return stack #stack will now contain entity_list from highest to lowest speed

    async def start_game(self):
        #Game Loop is here.
        self.game_is_active=True
        while (self.game_is_active):
            print("PUT GAME LOOP HERE.")
            await self.turn_queue(self.turn_sort()) #not sure if this is correct
            self.round=self.round+1
            await asyncio.sleep(1)
            if(self.round>10):
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
