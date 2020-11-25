import discord
import operator
import io
import json
import aiohttp
import asyncio
import csv
import datetime
import queue
from PIL import Image, ImageTk, ImageGrab, ImageDraw, ImageFont

from discord.ext import commands, tasks
from discord.utils import find
from discord import Webhook, AsyncWebhookAdapter
from .classes.Cards.cardretrieval import CardRetrievalClass
from .classes.discordhelper import *
from .classes.Cards.custom import CustomRetrievalClass
from .classes.imagemakingfunctions.imaging import *
from .classes.userservices.userprofile import SingleUserProfile
from .classes.userservices.useroperations import *

from .classes.Cards.DeckBuilding import *
from .classes.DiscordPlayerInputOutputSystem import *
#from .classes.main import *
from .classes.main.piece import *
from .classes.main.player import *
from .classes.main.GridClass import Grid

from .Discard import *


#from discord.ext.tasks import loop

# <a:stopwatch:774741008495542284>
# <a:stopwatch_15:774741008793337856>
async def get_everything(bot, author, channel, team=1):
    """Returns profile and player of the passed in info"""
    print("get profile of user.")
    SingleUser = SingleUserProfile("arg")
    id=author.id
    profile = SingleUser.getByID(id)
    playerDeck = []
    print("Right now, it only gets the first deck of the user.")
    playerDeck_RAW = profile.get_primary_deck()  # inventory entries.
    if playerDeck_RAW == None:
        return False, False
    for deck_card in playerDeck_RAW.get_deck_cards():
        newcard = await inventory_entry_to_card_object(bot, deck_card)
        playerDeck.append(newcard)
        print(newcard.get_image())
    player_DPIOS = DPIOS(channel, author, bot)
    await player_DPIOS.send_order()
    player = DiscordPlayer(deck=playerDeck, team=team, dpios=player_DPIOS)
    return profile, player
battles=1

class CardCogBattle(commands.Cog):
    """Commands for battle system goes here."""
    @commands.command()
    async def request_duel(self, ctx, *args):
        avgspeed=CardRetrievalClass().getMeanSpeed()
        """Start a duel with another person!"""
        bot = ctx.bot  # The refrence to the bot object. https://discordpy.readthedocs.io/en/latest/ext/commands/api.htm?highlight=bot#bot
            # The refrence to the message author.  https://discordpy.readthedocs.io/en/latest/api.html?highlight=user#user
        author = ctx.message.author
            # the refrence to the channel this message was sent in.  https://discordpy.readthedocs.io/en/latest/api.html?highlight=textchannel#textchannel
        channel = ctx.message.channel
        guild = channel.guild

        mentions=ctx.message.mentions

        avgspeed=CardRetrievalClass().getMeanSpeed()
        user1=author
        user2=None

        for mention in mentions:
            if author.id != mention.id:
                choices=[]
                choices.append(["no", "", '❌'])
                choices.append(["yes", "", '✔️'])
                message=await mention.send("{} has requested a duel with you.  Will you accept?".format(author.name))
                result = await make_dmtiebreaker(bot, mention, choices, message=message, timeout_enable=True, delete_after=True, timeout_time=60.0)
                #await ctx.channel.send(mention.name+" says "+result)
                if (result=="yes"):
                    user2=mention
                else:
                    await ctx.channel.send(mention.name+" has declined.")
                    return None
        if user2==None:
            await ctx.channel.send("No other user was mentioned.")
            return None
        battles=1
        rolea, room1 = await Create_Room_And_Role(user1, bot, guild, battles, 'a')
        roleb, room2 = await Create_Room_And_Role(user2, bot, guild, battles, 'b')

        battles=battles+1
        await room2.send("SAY SOMETHING HERE!")
        await room1.send("SAY SOMETHING HERE!")

        def check_message_1(m):
            return m.author != bot.user and m.channel == room1

        def check_message_2(m):
            return m.author != bot.user and m.channel == room2

        async def getMessageInChannel1():
            msg = await bot.wait_for('message', check=check_message_1)
            #print("Message ");
            return msg.author

        async def getMessageInChannel2():
            msg = await bot.wait_for('message', check=check_message_2)
            #print("Message ");
            return msg.author
        SingleUser = SingleUserProfile("arg")
        messagetask1 = asyncio.create_task(getMessageInChannel1())
        messagetask2 = asyncio.create_task(getMessageInChannel2())
        tasklist = [messagetask1, messagetask2]

        done, pending = await asyncio.wait(tasklist, return_when=asyncio.ALL_COMPLETED)
        if messagetask1 in done:
            room1.send("Reading you.")
        if messagetask2 in done:
            room2.send("Reading you.")

        profile1, player1 = await get_everything(bot, user1, room1, team=1)
        profile2, player2 = await get_everything(bot, user2, room2, team=2)

        profiles=[profile1, profile2]
        thisDuel = Card_Duel(bot)
        thisDuel.addPlayer(player1)
        thisDuel.addPlayer(player2)
        # Start Card_Duel
        testPiece = Leader(player1, player1.get_user_name(), position_notation="C1", speed=avgspeed)
        testPiece.set_image()

        testPiece2 = Leader(player2, player2.get_user_name(), position_notation="C5", speed=avgspeed)
        testPiece2.set_image()

        player1.set_leader(testPiece)
        player2.set_leader(testPiece2)

        thisDuel.add_piece(testPiece)
        thisDuel.add_piece(testPiece2)

        winner=await thisDuel.start_game()
        battles=battles-1
        await user1.remove_roles(rolea)
        await user2.remove_roles(rolea)
        if (winner!=None):
            if winner.get_user_name() == user1.name:
                await add_coin(profile1, 20)
                await incr_stars(channel, profile1)

            if winner.get_user_name() == user2.name:
                await add_coin(profile2, 20)
                await incr_stars(channel, profile2)

        for profile in profiles:
            await add_exp_point(profile, 20)
            await add_coin(profile)
            await incr_level(channel, profile)
            await incr_stars(channel, profile)
        SingleUser.save_all()







    # @commands.command()
    # async def start_duel(self, ctx, *args):  # Start a duel
    #     '''
    #     syntax: start_duel
    #     This function is for starting a CardDuel.
    #
    #
    #     '''
    #     bot = ctx.bot
    #     author = ctx.message.author
    #     channel = ctx.message.channel
    #     # Get Users involved.
    #     print("Get users.  For now, we only need to use the one who called this command.")
    #     # Get Decks to be used.
    #     print("Get deck of each player.")
    #     player1Deck = []
    #     # create DPIOS object
    #     player1_DPIOS = DPIOS(channel, author)
    #
    #     # make DiscordPlayer class
    #     player1 = DiscordPlayer(deck=player1Deck, team=1, dpios=player1_DPIOS)
    #     # Make Card_Duel class
    #     thisDuel = Card_Duel(bot)
    #     thisDuel.addPlayer(player1)
    #     # Start Card_Duel

    @commands.command()
    async def start_2_player_duel_test(self, ctx, *args):  # Start a duel
        '''
        syntax: start_test_duel
        This function is for starting a CardDuel, and TESTING it.

        Modify however you wish.


        '''
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel

        server = channel.guild
        SingleUser = SingleUserProfile("arg")
        room2 = server.get_channel(777998040283086900)
        room1 = server.get_channel(777997792558710804)

        await room2.send("SAY SOMETHING HERE!")
        await room1.send("SAY SOMETHING HERE!")
        user1 = None
        user2 = None

        def check_message_1(m):
            return m.author != bot.user and m.channel == room1

        def check_message_2(m):
            return m.author != bot.user and m.channel == room2

        async def getMessageInChannel1():
            msg = await bot.wait_for('message', check=check_message_1)
            #print("Message ");
            return msg.author

        async def getMessageInChannel2():
            msg = await bot.wait_for('message', check=check_message_2)
            #print("Message ");
            return msg.author

        messagetask1 = asyncio.create_task(getMessageInChannel1())
        messagetask2 = asyncio.create_task(getMessageInChannel2())
        tasklist = [messagetask1, messagetask2]

        await channel.send("Please have one user say something in room1, and have another user say something in room 2.")
        # there's probably a better way to do this.
        done, pending = await asyncio.wait(tasklist, return_when=asyncio.ALL_COMPLETED)
        if messagetask1 in done:
            user1 = messagetask1.result()
        if messagetask2 in done:
            user2 = messagetask2.result()
        print(user1.id, user2.id)
        profile1, player1 = await get_everything(bot, user1, room1, team=1)
        profile2, player2 = await get_everything(bot, user2, room2, team=2)

        thisDuel = Card_Duel(bot)
        thisDuel.addPlayer(player1)
        thisDuel.addPlayer(player2)
        # Start Card_Duel
        avgspeed=CardRetrievalClass().getMeanSpeed()
        testPiece = Leader(player1, player1.get_user_name(), position_notation="C1", speed=avgspeed)
        testPiece.set_image()

        testPiece2 = Leader(player2, player2.get_user_name(), position_notation="C5", speed=avgspeed)
        testPiece2.set_image()

        player1.set_leader(testPiece)
        player2.set_leader(testPiece2)

        thisDuel.add_piece(testPiece)
        thisDuel.add_piece(testPiece2)

        await thisDuel.start_game()

    @commands.command()
    async def AI_Test(self, ctx, *args):  # Start a duel
        """
        This is for a automated test.
        """
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel

    @commands.command()
    async def start_test_duel(self, ctx, *args):  # Start a duel
        '''
        syntax: start_test_duel
        This function is for starting a CardDuel, and TESTING it.

        Modify however you wish.


        '''
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        avgspeed=CardRetrievalClass().getMeanSpeed()
        # Get Users involved.
        SingleUser = SingleUserProfile("arg")
        profile1 = SingleUser.getByID(author.id)
        print("Get users.  For now, we only need to use the one who called this command.")
        # Get Decks to be used.
        print("Get deck of each player.")
        player1Deck = []
        player1Deck_RAW = profile1.get_decks()[0]
        for deck_card in player1Deck_RAW.get_deck_cards():
            newcard = await inventory_entry_to_card_object(bot, deck_card)
            player1Deck.append(newcard)

        # create DPIOS object
        player1_DPIOS = DPIOS(channel, author, bot)
        # This is so the messages are sent in the right order.
        await player1_DPIOS.send_order()
        # make DiscordPlayer class
        player1 = DiscordPlayer(deck=player1Deck, team=1, dpios=player1_DPIOS)
        # Make Card_Duel class
        thisDuel = Card_Duel(bot)
        thisDuel.addPlayer(player1)
        # Start Card_Duel
        testPiece = Leader(player1, "MY_NAME", position_notation="B2", speed=avgspeed)
        testPiece.set_image()

        player1.set_leader(testPiece)

        thisDuel.add_piece(testPiece)
        await thisDuel.update_grid_image()
        await thisDuel.start_game()

#        await thisDuel.update_grid_image()
#        testPiece.change_position("C2")
#        await asyncio.sleep(2)
#        await thisDuel.update_grid_image()
#        testPiece.change_position("C3")
#        await thisDuel.update_grid_image()
