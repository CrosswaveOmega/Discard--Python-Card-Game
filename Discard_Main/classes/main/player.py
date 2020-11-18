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

from .piece import Creature
from ..DiscordPlayerInputOutputSystem import *


# The player class.  FOR THE GAME.
class Player():
    def __init__(self, player_type="", deck=[], team=1):
        self.PlayerType = player_type
        self.id = "Play"  # I don't know why we have this one.
        self.deck = deck  # Should be a list of cards. Initalization prior might be useful.
        self.hand = []  # Cards in hand.
        self.graveyard = []  # All cards in the graveyard.
        self.team = team  # The team the player is on.

        self.leader = None  # The leader piece of the user.

        self.summon_r = 0.0
        self.summon_b = 0.0
        self.summon_g = 0.0
        # Initialize any other gameplay variables here as we need them.

    def gain_summon_points(self):
        # exactly how to gain Summon points, I still have no idea.
        # this will give points randomly.
        self.summon_r = self.summon_r + 1
        self.summon_b = self.summon_b + 1
        self.summon_g = self.summon_g + 1
        for i in range(0, 10):
            val = random.randint(1, 3)
            if val == 1:
                self.summon_r = self.summon_r + 0.2
            if val == 2:
                self.summon_b = self.summon_b + 0.2
            if val == 3:
                self.summon_g = self.summon_g + 0.2

    def set_leader(self, leader):
        self.leader = leader

    def get_PlayerType(self):
        return self.PlayerType

    async def select_piece(self, options=[], prompt=""):
        # get input from dpios.
        pass

    async def select_command(self, options=[], prompt=""):
        # get input from dpios.
        pass

    async def select_option(self, options=[], prompt=""):
        pass

    async def select_card(self, options=[], prompt=""):
        pass
    def card_to_graveyard(self, card):
        self.graveyard.append(card)
    def draw_card(self):
        if (len(self.deck) >= 1):
            card = self.deck.pop()
            self.hand.append(card)
            return "Added {} to hand.".format(str(card))
        return "Your deck is empty."

    async def get_summon_action(self, game_ref, summon_locations):
        valid_options = []
        for card in self.hand:
            if card.get_type() == "Creature":
                if (card.can_activate(self.summon_r, self.summon_b, self.summon_g)):
                    valid_options.append(card)
        card = await self.select_card(valid_options, "select a card.")
        if (card == 'back' or card == 'timeout' or card=="invalidmessage"):
            if(card=="invalidmessage"):
                await self.send_announcement("unrecognized string was sent in.")
            return False
        position_not = await self.select_option(summon_locations, "Where should it summon to?")
        if (position_not != "back" and position_not != "timeout"):
            print(position_not)
            new_creature = Creature(card, self, position_not)
            self.hand.remove(card)
            game_ref.add_creature(new_creature)

            r, b, g = card.get_summoncost_tuple()
            await game_ref.send_announcement("{} Summoned to {}".format(card.get_name(), position_not))
            self.summon_r = self.summon_r - r
            self.summon_b = self.summon_b - b
            self.summon_g = self.summon_g - g
            return True
        return False

    def get_input(self):
        return "TBD"

    def get_output(self):
        print("TBD")

    def get_team(self):
        return self.team

    def buffer(self):
        return True

    def to_embed(self, view):
        hand_disp = len(self.hand)
        if view == 'self':
            string = "Hand\n"
            for card in self.hand:
                string = string + "{}\n".format(str(card))
            hand_disp = string

        embed = discord.Embed(title="Player", colour=discord.Colour(0xce48e9), description="{}".format(hand_disp),
                              timestamp=datetime.datetime.now())
        mana = " Red= {}\n Blue= {}\n Green= {}".format(str(round(self.summon_r, 2)), str(round(self.summon_b, 2)),
                                                        str(round(self.summon_g, 2)))
        embed.add_field(name="Leader", value=self.leader.string_status(), inline=True)
        embed.add_field(name="Mana", value=mana, inline=True)
        embed.add_field(name="Deck", value=str(len(self.deck)), inline=True)
        # embed.add_field(name="custom", value="Custom was applied.",)
        embed.add_field(name="Exp", value="0", inline=True)
        embed.add_field(name="Level", value="0", inline=True)
        embed.add_field(name="graveyard", value=str(len(self.graveyard)), inline=True)
        return embed
    async def local_commands(self, action, game_ref):
        return True, False
    async def send_embed_to_user(self):
        await asyncio.sleep(1)


class DiscordPlayer(Player):
    def __init__(self, deck=[], team=1, dpios=None):
        player_type = "Discord"
        self.dpios = dpios
        super().__init__(player_type="Discord", deck=deck, team=team)

    def get_avatar_url(self):
        return self.dpios.get_avatar_url()

    def has_something_in_buffer(self):
        return self.dpios.has_something_in_buffer()
    def get_input(self):
        return None

    def get_dpios(self):
        return self.dpios

    async def local_commands(self, action, game_ref):
        my_turn = True
        print(action)
        completed = False
        if (action == "OVERVIEW"):
            await self.dpios.send_order()
        elif (action == "PLAYER"):
            await self.dpios.send_order(p=True, i=False, c=False)
        elif (action == "BOARD"):
            await self.dpios.send_order(p=False, i=True, c=False)
        elif (action == "CURRENT"):
            await self.dpios.send_order(p=False, i=False, c=True)
        return my_turn, completed
    async def select_piece(self, options=[], prompt="Select a piece"):
        option = await self.dpios.get_user_piece(options, prompt)
        return option

    async def select_command(self, options=[], prompt="Enter a command"):
        # get input from dpios.
        option = await self.dpios.get_user_command(options, prompt)
        return option

    async def select_option(self, options=[], prompt="Select a choice"):
        # get input from dpios.
        option = await self.dpios.get_user_choice(options, prompt)
        return option

    async def select_card(self, options=[], prompt="Select a card"):
        # get input from dpios.
        option = await self.dpios.get_user_card(options, prompt)
        return option

    async def send_embed_to_user(self):
        embed = self.to_embed('self')
        await self.dpios.update_player_message(embed)

    async def send_announcement(self, announce="blank."):
        await self.dpios.send_announcement(announce)
