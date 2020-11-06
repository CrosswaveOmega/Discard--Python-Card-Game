import discord
import operator
import io
from io import StringIO
import urllib
from urllib.request import Request, urlopen
import aiohttp
import asyncio
import json
import re
import math
import time
import datetime
import unicodedata
from collections import OrderedDict
from configparser import ConfigParser



import messageConfirming as messageIOfunctions
import discord

from discord.ext import commands, tasks
from discord.utils import find
from discord import Webhook, AsyncWebhookAdapter
#from discord.ext.tasks import loop
import random

from Discard_Main import Cards_Cog
from Discard_Main import Cards_Custom_Cog

from Discard_Main import Cards_Debug_Cog
from Discard_Main import Cards_Deckbuilding_Cog


bot = commands.Bot(command_prefix='>')

async def opening():
    print("OK.")


@bot.event
async def on_ready():
    print("Activating Bot.")
    await opening()
    print("BOT ACTIVE")

class Main(commands.Cog):
    """
    a basic class.
    """
    @commands.Cog.listener()
    async def on_message(self, message):
        '''
        This will fire whenever a message is given.
        '''
        user=message.author
        channel=message.channel
        if user != bot.user:
            if channel.id == 749673636280926228:
                await channel.send("HELLO I AM ME!")
bot.add_cog(Main())
bot.add_cog(Cards_Cog.CardCog())
bot.add_cog(Cards_Cog.CardCog2())
bot.add_cog(Cards_Deckbuilding_Cog.DeckCog())
bot.add_cog(Cards_Debug_Cog.DebugCog())
bot.add_cog(Cards_Custom_Cog.CustomsCog())
configur=ConfigParser()
configur.read('config.ini')
print(configur)
bot.run(configur.get("Default",'cipher'))
