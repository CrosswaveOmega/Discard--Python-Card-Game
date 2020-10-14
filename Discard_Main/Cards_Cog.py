import discord
import operator
import io
import json
import aiohttp
import asyncio
import csv
from discord.ext import commands, tasks
from discord.utils import find
from discord import Webhook, AsyncWebhookAdapter
from .classes.Cards.cardretrieval import CardRetrievalClass

from .classes.Cards.custom import CustomRetrievalClass
#from discord.ext.tasks import loop


class CardCog(commands.Cog):
    """Commands for cards."""
    @commands.command(pass_context=True, aliases=['stampV'])
    async def stamp(self, ctx, *args):
        bot=ctx.bot
        auth=ctx.message.author;
        channel=ctx.message.channel;
        leng=len(args)


    @commands.command(pass_context=True)
    async def cardGet(self, ctx, *args): #A very rudimentary card retrieval system.
        bot=ctx.bot
        auth=ctx.message.author;
        channel=ctx.message.channel;
        newcard=CardRetrievalClass().getByID(0x000FF)

        await channel.send(str(newcard))
        if newcard!=False:
            text=await CustomRetrievalClass().getByID(args[0], bot)

            newcard.apply_custom(custom=text)
        #    print(text)
            await channel.send(str(newcard))
