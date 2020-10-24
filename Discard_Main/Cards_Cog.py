import discord
import operator
import io
import json
import aiohttp
import asyncio
import csv

from PIL import Image, ImageTk, ImageGrab, ImageDraw, ImageFont

from discord.ext import commands, tasks
from discord.utils import find
from discord import Webhook, AsyncWebhookAdapter
from .classes.Cards.cardretrieval import CardRetrievalClass

from .classes.Cards.custom import CustomRetrievalClass
from .classes.imagemakingfunctions.imaging import *
from .classes.userservices.userprofile import SingleUserProfile
#from discord.ext.tasks import loop


class CardCog(commands.Cog):
    """Commands for cards."""
    @commands.command(pass_context=True, aliases=['stampV'])
    async def stamp(self, ctx, *args):
        bot=ctx.bot
        auth=ctx.message.author;
        channel=ctx.message.channel;
        leng=len(args)
    @commands.command(pass_context=True, aliases=['cardtest'])
    async def getimage(self, ctx, *args):
        bot=ctx.bot
        auth=ctx.message.author;
        channel=ctx.message.channel;
        leng=len(args)
        with io.BytesIO() as image_binary:
            make_summon_cost(1,1,1).save(image_binary, 'PNG') #Returns pil object.
            image_binary.seek(0)
            await channel.send(file=discord.File(fp=image_binary, filename='image.png'))

    @commands.command()
    async def add_exp(self, ctx, *args): #A very rudimentary card retrieval system.
        '''
        syntax: cardGet [CardId] CustomId]
        Gets a random genre out of the character-info channel.  Exlcusively for Sakura Beat.
        [CardId]: The Card ID you want to get.
        [CustomId]: The CustomId you want to apply to the card.

        '''
        bot=ctx.bot
        auth=ctx.message.author;
        channel=ctx.message.channel;
        SingleUser=SingleUserProfile("New.")
        profile=SingleUser.getByID(auth.id)
        await channel.send("Old EXP="+str(profile.get_exp()))
        profile.set_exp(profile.get_exp()+10)
        profile=SingleUser.getByID(auth.id)
        await channel.send("New EXP="+str(profile.get_exp()))
        SingleUser.save_all()
        #await channel.send(str(newcard))

    @commands.command(pass_context=True)
    async def cardGet(self, ctx, *args): #A very rudimentary card retrieval system.
        '''
        syntax: cardGet [CardId] CustomId]
        Gets a random genre out of the character-info channel.  Exlcusively for Sakura Beat.
        [CardId]: The Card ID you want to get.
        [CustomId]: The CustomId you want to apply to the card.

        '''
        bot=ctx.bot
        auth=ctx.message.author;
        channel=ctx.message.channel;
        leng=len(args)
        if(leng>=1):
            id=args[0]
            newcard=CardRetrievalClass().getByID(int(id, 16))
            await channel.send(str(newcard))
            if newcard!=False and leng>=2:
                text=await CustomRetrievalClass().getByID(args[1], bot)

                print(text.toCSV())

                newcard.apply_custom(custom=text)
            #    print(text)
                await channel.send(str(newcard))

                text.name="Daikon 02"
                await CustomRetrievalClass().updateCustomByID(text, bot)
