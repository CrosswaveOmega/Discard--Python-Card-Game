import discord
import operator
import io
import json
import aiohttp
import asyncio
import csv
import datetime

from discord.ext import commands, tasks
from discord.utils import find
from discord import Webhook, AsyncWebhookAdapter

class DPIOS:
    #Fil in later.
    def __init__(self, textchannel, user):
        self.textchannel=textchannel #Text channel to send input to.
        self.user=user
        print("tbd")
