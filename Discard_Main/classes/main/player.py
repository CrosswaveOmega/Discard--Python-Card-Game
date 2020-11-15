import discord
import operator
import io
import json
import aiohttp
import asyncio
import csv
import datetime
import queue

import random
from PIL import Image, ImageTk, ImageGrab, ImageDraw, ImageFont

from discord.ext import commands, tasks
from discord.utils import find
from discord import Webhook, AsyncWebhookAdapter

from ..DiscordPlayerInputOutputSystem import *
#The player class.  FOR THE GAME.
class Player():
    def __init__(self, player_type="", deck=[], team=1):
        self.PlayerType=player_type
        self.id="Play" #I don't know why we have this one.
        self.deck=deck #Should be a list of cards. Initalization prior might be useful.
        self.hand=[] #Cards in hand.
        self.graveyard=[]#All cards in the graveyard.
        self.team=team#The team the player is on.

        self.leader=None #The leader piece of the user.

        self.summon_r=0.0
        self.summon_b=0.0
        self.summon_g=0.0
        #Initialize any other gameplay variables here as we need them.
    def gain_summon_points(self):
        #exactly how to gain Summon points, I still have no idea.
        #this will give points randomly.
        self.summon_r=self.summon_r+0.20
        self.summon_b=self.summon_b+0.2
        self.summon_g=self.summon_g+0.2
        for i in range(0,5):
            val=random.randint(1,3)
            if val ==1:
                self.summon_r=self.summon_r+0.2
            if val==2:
                self.summon_b=self.summon_b+0.2
            if val==3:
                self.summon_g=self.summon_g+0.2


    def set_leader(self, leader):
        self.leader=leader
    def get_PlayerType(self):
        return self.PlayerType
    async def select_command(self, options=[]):
            #get input from dpios.
        pass
    async def select_option(self, options=[]):
        pass
    def draw_card(self):
        card=self.deck.pop()
        self.hand.append(card)

    def get_input(self):
        return "TBD"
    def get_output(self):
        #Ask for infomation here.
        print("TBD")
    def to_embed(self, view):
        hand_disp=len(self.hand)
        if view=='self':
            string="Hand\n"
            for card in self.hand:
                string=string + "{}\n".format(str(card))
            hand_disp=string

        embed = discord.Embed(title="Player", colour=discord.Colour(0xce48e9), description="{}".format(hand_disp), timestamp=datetime.datetime.now())
        mana=" Red= {}\n Blue= {}\n Green= {}".format( str(round(self.summon_r, 2)), str(round(self.summon_b, 2)),str(round(self.summon_g, 2)))
        embed.add_field(name="Leader", value= self.leader.string_status(), inline=True)
        embed.add_field(name="Mana", value=mana, inline=True)
        embed.add_field(name="Deck", value=str(len(self.deck)), inline=True)
#embed.add_field(name="custom", value="Custom was applied.",)
        embed.add_field(name="Exp", value="0", inline=True)
        embed.add_field(name="Level", value="0", inline=True)
        embed.add_field(name="graveyard", value=str(len(self.graveyard)), inline=True)
        return embed
    async def send_embed_to_user(self):
        await asyncio.sleep(1)


class DiscordPlayer(Player):
    def __init__(self, deck=[], team=1, dpios=None):
        player_type="Discord"
        self.dpios=dpios
        super().__init__(player_type="Discord", deck=deck, team=team)
    def get_avatar_url(self):
        return self.dpios.get_avatar_url()
    def get_input(self):
        return None
    def get_dpios(self):
        return self.dpios
    async def select_command(self, options=[]):
            #get input from dpios.
        option= await self.dpios.get_user_command(options)
        return option
    async def select_option(self, options=[]):
        #get input from dpios.
        option= await self.dpios.get_user_choice(options)
        return option
    async def send_embed_to_user(self):
        embed=self.to_embed('self')
        await self.dpios.update_player_message(embed)
