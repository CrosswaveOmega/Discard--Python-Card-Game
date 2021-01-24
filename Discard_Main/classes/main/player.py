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
    def __init__(self, player_type="", deck=[], team=1, name="Default"):
        self.PlayerType = player_type
        self.id = "Play"  # I don't know why we have this one.
        self.name= name
        self.deck = deck  # Should be a list of cards. Initalization prior might be useful.
        self.hand = []  # Cards in hand.
        self.graveyard = []  # All cards in the graveyard.
        self.spell_slots = {} #the spell slots currently set.

        self.team = team  # The team the player is on.
        self.active= True

        self.leader = None  # The leader piece of the user.

        self.summon_r = 1.0
        self.summon_b = 1.0
        self.summon_g = 1.0
        self.summon_u = 1.0 #universal mana.

        self.fp = 0 #Flower points.
        self.max_fp = 20

        self.status="OK"
        # Initialize any other gameplay variables here as we need them.
    def set_status(self, status="OK"):
        self.status=status
    def get_status(self):
        return self.status
    def get_fp(self):
        return self.fp
    def gain_fp(self, fp=1):
        self.fp=self.fp+fp
        if(self.fp>=self.max_fp):
            self.fp=self.max_fp
    def sub_fp(self, fp=1):
        self.fp=self.fp-fp
        if self.fp<=0:
            self.fp=0
    def gain_summon_points(self):
        # exactly how to gain Summon points, I still have no idea.
        # this will give points randomly.
        self.summon_u = self.summon_u + 1
        self.summon_r = self.summon_r + 1
        self.summon_b = self.summon_b + 1
        self.summon_g = self.summon_g + 1

        # for i in range(0, 10):
        #     val = random.randint(1, 3)
        #     if val == 1:
        #         self.summon_r = self.summon_r + 0.2
        #     if val == 2:
        #         self.summon_b = self.summon_b + 0.2
        #     if val == 3:
        #         self.summon_g = self.summon_g + 0.2

    def set_leader(self, leader):
        self.leader = leader
    def get_leader(self, leader):
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

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def draw_card(self):
        if (len(self.deck) >= 1):
            card = self.deck.pop()
            self.hand.append(card)
            return "Added {} to hand.".format(str(card))
        return "Your deck is empty."

    async def get_focus_action(self, game_ref, focus_value=1.5):
        valid_options = ["RED", "BLUE", "GREEN"]
        valuetoadd=focus_value
        choice = await self.select_option(valid_options, "Where would you like to focus?")
        if (choice == 'back' or choice == 'timeout' or choice=="invalidmessage"):
            if(choice=="invalidmessage"):
                await self.send_announcement("unrecognized string was sent in.")
            return False
        if choice=="RED":
            self.summon_r = self.summon_r + 1.5
        if choice=="BLUE":
            self.summon_b = self.summon_b + 1.5
        if choice=="GREEN":
            self.summon_g = self.summon_g + 1.5
        await game_ref.send_announcement("Focused {} extra {} mana".format(1.5, choice))
        return True

    async def get_set_action(self, game_ref):
        #Set a spell card.
        print("TBD")
        valid_options=[]
        for card in self.hand:
            if card.get_type() == "Spell":
                if (card.can_set(self)):
                    valid_options.append(card)
        card = await self.select_card(valid_options, "select a spell card to set.")
        if (card == 'back' or card == 'timeout' or card=="invalidmessage"):
            if(card=="invalidmessage"):
                await self.send_announcement("unrecognized string was sent in.")
            return False
        self.spell_slots.append(card)
        self.hand.remove(card)
        card.set_spell()


    async def get_summon_action(self, game_ref, summon_locations):
        valid_options = []
        #1: Check if within creature limit, if
        #2: check if you need card points to summon
        #3: check if you need separate flavors to summon.
        for card in self.hand:
            if card.get_type() == "Creature":
                if (card.can_activate(self.summon_r, self.summon_b, self.summon_g, self.summon_u) or game_ref.check_setting('card_point_summons')==False):
                    valid_options.append(card)
        card = await self.select_card(valid_options, "select a card.")
        if (card == 'back' or card == 'timeout' or card=="invalidmessage"):
            if(card=="invalidmessage"):
                await self.send_announcement("unrecognized string was sent in.")
            return False
        position_not = await self.select_option(summon_locations, "Where should it summon to?")
        if (position_not != "back" and position_not != "timeout"and position_not!="invalidmessage"):
            print(position_not)
            new_creature = Creature(card, self, position_not)
            self.hand.remove(card)
            game_ref.add_creature(new_creature)
            await game_ref.send_user_updates()

            r, b, g = card.get_cost_tuple()
            await game_ref.send_announcement("{} Summoned to {}".format(card.get_name(), position_not))
            if game_ref.check_setting('card_point_summons'):
                self.summon_r = self.summon_r - r
                self.summon_b = self.summon_b - b
                self.summon_g = self.summon_g - g
                if self.summon_r < 0:
                    self.summon_u = self.summon_u - abs(self.summon_r)
                    self.summon_r=0
                if self.summon_b < 0:
                    self.summon_u = self.summon_u - abs(self.summon_b)
                    self.summon_b=0
                if self.summon_g < 0:
                    self.summon_u = self.summon_u - abs(self.summon_g)
                    self.summon_g=0
            return True
        return False

    def get_input(self):
        return "TBD"

    def get_output(self):
        print("TBD")

    def get_team(self):
        return self.team
    def get_name(self):
        return self.name

    def buffer(self):
        return True

    def get_summon_point_string(self):
        mana = " Red={}  Blue= {} Green= {}".format(str(round(self.summon_r, 2)), str(round(self.summon_b, 2)),
                                                        str(round(self.summon_g, 2)))
        return mana

    def to_embed(self, view):
        hand_disp = len(self.hand)
        if view == 'self':
            string = "Hand\n"
            for card in self.hand:
                string = string + "{}\n".format(str(card))
            hand_disp = string

        embed = discord.Embed(title="Player", colour=discord.Colour(0xce48e9), description="{}".format(hand_disp),
                              timestamp=datetime.datetime.now())
        mana = " Red= {}\n Blue= {}\n Green= {}\n Universal= {}".format(str(round(self.summon_r, 2)), str(round(self.summon_b, 2)),
                                                        str(round(self.summon_g, 2)), str(round(self.summon_u, 2)))
        deckgrave="**Deck:**{}\n\n**Graveyard**:{}".format(len(self.deck), len(self.graveyard))
        embed.add_field(name="Leader", value=self.leader.string_status(), inline=True)
        embed.add_field(name="Mana", value=mana, inline=True)
        embed.add_field(name="-", value=deckgrave, inline=True)
        # embed.add_field(name="custom", value="Custom was applied.",)
        embed.set_footer(text="FP: {}".format(self.get_fp()))
        return embed
    async def local_commands(self, action, game_ref):
        return True, False
    async def send_embed_to_user(self):
        pass
        #await asyncio.sleep(1)


class DiscordPlayer(Player):
    def __init__(self, deck=[], team=1, dpios=None):
        player_type = "Discord"
        self.dpios = dpios
        super().__init__(player_type="Discord", deck=deck, team=team, name=self.dpios.get_user_name())
    def get_user_name(self):
        return self.dpios.get_user_name()
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
        completed = False
        if (action == "OVERVIEW"):
            await self.dpios.send_order()
        elif (action == "PLAYER"):
            await self.dpios.send_order(p=True, i=False, c=False)
        elif (action == "BOARD"):
            await self.dpios.send_order(p=False, i=True, c=False)
        elif (action == "CURRENT"):
            await self.dpios.send_order(p=False, i=False, c=True)
        elif (action == "QUIT"):
            print("LOCAL COMMAND: QUIT DETECTED.")
            game_ref.force_check()
            self.set_status("QUIT")
            my_turn= False
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

    async def send_announcement(self, announcement, sent=True):
        await self.dpios.send_announcement(announcement, sent)

class TestPlayer(Player):
    def __init__(self, deck=[], team=1, dpios=None, name="TEST", command_series=[]):
        player_type = "Test"
        self.dpios = dpios
        self.dpios.set_input_buffer(command_series)
        super().__init__(player_type="Test", deck=deck, team=team, name=name)
    def get_user_name(self):
        return self.dpios.get_user_name()
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
        completed = False
        if (action == "OVERVIEW"):
            await self.dpios.send_order()
        elif (action == "PLAYER"):
            await self.dpios.send_order(p=True, i=False, c=False)
        elif (action == "BOARD"):
            await self.dpios.send_order(p=False, i=True, c=False)
        elif (action == "CURRENT"):
            await self.dpios.send_order(p=False, i=False, c=True)
        elif (action == "QUIT"):
            print("LOCAL COMMAND: QUIT DETECTED.")
            game_ref.force_check()
            self.set_status("QUIT")
            my_turn= False
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

    async def send_announcement(self, announcement, sent=True):
        await self.dpios.send_announcement(announcement, sent)
