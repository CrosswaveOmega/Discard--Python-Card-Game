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


async def pages(ctx, display=[], perpage=5, header="new", content="new"):
    # seems self explanitory
    spot = 0
    running = True
    length = len(display)
    largest_spot = ((length - 1) // perpage) * perpage
    maxpages = ((length - 1) // perpage) + 1
    emb = discord.Embed(title=header, colour=discord.Colour(
        0x7289da), description=content)
    page = (spot // perpage) + 1
    emb.set_author(name=" Page {}/{}, {} total".format(page, maxpages, length))
    # <a:stopwatch:774737394594218035>
    # <a:stopwatch_15:774737457371152396>

    message = await ctx.channel.send(content="active", embed=emb)
    while running:
        page = (spot // perpage) + 1

        emb = discord.Embed(title=header, colour=discord.Colour(
            0x7289da), description=content)
        emb.set_author(
            name=" Page {}/{}, {} total".format(page, maxpages, length))
        numberlist = ["1️⃣", "2️⃣", "3️⃣", "4️⃣",
                      "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        c = 0
        for i in display[spot:spot + perpage]:
            emb.add_field(name=str(numberlist[c]), value=i, inline=False)
            c = c + 1
        await message.edit(content="active", embed=emb)
        choices = []
        defchoice = ["exit", "", '⏹️']
        choices.append(defchoice)
        choices.append(["first", "", '⏮️'])
        choices.append(["back", "", '◀️'])
        choices.append(["next", "", '▶️'])
        choices.append(["last", "", '⏭️'])
        # for i in range(0,c):
        #    choices.append([str(i),"", numberlist[i]])
        result = await make_tiebreaker(ctx, choices, message=message, timeout_enable=True, ignore_message=True,
                                       remove_after=True)
        if (result == 'timeout' or result == 'exit'):
            # WILL TERMINATE.
            running = False
            await message.clear_reactions()
            await message.edit(content="Done.", embed=emb)
        if result == "next":
            spot = spot + perpage
            if (spot) >= length:
                spot = spot - perpage
        if result == "back":
            spot = spot - perpage
            if spot < 0:
                spot = 0
        if result == "first":
            spot = 0
        if result == "last":
            spot = largest_spot


async def pages_of_cards(ctx, display=[], deck_mode=False, profile=None):
    # seems self explanitory
    bot=ctx.bot
    spot = 0
    running = True
    perpage=1
    length = len(display)
    largest_spot = ((length - 1) // perpage) * perpage
    maxpages = ((length - 1) // perpage) + 1

    page = (spot // perpage) + 1

    message = await ctx.channel.send(content="Cards")
    while running:
        page = (spot // perpage) + 1
        key=""
        if deck_mode:
            ent=display[page-1]

            c, k=display[page-1]
            emb=c.to_DiscordEmbed()
            key=k
        else:
            emb=display[page-1].to_DiscordEmbed()
        emb.set_author(
            name=" Page {}/{}, {} total".format(page, maxpages, length))

        numberlist = ["1️⃣", "2️⃣", "3️⃣", "4️⃣",
                      "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        c = 0
        await message.edit(content="active", embed=emb)
        choices = []
        defchoice = ["exit", "", '⏹️']
        choices.append(defchoice)
        choices.append(["first", "", '⏮️'])
        choices.append(["back", "", '◀️'])
        choices.append(["next", "", '▶️'])
        choices.append(["last", "", '⏭️'])
        if(deck_mode):
            choices.append(["add_to_deck", "", '<:add_to_deck:780476387098099722>'])
            choices.append(["remove_from_deck", "", '<:remove_from_deck:780476387148169236>'])
        # for i in range(0,c):
        #    choices.append([str(i),"", numberlist[i]])
        result = await make_tiebreaker(ctx, choices, message=message, timeout_enable=True, ignore_message=True,
                                       remove_after=True, timeout_time=60.0)
        if (result == 'timeout' or result == 'exit'):
            # WILL TERMINATE.
            running = False
            await message.clear_reactions()
            await message.edit(content="Done.", embed=emb)
        if result == "next":
            spot = spot + perpage
            if (spot) >= length:
                spot = spot - perpage
        if result == "back":
            spot = spot - perpage
            if spot < 0:
                spot = 0
        if result == "first":
            spot = 0
        if result == "last":
            spot = largest_spot
        if result == "add_to_deck":
            if profile!=None:
                deck = profile.get_primary_deck()
                if deck!=None:
                    playerDeck = deck
                    deckName=playerDeck.get_deck_name()
                    await ctx.invoke(bot.get_command('addToDeck'), deckName, key)
                else:
                    await ctx.channel.send("You never set a primary deck.  User the >setPrimaryDeck command to set one.")
        if result == "remove_from_deck":
            if profile!=None:
                deck = profile.get_primary_deck()
                if deck!=None:
                    playerDeck = deck
                    deckName=playerDeck.get_deck_name()
                    await ctx.invoke(bot.get_command('removeFromDeck'), deckName, key)
                else:
                    await ctx.channel.send("You never set a primary deck.  User the >setPrimaryDeck command to set one.")

async def pages_of_embeds(ctx, display=[]):
    # seems self explanitory
    bot=ctx.bot
    spot = 0
    running = True
    perpage=1
    length = len(display)
    largest_spot = ((length - 1) // perpage) * perpage
    maxpages = ((length - 1) // perpage) + 1

    page = (spot // perpage) + 1

    message = await ctx.channel.send(content="page")
    while running:
        page = (spot // perpage) + 1
        key=""
        emb=display[page-1]
        emb.set_author(
            name=" Page {}/{}, {} total".format(page, maxpages, length))

        numberlist = ["1️⃣", "2️⃣", "3️⃣", "4️⃣",
                      "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        c = 0

        await message.edit(content="active", embed=emb)
        choices = []
        defchoice = ["exit", "", '⏹️']
        choices.append(defchoice)
        choices.append(["first", "", '⏮️'])
        choices.append(["back", "", '◀️'])
        choices.append(["next", "", '▶️'])
        choices.append(["last", "", '⏭️'])

        result = await make_tiebreaker(ctx, choices, message=message, timeout_enable=True, ignore_message=True,
                                       remove_after=True, timeout_time=60.0)
        if (result == 'timeout' or result == 'exit'):
            # WILL TERMINATE.
            running = False
            await message.clear_reactions()
            await message.edit(content="Done.", embed=emb)
        if result == "next":
            spot = spot + perpage
            if (spot) >= length:
                spot = spot - perpage
        if result == "back":
            spot = spot - perpage
            if spot < 0:
                spot = 0
        if result == "first":
            spot = 0
        if result == "last":
            spot = largest_spot
