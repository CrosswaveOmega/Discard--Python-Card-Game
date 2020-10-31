import discord
import operator
import io
import json
import aiohttp
import asyncio
import csv
from configparser import ConfigParser #For Config, which is used here.
import datetime
from PIL import Image, ImageTk, ImageGrab, ImageDraw, ImageFont

from discord.ext import commands, tasks
from discord.utils import find
from discord import Webhook, AsyncWebhookAdapter
from .classes.Cards.cardretrieval import CardRetrievalClass
from .classes.discordhelper.tiebreaker import make_tiebreaker
from .classes.Cards.custom import CustomRetrievalClass
from .classes.imagemakingfunctions.imaging import *
from .classes.userservices.userprofile import SingleUserProfile
#from discord.ext.tasks import loop


#Primary area with commands.
configur=ConfigParser()
configur.read('config.ini')

class CustomsCog(commands.Cog):

    @commands.command(pass_context=True)
    async def upload_image(self, ctx, *args): #A very rudimentary card retrieval system.
        '''
        syntax: upload_image CustomId
        [CustomId]: The CustomId you want to change the image of.

        This command must accompany a attached image file.

        '''
        bot=ctx.bot
        author=ctx.message.author;
        channel=ctx.message.channel;
        leng=len(args)
        attachLength=len(ctx.message.attachments)
        if (leng>=1 and attachLength==0):
            for attach in ctx.message.attachments:
                byte=await attach.read();
                fil=io.BytesIO(byte) #file in attachments.
                with io.BytesIO() as image_binary:
                    custom=await CustomRetrievalClass().getByID(args[0], bot)
                        channel.send("Error! {0} not found.".format(args[0])) #EXCEPTION: INVALID CIPHER ID WAS GIVEN.
                    make_card_image(fil).save(image_binary, 'PNG') #Returns pil object.
                    image_binary.seek(0)
                    checkGuild= bot.get_guild(int(configur.get("Default",'bts_server'))) #Behind The Scenes server
                    custom_channel= checkGuild.get_channel(int(configur.get("Default",'bts_card_image_channel'))) #Customs Channel.
                    image_msg=await custom_channel.send(file=discord.File(fp=image_binary, filename='image.png'))

                    url="p"
                    for attach in image_msg.attachments:
                        url=attach.url
                        custom.change_display_image(url, image_msg.id)
                    await CustomRetrievalClass().updateCustomByID(custom, bot)

    @commands.command(pass_context=True)
    async def newCustom(self, ctx, *args): #A very rudimentary card retrieval system.
        '''
        syntax: createCustom

        '''
        bot=ctx.bot
        author=ctx.message.author;
        channel=ctx.message.channel;
        leng=len(args)
        SingleUser = SingleUserProfile("arg")

        user_id = .id
        profile = SingleUser.getByID(user_id)
        cipher=await CustomRetrievalClass().addCustom("TEXT", bot)
        await channel.send(content=cipher)
        profile.add_custom(cipher) #add cipher to userprofile
        SingleUser.save_all()
