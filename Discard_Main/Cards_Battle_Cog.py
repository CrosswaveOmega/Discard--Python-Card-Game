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
from .classes.discordhelper.tiebreaker import make_tiebreaker, card_multimatch
from .classes.discordhelper.pagesystem import *
from .classes.Cards.custom import CustomRetrievalClass
from .classes.imagemakingfunctions.imaging import *
from .classes.userservices.userprofile import SingleUserProfile
from .classes.Cards.DeckBuilding import *
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
        auth=ctx.message.author;
        channel=ctx.message.channel;
        #Get Users involved.
        print("Get users.  For now, we only need to use the one who called this command.")
        #Get Decks to be used.
        print("Get deck of each player.")

        #make DiscordPlayer class

        #Make Card_Duel class

        #Start Card_Duel
