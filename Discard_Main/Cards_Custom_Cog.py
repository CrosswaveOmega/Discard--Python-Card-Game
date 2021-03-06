import discord
import operator
import io
import json
import aiohttp
import asyncio
import csv
from configparser import ConfigParser  # For Config, which is used here.
import datetime
from PIL import Image, ImageTk, ImageGrab, ImageDraw, ImageFont

from discord.ext import commands, tasks
from discord.utils import find
from discord import Webhook, AsyncWebhookAdapter
from .classes.Cards.cardretrieval import CardRetrievalClass
#from .classes.discordhelper.tiebreaker import *
from .classes.discordhelper import *
from .classes.Cards.custom import CustomRetrievalClass, CustomBase
from .classes.imagemakingfunctions.imaging import *
from .classes.userservices.userprofile import SingleUserProfile

# from discord.ext.tasks import loop


# Primary area with commands.
configur = ConfigParser()
configur.read('config.ini')

async def upload_new_image(bot, author, channel, attach, custom_id):
    """Upload a new image to the bts_card_image_channel given an attachment object.  Sets a new image."""
    byte = await attach.read()
    fil = io.BytesIO(byte)  # file in attachments.
    with io.BytesIO() as image_binary:
        custom = await CustomRetrievalClass().getByID(custom_id, bot)
        if custom == None:
            await channel.send("Error! {0} not found.".format(custom_id))
        print("Going for it.")
        # Returns pil object.
        make_card_image(fil).save(image_binary, 'PNG')
        image_binary.seek(0)
        # Behind The Scenes server
        checkGuild = bot.get_guild(int(configur.get("Default", 'bts_server')))
        custom_channel = checkGuild.get_channel(int(configur.get("Default", 'bts_card_image_channel')))  # Customs Channel.
        image_msg = await custom_channel.send(file=discord.File(fp=image_binary, filename='image.png'))

        url = "p"
        for attach in image_msg.attachments:
            url = attach.url
            print("url")
            custom.change_display_image(url, image_msg.id)
        await CustomRetrievalClass().updateCustomByID(custom, bot)
        await channel.send("Display Image of {0} updated without problems.".format(custom_id))

async def custom_id_from_match(ctx, profile, data_to_match):
    bot = ctx.bot
    author = ctx.message.author
    channel = ctx.message.channel
    custom_id = None
    type_of_match, matched_data = card_multimatch_with_type(profile, data_to_match)
    if (type_of_match == "custom_name" or type_of_match == "card_id"):
        print(type_of_match, matched_data)
        if(len(matched_data)>1):
            inventory_entry = await make_tiebreaker_with_inventory_entries(ctx, matched_data)
        elif(len(matched_data)==1):
            inventory_entry=matched_data[0]
        # matched Data is list.
        if (inventory_entry == "timeout"):
            channel.send("Timeout, terminating task.")
            return None
        if (inventory_entry == "exit"):
            return None
        else:
            if (inventory_entry["custom"] == None):
                # This card does not have a custom, so it makes one.
                await ctx.invoke(bot.get_command('newCustom'), "Temporary Name", inventory_entry["inv_key"])
                custom_id = profile.get_inventory_entry_by_key(
                    inventory_entry["inv_key"])["custom"]
            else:
                custom_id = profile.get_inventory_entry_by_key(
                    inventory_entry["inv_key"])["custom"]
    elif (type_of_match == "custom_id"):
        return matched_data
    return custom_id


async def inv_key_from_match(ctx, profile, data_to_match):
    "returns inventory key from a match"
    bot = ctx.bot
    author = ctx.message.author
    channel = ctx.message.channel
    inv_key = None
    type_of_match, matched_data = card_multimatch_with_type(
        profile, data_to_match, match_by_custom_id=False)
    if (type_of_match == "custom_name" or type_of_match == "card_id"):
        print(type_of_match, matched_data)
        inventory_entry = await make_tiebreaker_with_inventory_entries(ctx, matched_data)
        # matched Data is list.
        if (inventory_entry == "timeout"):
            channel.send("Timeout, terminating task.")
            return None
        if (inventory_entry == "exit"):
            return None
        else:
            inv_key = inventory_entry["inv_key"]
    return inv_key


class CustomsCog(commands.Cog):
    """For creating custom cards."""
    @commands.command(pass_context=True)
    async def newCustom(self, ctx, *args):
        '''
        syntax: createCustom "New Name" [key_id]
        Creates a new custom,
        '''
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        leng = len(args)
        set_name = "blank_custom"
        key_id = None
        if (leng >= 1):
            set_name = args[0]
        if (leng >= 2):
            key_id = args[1]
        SingleUser = SingleUserProfile("arg")

        user_id = author.id
        profile = SingleUser.getByID(user_id)
        cipher = await CustomRetrievalClass().addCustom(set_name, bot)
        await channel.send(content=cipher)
        profile.add_custom(cipher)  # add cipher to userprofile
        if key_id != None:  # key_id is optional.
            await ctx.invoke(bot.get_command('ApplyCustomWithInvKey'), key_id, cipher)

        SingleUser.save_all()

    @commands.command(pass_context=True)
    async def changeDisplayName(self, ctx, *args):
        '''
        syntax: changeDisplayName [card identifier] [new name]
        Changes the name of a card in your inventory or a custom you have created.
        [card_identifier] - can be custom_id, card_id, custom_name, or card_name
        [new name] - the new name of the card
        '''
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        leng = len(args)
        data_to_match = None
        new_name = None
        if (leng >= 1):
            data_to_match = args[0]
        if (leng >= 2):
            new_name = args[1]
        if (data_to_match != None and new_name != None):
            SingleUser = SingleUserProfile("arg")
            user_id = author.id
            profile = SingleUser.getByID(user_id)
            # check if ]
            custom_id = await custom_id_from_match(ctx, profile, data_to_match)
            if (custom_id != None):
                custom = await CustomRetrievalClass().getByID(custom_id, bot)
                custom.name = new_name
                SingleUser.save_all()
                await CustomRetrievalClass().updateCustomByID(custom, bot)
                await channel.send("Name Updated.")
            else:
                await channel.send("Custom Id Not found.")

    @commands.command(pass_context=True)
    async def changeDisplayIcon(self, ctx, *args):
        '''
        syntax: changeDisplayIcon  [card identifier] [new icon (must be emoji)]
        Changes the icon of a card in your inventory or a custom you have created.
        [card_identifier] - can be custom_id, card_id, custom_name, or card_name
        [new icon] - the new icon of the card.  Must be a emoji.
        '''
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        leng = len(args)
        data_to_match = None
        new_icon = None
        if (leng >= 1):
            data_to_match = args[0]
        if (leng >= 2):
            new_icon = args[1]
        if (data_to_match != None and new_icon != None):
            SingleUser = SingleUserProfile("arg")
            user_id = author.id
            profile = SingleUser.getByID(user_id)
            custom_id = await custom_id_from_match(ctx, profile, data_to_match)
            if (custom_id == None):
                channel.send("Custom Id Not Found.")
                return
            custom = await CustomRetrievalClass().getByID(custom_id, bot)
            custom.icon = new_icon
            SingleUser.save_all()
            await CustomRetrievalClass().updateCustomByID(custom, bot)
            await channel.send("Name Updated.")

    @commands.command(pass_context=True)
    # A very rudimentary card retrieval system.
    async def changeDisplayImage(self, ctx, *args):
        '''
        syntax: changeDisplayImage CustomId
        [CustomId]: The CustomId you want to change the image of.

        This command must accompany a attached image file.

        '''
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        leng = len(args)
        attachLength = len(ctx.message.attachments)
        print(attachLength)
        if (leng >= 1 and attachLength > 0):
            for attach in ctx.message.attachments:
                await upload_new_image(bot, author, channel, attach, args[0])

    @commands.command(pass_context=True, hidden=True)
    async def changeDisplayAll_internal(self, ctx, data_to_match, new_name, new_icon=None, attach=None):
        "This is a internal version of change display all."
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        SingleUser = SingleUserProfile("arg")
        user_id = author.id
        profile = SingleUser.getByID(user_id)
        custom_id = await custom_id_from_match(ctx, profile, data_to_match)
        if (custom_id == None):
            await channel.send("Custom Id Not Found.")
            return
        custom = await CustomRetrievalClass().getByID(custom_id, bot)
        custom.name = new_name
        if new_icon != None:
            custom.icon = new_icon
        SingleUser.save_all()
        await CustomRetrievalClass().updateCustomByID(custom, bot)
        if attach != None:
            await upload_new_image(bot, author, channel, attach, custom_id)
        await channel.send("Name Updated.")

    @commands.command(pass_context=True)
    async def changeDisplayAll(self, ctx, *args):
        '''
        syntax: changeDisplayAll  [card identifier] [new icon (must be emoji)]
        Creates a new custom object for the card you've selected
        [card_identifier] - can be custom_id, card_id, custom_name, or card_name
        [new name] - the new name of the card
        [new icon] - the new icon of the card.  Must be a emoji.

        This command can accompany an attached image.
        '''
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        leng = len(args)
        data_to_match = None
        new_name = None
        new_icon = None
        if (leng >= 1):
            data_to_match = args[0]
        if (leng >= 2):
            new_name = args[1]
        if (leng >= 3):
            new_icon = args[2]
        if (data_to_match != None and new_name != None):
            this_attach=None
            for attach in ctx.message.attachments:
                print("Attatchment Found")
                this_attach=attach
            await self.changeDisplayAll_internal(ctx, data_to_match, new_name, new_icon, this_attach)
                # await upload_new_image(bot, author, channel, attach, custom_id)


            # SingleUser = SingleUserProfile("arg")
            # user_id = author.id
            # profile = SingleUser.getByID(user_id)
            # custom_id = await custom_id_from_match(ctx, profile, data_to_match)
            # if (custom_id == None):
            #     await channel.send("Custom Id Not Found.")
            #     return
            # custom = await CustomRetrievalClass().getByID(custom_id, bot)
            # custom.name = new_name
            # if new_icon != None:
            #     custom.icon = new_icon
            # SingleUser.save_all()
            # await CustomRetrievalClass().updateCustomByID(custom, bot)
            # for attach in ctx.message.attachments:
            #     await upload_new_image(bot, author, channel, attach, custom_id)
            # await channel.send("Name Updated.")
        else:
            emb=changeDisplayAllHelp()
            await channel.send(embed=emb)
            #help_message

    @commands.command(pass_context=True)
    # A very rudimentary card retrieval system.
    async def applyCustom(self, ctx, *args):
        '''
        syntax: applyCustom "[inventory_identifier]" "custom_id"
        Applies a customization to a card in your inventory.
        '''
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        leng = len(args)
        data_to_match = None
        custom = None
        if (leng >= 1):
            data_to_match = args[0]
        if (leng >= 2):
            custom = args[1]
        if (data_to_match != None and custom != None):
            SingleUser = SingleUserProfile("arg")

            user_id = author.id
            profile = SingleUser.getByID(user_id)
            key = await inv_key_from_match(ctx, profile, data_to_match)
            if (key != None):
                # invokes the OTHER command
                await ctx.invoke(bot.get_command('ApplyCustomWithInvKey'), key, custom)
                profile.apply_custom(key, custom)
                # cipher=await CustomRetrievalClass().addCustom(set_name, bot)
                # await channel.send(content=cipher)
                # profile.add_custom(cipher) #add cipher to userprofile
                SingleUser.save_all()
                await channel.send("Applied Customization successfully updated.")
            else:
                await channel.send("Key Not found.")

            await channel.send("updated")
        else:
            await channel.send("INVALID KEY OR CUSTOMID.")

    @commands.command(pass_context=True)
    # A very rudimentary card retrieval system.
    async def ApplyCustomWithInvKey(self, ctx, *args):
        '''
        syntax: ApplyCustomWithInvKey "inv_key" "custom_id"
        Applies a customization to a card in your inventory via the inventory key.
        '''
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        leng = len(args)
        key = None
        custom = None
        if (leng >= 1):
            key = args[0]
        if (leng >= 2):
            custom = args[1]
        if (key != None and custom != None):
            SingleUser = SingleUserProfile("arg")

            user_id = author.id
            profile = SingleUser.getByID(user_id)

            profile.apply_custom(key, custom)
            # cipher=await CustomRetrievalClass().addCustom(set_name, bot)
            # await channel.send(content=cipher)
            # profile.add_custom(cipher) #add cipher to userprofile
            SingleUser.save_all()
            await channel.send("updated")
        else:
            await channel.send("INVALID KEY OR CUSTOMID.")

    @commands.command(pass_context=True)
    async def copyCustom(self, ctx, *args):
        '''
        syntax: copyCustom "custom_id"
        Makes a copy of the custom.
        '''
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        leng = len(args)
        custom = None
        if (leng >= 1):
            custom = args[0]
        if (custom != None):
            SingleUser = SingleUserProfile("arg")
            user_id = author.id
            profile = SingleUser.getByID(user_id)
            custom = await CustomRetrievalClass().getByID(args[0], bot)
            if (custom != None):
                cipher = await CustomRetrievalClass().cloneCustom(custom, bot)
                await channel.send(content=cipher)
                profile.add_custom(cipher)  # add cipher to userprofile
                SingleUser.save_all()
                await channel.send("clone has been successful")
            else:
                await channel.send("invalid custom id.")
        else:
            await channel.send("INVALID KEY OR CUSTOMID.")

    @commands.command(pass_context=True)
    # A very rudimentary card retrieval system.
    async def deleteCustom(self, ctx, *args):
        '''
        syntax: deleteCustom "custom_id"
        deletes a custom
        '''
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        await channel.send("Delete custom comming soon.")
        print("TO BE DONE.")
