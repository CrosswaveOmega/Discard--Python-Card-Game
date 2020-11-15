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

from ..discordhelper.tiebreaker import *

class DPIOS:
    #Fil in later.
    def __init__(self, textchannel, user, bot):
        self.textchannel=textchannel #Text channel to send input to.
        self.user=user
        self.bot=bot
        print("tbd")
        self.image_msg=None
        self.player_msg=None

    def get_avatar_url(self):
        """returns the avatar url of the user"""
        return self.user.avatar_url
    #INPUT
    async def get_user_choice(self, choice_list, prompt="Select a choice."):
        #get command from user.
        """select a choice from a list.  Same as Tiebreaker.
        choice_list is a single list of strings.  prompt is a possible promgt.
        """
        choices=[]
        numberlist=["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
        defchoice=["back","", '🔙']
        choices.append(defchoice)
        outputString=""
        for i in range(0,len(choice_list)):
            name=choice_list[i]
            emoji=numberlist[i]
            choices.append([choice_list[i], name, emoji])
            outputString=outputString + " {}[{}] ".format(emoji, name)
        message=await self.textchannel.send(content="{}\n{}".format(prompt, outputString))
        result=await make_internal_tiebreaker(self.bot, self.user, self.textchannel, choices, message=message, timeout_enable=True, remove_after=True, delete_after=True)
        return result
    async def get_user_command(self, actions, prompt="ENTER COMMAND:"):
        """get command from user.  Same as Tiebreaker.
        actions is a single list of strings.  Prompt is the prompt.
        """
        choices=[]
        numberlist=["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
        defchoice=["exit","", '🔚']
        choices.append(defchoice)
        outputString=""
        if(len(actions)==1):
            return actions[0]
        for i in range(0,len(actions)):
            name=actions[i]
            emoji=numberlist[i]
            choices.append([actions[i], name, emoji])
            outputString=outputString + " {}[{}] ".format(emoji, name)
        message=await self.textchannel.send(content="{}\n{}".format(prompt, outputString))
        result=await make_internal_tiebreaker(self.bot, self.user, self.textchannel, choices, message=message, timeout_enable=True, remove_after=True, delete_after=True)
        return result

    #output
    async def update_player_message(self, embed):
        if(self.player_msg==None):
            self.player_msg=await self.textchannel.send("Newly_sent", embed=embed)
        else:
            await self.player_msg.edit(content="$", embed=embed)
    async def update_grid_message(self, iurl, round):
        #updates the grid image.
        embed=discord.Embed(title="Map", colour=discord.Colour(0x7289da), description="Round: {}".format(round))
        embed.set_image(url="{imgurl}".format(imgurl=iurl))
        if(self.image_msg==None):
            self.image_msg=await self.textchannel.send("Newly_sent", embed=embed)
        else:
            await self.image_msg.edit(content="$", embed=embed)
    async def send_pil_image(self, pil):
        #sends pil image, but saves it to a image_binary first
        #returns message
        image_mes=None
        with io.BytesIO() as image_binary:
            pil.save(image_binary, 'PNG') #Returns pil object.
            image_binary.seek(0)
            image_mes=await self.textchannel.send(content="Preview:", file=discord.File(fp=image_binary, filename='image.png'))
        return image_mes
