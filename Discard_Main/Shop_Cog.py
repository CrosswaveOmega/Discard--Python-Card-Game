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
from .classes.Cards.cardretrieval import CardRetrievalClass

from .classes.discordhelper import *

from .classes.Cards.custom import CustomRetrievalClass
from .classes.imagemakingfunctions.imaging import *
from .classes.userservices.userprofile import SingleUserProfile
from .classes.Cards.DeckBuilding import *
from .how_to_play.howtoplayembeds import make_how_to_play_embeds

# from discord.ext.tasks import loop


# <a:stopwatch:774741008495542284>
# <a:stopwatch_15:774741008793337856>


class ShopCog(commands.Cog):
    """This is for the shop system."""
    @commands.group()
    async def shop(self, ctx):
        bot=ctx.bot
        channel=ctx.message.channel
        if ctx.invoked_subcommand is None:
            #send front page.
            await ctx.channel.send("Shop under construction.  In the meantime, you can use the >shop random to get a random new card.")
    @shop.command()
    async def page(self, ctx):
     #   print(str(val))
        await ctx.channel.send("Shop under construction!")
    @shop.command()
    async def random(self, ctx):
     #   print(str(val))
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        SingleUser = SingleUserProfile("arg")

        user_id = author.id
        profile = SingleUser.getByID(user_id)

        all_cards=CardRetrievalClass().getAllCards()
        ids=[]
        for card in all_cards:
            id=card.get_ID()
            print("id")
            if not profile.has_card(id):
                ids.append(card)

        if (len(ids)<= 0):
            await channel.send("You have all the cards.")
        else:
            card_id=(random.choice(ids)).get_ID()
            profile.add_card(card_id)
            await channel.send("Card {} added.".format(card_id))
        SingleUser.save_all()
    @shop.command()
    async def buy(self, ctx, objectname:str):
     #   print(str(val))
        await ctx.channel.send("Your object name is {}.".format(objectname))
