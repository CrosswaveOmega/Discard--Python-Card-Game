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
from .classes.discordhelper.tiebreaker import make_tiebreaker, card_multimatch
from .classes.discordhelper.pagesystem import *
from .classes.discordhelper.universal_functions import *
from .classes.Cards.custom import CustomRetrievalClass
from .classes.imagemakingfunctions.imaging import *
from .classes.userservices.userprofile import SingleUserProfile
from .classes.Cards.DeckBuilding import *
from .classes.DiscordPlayerInputOutputSystem import *
#from .classes.main import *
from .classes.main.piece import *
from .classes.main.player import *
from .classes.main.GridClass import Grid

from .Discard import *


#from discord.ext.tasks import loop


    #<a:stopwatch:774741008495542284>
    #<a:stopwatch_15:774741008793337856>

class CardCogBattle(commands.Cog):
    """Commands for battle system goes here."""
    @commands.command()
    async def start_duel (self, ctx, *args): #Start a duel
        '''
        syntax: start_duel
        This function is for starting a CardDuel.


        '''
        bot=ctx.bot
        author=ctx.message.author;
        channel=ctx.message.channel;
        #Get Users involved.
        print("Get users.  For now, we only need to use the one who called this command.")
        #Get Decks to be used.
        print("Get deck of each player.")
        player1Deck=[]
        #create DPIOS object
        player1_DPIOS=DPIOS(channel, author)

        #make DiscordPlayer class
        player1 = DiscordPlayer(deck=player1Deck, team=1, dpios=player1_DPIOS)
        #Make Card_Duel class
        thisDuel=Card_Duel(bot)
        thisDuel.addPlayer(player1)
        #Start Card_Duel

    @commands.command()
    async def start_test_duel (self, ctx, *args): #Start a duel
        '''
        syntax: start_test_duel
        This function is for starting a CardDuel, and TESTING it.

        Modify however you wish.


        '''
        bot=ctx.bot
        author=ctx.message.author;
        channel=ctx.message.channel;
        #Get Users involved.
        SingleUser = SingleUserProfile("arg")
        profile1 = SingleUser.getByID(author.id)
        print("Get users.  For now, we only need to use the one who called this command.")
        #Get Decks to be used.
        print("Get deck of each player.")
        player1Deck=[]
        player1Deck_RAW=profile1.get_decks()[0]
        for deck_card in player1Deck_RAW.get_deck_cards():
            newcard=await inventory_entry_to_card_object(bot, deck_card)
            player1Deck.append(newcard)

        #create DPIOS object
        player1_DPIOS=DPIOS(channel, author, bot)
        #make DiscordPlayer class
        player1 = DiscordPlayer(deck=player1Deck, team=1, dpios=player1_DPIOS)
        #Make Card_Duel class
        thisDuel=Card_Duel(bot)
        thisDuel.addPlayer(player1)
        #Start Card_Duel
        testPiece=Leader(player1, "MY_NAME", position_notation="B2")
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
