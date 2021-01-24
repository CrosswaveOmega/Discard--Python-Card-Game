import discord
import operator
import io
import json
import aiohttp
import asyncio
import csv
import datetime
import queue

from ..Cards import SpellResult
from PIL import Image, ImageTk, ImageGrab, ImageDraw, ImageFont

from discord.ext import commands, tasks
from discord.utils import find
from discord import Webhook, AsyncWebhookAdapter

from .generic.position import Position

from ..imagemakingfunctions.imaging import *
from .target_matching import match_with_target_data

class SpellSlot():
    def __init__(self):
        self.filled=False #Is the Spell Slot Filled with a Spell Card.

        self.revealed=False #If the Spell Slot is filled, is the spell revealed.
        #Revealed spells can be seen by opponents.
        self.activated=False #is the spell activated.

        self.spell_card=None #The card currently occupying the slot.
        self.bp=0 #The current BP of the spell inside the slot.

        self.turns_set=0 #if the slot is filled, the number of turns it's been set.

    def set_spell(self, card:SpellCard):
        """Fill the spell slot with a spell card.
        param: card.  The SpellCard to fill with.
        """
        self.spell_card=card
        self.filled=True
        self.revealed=False
        self.activated=False

        self.bp =card.bp
        self.turns_set=0

    def remove_spell(self):
        """removes the spell card, and returns the SpellCard object."""
        card=self.spell_card
        self.spell_card=None
        self.filled=False
        return card

    def do_set_effect(self, user, game_ref=None):
        """if the spell is set, do the set effect."""

    def check_activate(self, user, game_ref=None):
        """Check if you can activate."""

    async def activate_spell(self, user, game_ref=None):
        """Activate Spell."""
        """Activate the spell card."""
        """Will return a SpellResult enum."""
        """user is the player's Leader piece."""
        if self.filled ==True:
            if self.check_activate(user, game_ref):
                result=await self.spell_card.activate_spell(self, user, game_ref)
                if result == SpellResult.Finished:
                    print("OK")
