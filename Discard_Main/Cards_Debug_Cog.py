import discord
import operator
import io
import json
import aiohttp
import asyncio
import csv
import random

from PIL import Image, ImageTk, ImageGrab, ImageDraw, ImageFont

from discord.ext import commands, tasks
from discord.utils import find
from discord import Webhook, AsyncWebhookAdapter
from .classes.Cards.cardretrieval import CardRetrievalClass
from .classes.discordhelper import *

from .classes.Cards.custom import CustomRetrievalClass
from .classes.imagemakingfunctions.imaging import *
from .classes.userservices.userprofile import SingleUserProfile


# from discord.ext.tasks import loop

# Make debug commands here

class DebugCog(commands.Cog):
    """Commands for testing the system goes here."""

    @commands.command()
    async def resync_names(self, ctx, *args):  # A example command.
        """Command to fix names."""
        await CustomRetrievalClass().resync_names(ctx.bot)
        await ctx.channel.send("Sync Completed")

    @commands.command(hidden=True)
    async def GetPing(self, ctx, *args):  # A example command.
        bot = ctx.bot  # The refrence to the bot object. https://discordpy.readthedocs.io/en/latest/ext/commands/api.htm?highlight=bot#bot
        # The refrence to the message author.  https://discordpy.readthedocs.io/en/latest/api.html?highlight=user#user
        author = ctx.message.author
        # the refrence to the channel this message was sent in.  https://discordpy.readthedocs.io/en/latest/api.html?highlight=textchannel#textchannel
        channel = ctx.message.channel

        mentions = ctx.message.mentions
        for mention in mentions:
            userid=mention.id
            await ctx.channel.send("id is "+str(userid))
            choices=[]
            choices.append(["no", "", '❌'])
            choices.append(["yes", "", '✔️'])
            message=await mention.send("Would you like do DUEL?!")
            result = await make_dmtiebreaker(bot, mention, choices, message=message, timeout_enable=True, delete_after=True, timeout_time=60.0)
            await ctx.channel.send(mention.name+" says "+result)

    @commands.command(hidden=True)
    async def Create_Room_And_Role(self, ctx, *args):  # A example command.
        bot = ctx.bot  # The refrence to the bot object. https://discordpy.readthedocs.io/en/latest/ext/commands/api.htm?highlight=bot#bot
        # The refrence to the message author.  https://discordpy.readthedocs.io/en/latest/api.html?highlight=user#user
        author = ctx.message.author
        # the refrence to the channel this message was sent in.  https://discordpy.readthedocs.io/en/latest/api.html?highlight=textchannel#textchannel
        channel = ctx.message.channel
        guild = channel.guild

        number=1
        battle_role_name="battle role "+ str(number)
        channel_name="room "+str(number)
        roles = guild.roles
        role=None
        for r in roles:
            if r.name==battle_role_name:
                role=r
        if (role!=None):
            role=await guild.create_role(name=battle_role_name, hoist=True, reason="For Battle")

        overwrites={
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True),
        role: discord.PermissionOverwrite(read_messages=True)
        }

        newchannel= await guild.create_text_channel(name=channel_name, overwrites=overwrites, position=0)
        await author.add_roles(role)

        await author.remove_roles(role)

    @commands.command(pass_context=True, hidden=True)
    async def make_space_emojis(self, ctx, *args):
        bot = ctx.bot
        auth = ctx.message.author
        channel = ctx.message.channel
        guild = channel.guild
        leng = len(args)
        number = None
        letters=["A","B","C","D","E","F","G"]
        numbers= ["1","2","3","4","5","6","7"]
        for l in letters:
            for n in numbers:
                number="{}{}".format(l,n)
                if (number != None):
                    with io.BytesIO() as image_binary:
                        # Returns pil object.
                        make_space_emoji(number).save(image_binary, 'PNG')
                        image_binary.seek(0)
                        await channel.send(file=discord.File(fp=image_binary, filename='image.png'))
                        image_binary.seek(0)
                        byte=image_binary.read()
                        print(byte)
                        await guild.create_custom_emoji(name=number, image=byte)

    @commands.command()
    async def getemojis(self, ctx):  # A example command.
        """Command to ensure user data is saved."""
        bot=ctx.bot
        channel=ctx.message.channel
     #   print(str(val))
        emoji=await ctx.message.guild.fetch_emojis()
        diction={}
        for emoj in emoji:
            print(str(emoj))
            diction[emoj.name]=str(emoj)
        dump=json.dumps(diction)
        print(dump)

    @commands.command()
    async def save(self, ctx):  # A example command.
        """Command to ensure user data is saved."""
        editmess = await ctx.channel.send("Saving All Data...")
        SingleUser = SingleUserProfile("arg")
        SingleUser.save_all()
        await editmess.edit(content="Saving All Data...\n ...Save Completed")

    @commands.command()
    async def add_exp(self, ctx):  # A example command.
        '''
        syntax: add_exp
        Add 10 exp to the user who invokes this command.

        '''
        bot = ctx.bot  # The refrence to the bot object. https://discordpy.readthedocs.io/en/latest/ext/commands/api.htm?highlight=bot#bot
        # The refrence to the message author.  https://discordpy.readthedocs.io/en/latest/api.html?highlight=user#user
        author = ctx.message.author
        # the refrence to the channel this message was sent in.  https://discordpy.readthedocs.io/en/latest/api.html?highlight=textchannel#textchannel
        channel = ctx.message.channel
        # Singleton Object that gets a user based on their id.
        SingleUser = SingleUserProfile("arg")

        user_id = author.id
        profile = SingleUser.getByID(user_id)
        await channel.send("Old EXP=" + str(profile.get_exp()))
        profile.set_exp(profile.get_exp() + 10)
        profile = SingleUser.getByID(user_id)
        await channel.send("New EXP=" + str(profile.get_exp()))
        SingleUser.save_all()
        # await channel.send(str(newcard))

    @commands.command()
    async def add_coins(self, ctx, *args):
        # increase the coins in user's account by the amount passed in the argument
        # if no argument is passed, then increase the coins by 4
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        SingleUser = SingleUserProfile("arg")

        user_id = author.id
        profile = SingleUser.getByID(user_id)
        if (len(args) > 1):
            await channel.send("Please enter either the command only or the command with 1 other integer only.")
        else:
            if (len(args) == 0):
                profile.set_coins(profile.get_coins() + 4)
                await channel.send("4 coins have been added to your account.\nCoins = " + str(profile.get_coins()))
            else:
                if (args[0].isdigit() == True):
                    profile.set_coins(profile.get_coins() + int(args[0]))
                    await channel.send(
                        "{} coins have been added to your account.\nCoins = ".format(int(args[0], profile.get_coins())))
                else:
                    await channel.send("Invalid input.")
        SingleUser.save_all()

    @commands.command()
    async def increase_stars(self, ctx):
        # increase the amount of the user's stars by 1 if their coins are greater than or equal to 20
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        SingleUser = SingleUserProfile("arg")

        user_id = author.id
        profile = SingleUser.getByID(user_id)
        if (profile.get_coins() >= 20):
            await channel.send("Old Stars = " + str(profile.get_stars()))
            await channel.send("Old Coins = " + str(profile.get_coins()))
            profile.set_stars(profile.get_stars() + 1)
            profile.set_coins(profile.get_coins() - 20)
            await channel.send("New Stars = " + str(profile.get_stars()))
            await channel.send("New Coins = " + str(profile.get_coins()))
        SingleUser.save_all()

    @commands.command()
    async def increase_level(self, ctx):
        # increase the user's level by 1 if their exp is greater than or equal to 100
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        SingleUser = SingleUserProfile("arg")

        user_id = author.id
        profile = SingleUser.getByID(user_id)
        if (profile.get_exp() >= 100):
            await channel.send("Old Level = " + str(profile.get_level()))
            await channel.send("Old EXP = " + str(profile.get_exp()))
            profile.set_level(profile.get_level() + 1)
            profile.set_exp(profile.get_exp() - 100)
            await channel.send("New Level = " + str(profile.get_level()))
            await channel.send("New EXP = " + str(profile.get_exp()))
        SingleUser.save_all()

    @commands.command()
    async def add_card(self, ctx, args):
        '''
        syntax: add_card [card_id]
        '''
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        SingleUser = SingleUserProfile("arg")

        user_id = author.id
        profile = SingleUser.getByID(user_id)
        card_id = args
        card=CardRetrievalClass().getByID(int(card_id, 16))
        if (card == False):
            await channel.send("Card does not exist")
        else:
            profile.add_card(card.get_ID()) #Add as string.
            await channel.send("Card added without issue.")
        SingleUser.save_all()

    @commands.command()
    async def add_card_wizard(self, ctx):
        '''
        Same as add card, but requires no arguments.
        '''
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        SingleUser = SingleUserProfile("arg")

        user_id = author.id
        profile = SingleUser.getByID(user_id)
        call=CallandResponse()
        call.add_field("card_id", "Enter the card id of the card you wish to add.", False)
        comp, res=await call.field_loop(ctx)
        if comp:
            if "card_id" in res:
                await ctx.invoke(bot.get_command('add_card'), res['card_id'])
        else:
            await ctx.channel.send("Loop terminated.")
    @commands.command(hidden=True)
    async def callandresponsetest(self, ctx):
        '''
        syntax: callandresponcetest
        for testing the call and responce system.
        '''
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        SingleUser = SingleUserProfile("arg")

        user_id = author.id
        profile = SingleUser.getByID(user_id)
        call=CallandResponce()
        call.add_field("Name 1", "Prompt", False)
        call.add_field("Beta 2", "Prompt", True)
        comp, to_reutn=await call.field_loop(ctx)
        if comp:
            for i, v in to_reutn.items():
                await channel.send("{}:{}".format(i,v))
        else:
            await ctx.channel.send("Loop terminated.")




        if (CardRetrievalClass().getByID(int(card_id, 16)) == False):
            await channel.send("Card does not exist")
        else:
            profile.add_card(card_id)
            await channel.send("Card added without issue.")
        SingleUser.save_all()

    @commands.command()
    async def addRandomCard(self, ctx):
        '''
        syntax: addRandomCard
        add a random card to your inventory that you don't already have.
        '''
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
            await channel.send("Card added.")
        SingleUser.save_all()
