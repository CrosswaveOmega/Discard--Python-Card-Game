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

#Make debug commands here

class DebugCog(commands.Cog):
    """Commands for testing the system goes here."""
    @commands.command()
    async def add_exp(self, ctx, *args): #A example command.
        '''
        syntax: add_exp
        Add 10 exp to the user who invokes this command.

        '''
        bot=ctx.bot #The refrence to the bot object. https://discordpy.readthedocs.io/en/latest/ext/commands/api.htm?highlight=bot#bot
        author=ctx.message.author;  #The refrence to the message author.  https://discordpy.readthedocs.io/en/latest/api.html?highlight=user#user
        channel=ctx.message.channel; #the refrence to the channel this message was sent in.  https://discordpy.readthedocs.io/en/latest/api.html?highlight=textchannel#textchannel
        SingleUser=SingleUserProfile("arg") #Singleton Object that gets a user based on their id.
        
        user_id=author.id
        profile=SingleUser.getByID(user_id)
        await channel.send("Old EXP="+str(profile.get_exp()))
        profile.set_exp(profile.get_exp()+10)
        profile=SingleUser.getByID(user_id)
        await channel.send("New EXP="+str(profile.get_exp()))
        SingleUser.save_all()
        #await channel.send(str(newcard))
