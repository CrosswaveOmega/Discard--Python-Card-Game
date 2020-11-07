import discord
import operator
import io
import json
import aiohttp
import asyncio
import csv
import datetime
from PIL import Image, ImageTk, ImageGrab, ImageDraw, ImageFont

from discord.ext import commands, tasks
from discord.utils import find
from discord import Webhook, AsyncWebhookAdapter

from .tiebreaker import *

async def pages(ctx, display=[], perpage=5):

    #seems self explanitory
    spot=0
    running=True
    emb=discord.Embed(title="New", colour=discord.Colour(0x7289da), description="name")

#<a:stopwatch:774737394594218035>
#<a:stopwatch_15:774737457371152396>

    message=await ctx.channel.send(content="active", embed=emb)
    while running:
        emb=discord.Embed(title="New", colour=discord.Colour(0x7289da), description="Description")
        numberlist=["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
        c=0
        for i in display[spot:spot+perpage]:
            emb.add_field(name=str(numberlist[c]), value=i, inline=False)
            c=c+1
        await message.edit(content="active",embed=emb)
        choices=[]
        defchoice=["exit","", '⏹️']
        choices.append(defchoice)
        choices.append(["back","", '◀️'])
        choices.append(["next","", '▶️'])
        result=await make_tiebreaker(ctx, choices, message=message, timeout_enable=True, ignore_message=True, remove_after=True)
        if(result=='timeout' or result=='exit'):
            #WILL TERMINATE.
            running=False
            await message.clear_reactions()
            await message.edit(content="Done.", embed=emb)

        if result=="next":
            spot=spot+perpage
            if(spot)>len(display):
                spot=spot-perpage
        if result=="back ":
            spot=spot-perpage
            if spot < 0:
                spot=0
