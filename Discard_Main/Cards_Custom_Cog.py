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
from .classes.Cards.custom import CustomRetrievalClass, CustomBase
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
        print(attachLength)
        if (leng>=1 and attachLength>0):
            for attach in ctx.message.attachments:
                byte=await attach.read();
                fil=io.BytesIO(byte) #file in attachments.
                with io.BytesIO() as image_binary:
                    custom=await CustomRetrievalClass().getByID(args[0], bot)
                    await channel.send("Error! {0} not found.".format(args[0])) #EXCEPTION: INVALID CIPHER ID WAS GIVEN.+
                    print("Going for it.")
                    make_card_image(fil).save(image_binary, 'PNG') #Returns pil object.
                    image_binary.seek(0)
                    checkGuild= bot.get_guild(int(configur.get("Default",'bts_server'))) #Behind The Scenes server
                    custom_channel= checkGuild.get_channel(int(configur.get("Default",'bts_card_image_channel'))) #Customs Channel.
                    image_msg=await custom_channel.send(file=discord.File(fp=image_binary, filename='image.png'))

                    url="p"
                    for attach in image_msg.attachments:
                        url=attach.url
                        print("url")
                        custom.change_display_image(url, image_msg.id)
                    await CustomRetrievalClass().updateCustomByID(custom, bot)

    @commands.command(pass_context=True)
    async def newCustom(self, ctx, *args): #A very rudimentary card retrieval system.
        '''
        syntax: createCustom "New Name"

        '''
        bot=ctx.bot
        author=ctx.message.author;
        channel=ctx.message.channel;
        leng=len(args)
        set_name="blank_custom"
        if(leng>=1):
            set_name=args[0]
        SingleUser = SingleUserProfile("arg")

        user_id = author.id
        profile = SingleUser.getByID(user_id)
        cipher=await CustomRetrievalClass().addCustom(set_name, bot)
        await channel.send(content=cipher)
        profile.add_custom(cipher) #add cipher to userprofile
        SingleUser.save_all()
    @commands.command(pass_context=True)
    async def changeDisplayName(self, ctx, *args):
        '''
        syntax: changeDisplayName cipher_id "New Name"

        '''
        bot=ctx.bot
        author=ctx.message.author;
        channel=ctx.message.channel;
        leng=len(args)
        custom_id=None
        new_name=None
        if(leng>=1):
            custom_id=args[0]
        if(leng>=2):
            new_name=args[1]
        if(custom_id!=None and new_name!=None):
            SingleUser = SingleUserProfile("arg")
            user_id = author.id
            profile = SingleUser.getByID(user_id)

            custom=await CustomRetrievalClass().getByID(custom_id, bot)

            custom.name=new_name
            SingleUser.save_all()
            await CustomRetrievalClass().updateCustomByID(custom, bot)
            await channel.send("Name Updated.")
    @commands.command(pass_context=True)
    async def changeDisplayIcon(self, ctx, *args):
        '''
        syntax: changeDisplayIcon cipher_id "New Icon(EMOJI)"

        '''
        bot=ctx.bot
        author=ctx.message.author;
        channel=ctx.message.channel;
        leng=len(args)
        custom_id=None
        new_icon=None
        if(leng>=1):
            custom_id=args[0]
        if(leng>=2):
            new_icon=args[1]
        if(custom_id!=None and new_icon!=None):
            SingleUser = SingleUserProfile("arg")
            user_id = author.id
            profile = SingleUser.getByID(user_id)
            custom=await CustomRetrievalClass().getByID(custom_id, bot)
            custom.icon=new_icon
            SingleUser.save_all()
            await CustomRetrievalClass().updateCustomByID(custom, bot)
            await channel.send("Name Updated.")
    @commands.command(pass_context=True)
    async def ApplyCustom(self, ctx, *args): #A very rudimentary card retrieval system.
        '''
        syntax: ApplyCustom "inv_key" "custom"

        '''
        bot=ctx.bot
        author=ctx.message.author;
        channel=ctx.message.channel;
        leng=len(args)
        key=None
        custom=None
        if(leng>=1):
            key=args[0]
        if(leng>=2):
            custom=args[1]
        if (key!=None and custom !=None):
            SingleUser = SingleUserProfile("arg")

            user_id = author.id
            profile = SingleUser.getByID(user_id)
            profile.apply_custom(key, custom)
            #cipher=await CustomRetrievalClass().addCustom(set_name, bot)
            #await channel.send(content=cipher)
            #profile.add_custom(cipher) #add cipher to userprofile
            SingleUser.save_all()
            await channel.send("updated")
        else:
            await channel.send("INVALID KEY OR CUSTOMID.")
