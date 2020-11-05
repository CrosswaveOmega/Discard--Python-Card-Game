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
from .classes.discordhelper.tiebreaker import *
from .classes.Cards.custom import CustomRetrievalClass, CustomBase
from .classes.imagemakingfunctions.imaging import *
from .classes.userservices.userprofile import SingleUserProfile
#from discord.ext.tasks import loop


#Primary area with commands.
configur=ConfigParser()
configur.read('config.ini')

async def custom_id_from_match(ctx, profile, data_to_match):
    bot=ctx.bot
    author=ctx.message.author;
    channel=ctx.message.channel;
    custom_id=None
    type_of_match, matched_data=card_multimatch_with_type(profile, data_to_match)
    if(type_of_match=="custom_name" or type_of_match=="card_id"):
        print(type_of_match, matched_data)
        inventory_entry=await make_tiebreaker_with_inventory_entries(ctx, matched_data)
        #matched Data is list.
        if(inventory_entry=="timeout"):
            channel.send("Timeout, terminating task.")
            return None
        if(inventory_entry=="exit"):
            return None
        else:
            if(inventory_entry["custom"]==None):
                await ctx.invoke(bot.get_command('newCustom'), "Temporary Name", inventory_entry["inv_key"]) #Makes new custom, and applys it to the key_id
                custom_id=profile.get_inventory_entry_by_key(inventory_entry["inv_key"])["custom"]
            else:
                custom_id=profile.get_inventory_entry_by_key(inventory_entry["inv_key"])["custom"]
    elif(type_of_match=="custom_id"):
        return matched_data
    return custom_id
class CustomsCog(commands.Cog):

    @commands.command(pass_context=True)
    async def changeDisplayImage(self, ctx, *args): #A very rudimentary card retrieval system.
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
                    if custom==None:
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
        Creates a new custom,
        '''
        bot=ctx.bot
        author=ctx.message.author;
        channel=ctx.message.channel;
        leng=len(args)
        set_name="blank_custom"
        key_id=None
        if(leng>=1):
            set_name=args[0]
        if(leng>=2):
            key_id=args[1]
        SingleUser = SingleUserProfile("arg")

        user_id = author.id
        profile = SingleUser.getByID(user_id)
        cipher=await CustomRetrievalClass().addCustom(set_name, bot)
        await channel.send(content=cipher)
        profile.add_custom(cipher) #add cipher to userprofile
        if key_id!=None: #key_id is optional.
            await ctx.invoke(bot.get_command('ApplyCustom'), key_id, cipher)

        SingleUser.save_all()

    @commands.command(pass_context=True)
    async def changeDisplayName(self, ctx, *args):
        '''
        syntax: changeDisplayName [card identifier] [new name]
        Changes the name of a card in your inventory or a custom you have created.
        [card_identifier] - can be custom_id, card_id, custom_name, or card_name
        [new name] - the new name of the card
        '''
        bot=ctx.bot
        author=ctx.message.author;
        channel=ctx.message.channel;
        leng=len(args)
        data_to_match=None
        new_name=None
        if(leng>=1):
            data_to_match=args[0]
        if(leng>=2):
            new_name=args[1]
        if(data_to_match!=None and new_name!=None):
            SingleUser = SingleUserProfile("arg")
            user_id = author.id
            profile = SingleUser.getByID(user_id)
            #check if ]
            custom_id=await custom_id_from_match(ctx, profile, data_to_match)
            if(custom_id!=None):
                custom=await CustomRetrievalClass().getByID(custom_id, bot)
                custom.name=new_name
                SingleUser.save_all()
                await CustomRetrievalClass().updateCustomByID(custom, bot)
                await channel.send("Name Updated.")
            else:
                await channel.send("Custom Id Not found.")
    @commands.command(pass_context=True)
    async def changeDisplayIcon(self, ctx, *args):
        '''
        syntax: changeDisplayIcon cipher_id "New Icon(EMOJI)"

        '''
        bot=ctx.bot
        author=ctx.message.author;
        channel=ctx.message.channel;
        leng=len(args)
        data_to_match=None
        new_icon=None
        if(leng>=1):
            data_to_match=args[0]
        if(leng>=2):
            new_icon=args[1]
        if(data_to_match!=None and new_icon!=None):
            SingleUser = SingleUserProfile("arg")
            user_id = author.id
            profile = SingleUser.getByID(user_id)
            custom_id=await custom_id_from_match(ctx, profile, data_to_match)
            if(custom_id==None):
                channel.send("Custom Id Not Found.")
                return 
            custom=await CustomRetrievalClass().getByID(custom_id, bot)
            custom.icon=new_icon
            SingleUser.save_all()
            await CustomRetrievalClass().updateCustomByID(custom, bot)
            await channel.send("Name Updated.")
    @commands.command(pass_context=True)
    async def ApplyCustom(self, ctx, *args): #A very rudimentary card retrieval system.
        '''
        syntax: ApplyCustom "inv_key" "custom_id"
        Applies a customization to a card in your inventory.
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
