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

    def get_avatar_url(self):
        return self.user.avatar_url
    async def send_pil_image(self, pil):
        with io.BytesIO() as image_binary:
            pil.save(image_binary, 'PNG') #Returns pil object.
            image_binary.seek(0)
            image_msg=await self.textchannel.send(file=discord.File(fp=image_binary, filename='image.png'))
