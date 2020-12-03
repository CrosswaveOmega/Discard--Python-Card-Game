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
    # To Do- Make Better Buffer system.
    def __init__(self, textchannel, user, bot):
        self.textchannel = textchannel  # Text channel to send input to.
        self.user = user
        self.bot = bot
        self.announceCount=0



        self.input_buffer = []
        print("tbd")
        # THE MESSAGES.
        self.image_msg = None
        self.player_msg = None
        self.current_msg = None
        self.grid_url = "https://media.discordapp.net/attachments/780514923075469313/781631060593213470/512px-AAA_SVG_Chessboard_and_chess_pieces_02.png"
        self.image_embed = embed = discord.Embed(
            title="place", colour=discord.Colour(0x7289da), description="New")
        self.player_embed = embed = discord.Embed(
            title="place", colour=discord.Colour(0x7289da), description="New")
        self.current_embed = embed = discord.Embed(
            title="place", colour=discord.Colour(0x7289da), description="New")

        self.emoji_pedia={}
        self.emoji_pedia["MOVE"]="<:MOVE:782370461526655036>"
        self.emoji_pedia["DRAW"]="<a:DRAW:782347650459631658>"
        self.emoji_pedia["SKILL"]="<:SKILL:782348097434943499>"
        self.emoji_pedia["SUMMON"]="<a:SUMMON:782367512599592960>"

        self.webhook_message=None

    async def postMessageAsWebhook(self, message_content, display_username, avatar_url, embed=[]):
        """posts a message as a webhook
        :param message_content: content of message
        :param display_username: name to display of webhook
        :param avatar_url: url to paste webhook as.
        """
        print(len(embed))
        text_channel=self.textchannel
        webhooks=await text_channel.webhooks()
        webhook=None
        for web in webhooks:
            name=web.name
            if (text_channel.name in name):
                webhook=web
        if(webhook==None):
            webhook=await text_channel.create_webhook(name="DUELHOOK_"+text_channel.name, reason="For sending a message in this channel.")
        newContent=message_content
        mess=await webhook.send(content=newContent, username=display_username,avatar_url=avatar_url, embeds=embed, wait=True)
        return mess
    def has_something_in_buffer(self):
        if len(self.input_buffer) > 0:
            return True
        return False

    def set_input_buffer(self, buff=[]):
        self.input_buffer=buff

    def get_avatar_url(self):
        """returns the avatar url of the user"""
        return self.user.avatar_url
    def get_user_name(self):
        """returns the avatar url of the user"""
        return self.user.name

    def get_special_emoji(self, name):
        if name in self.emoji_pedia:
            return self.emoji_pedia[name]
        return None




    # INPUT
    async def get_user_choice(self, choice_list, prompt="Select a choice."):
        # get command from user.
        """select a choice from a list.  Same as Tiebreaker.
        choice_list is a single list of strings.  prompt is a possible prompt.
        """
        choices = []
        numberlist = ["1️⃣", "2️⃣", "3️⃣", "4️⃣",
                      "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        defchoice = ["back", [""], '🔙']
        choices.append(defchoice)
        outputString = ""
        for i in range(0, len(choice_list)):
            name = choice_list[i]
            namelist = [name]
            emoji = numberlist[i]
            choices.append([choice_list[i], namelist, emoji])
            outputString = outputString + " {}[{}] ".format(emoji, name)
        messagecontent = "{}\n{}".format(prompt, outputString)
        result, self.input_buffer = await make_internal_tiebreaker_with_buffer(self.bot, self.user, self.textchannel, choices, buffer=self.input_buffer, message_content=messagecontent, timeout_enable=True, delete_after=True, delete_input_message=True)
        return result

    async def get_user_card(self, choice_list, prompt=""):
        """select a cardobject from a list of card objects.  Same as Tiebreaker.
        choice_list is a single list of cardobjects.  prompt is a possible prompt.
        """
        choices = []
        numberlist = ["1️⃣", "2️⃣", "3️⃣", "4️⃣",
                      "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        defchoice = ["back", [""], '🔙']
        choices.append(defchoice)
        outputString = ""
        for i in range(0, len(choice_list)):
            name = choice_list[i].get_name()
            namelist = [name]
            emoji = numberlist[i]
            choices.append([choice_list[i], namelist, emoji])
            outputString = outputString + " {}[{}] ".format(emoji, name)
        messagecontent = "{}\n{}".format(prompt, outputString)
        result, self.input_buffer = await make_internal_tiebreaker_with_buffer(self.bot, self.user, self.textchannel, choices, buffer=self.input_buffer, message_content=messagecontent, timeout_enable=True, delete_after=True, delete_input_message=True)
        return result

    async def get_user_piece(self, choice_list, prompt=""):
        """select a piece from a list of piece objects.  Same as Tiebreaker.
        choice_list is a single list of cardobjects.  prompt is a possible prompt.
        """
        choices = []
        numberlist = ["1️⃣", "2️⃣", "3️⃣", "4️⃣",
                      "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        defchoice = ["back", [""], '🔙']
        choices.append(defchoice)
        outputString = ""
        for i in range(0, len(choice_list)):
            name = choice_list[i].get_name()
            namelist = [name]
            emoji = numberlist[i]
            choices.append([choice_list[i], namelist, emoji])
            outputString = outputString + " {}[{}] ".format(emoji, name)
        messagecontent = "{}\n{}".format(prompt, outputString)
        result, self.input_buffer = await make_internal_tiebreaker_with_buffer(self.bot, self.user, self.textchannel, choices, buffer=self.input_buffer, message_content=messagecontent, timeout_enable=True, delete_after=True, delete_input_message=True)
        return result

    async def get_user_command(self, actions, prompt="ENTER COMMAND:"):
        """get command from user.  Same as Tiebreaker.
        actions is a single list of strings.  Prompt is the prompt.
        """
        if len(self.input_buffer)<=0:
            if(self.announceCount>=1):
                await self.send_order()
                self.announceCount=0
        choices = []
        local_commands = ["OVERVIEW", "BOARD", "PLAYER", "CURRENT", "QUIT"]
        numberlist = ["1️⃣", "2️⃣", "3️⃣", "4️⃣",
                      "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        defchoice = ["exit", [""], '🔚']
        choices.append(defchoice)
        outputString = ""
        if(len(actions) == 1):
            # return the first action if there is no need.
            return actions[0]
        for i in range(0, len(actions)):
            name = actions[i]
            emoji = numberlist[i]
            sp=self.get_special_emoji(str(name))
            if(sp):
                emoji=sp
            choices.append([actions[i], [str(name)], emoji])
            outputString = outputString + " {}[{}] ".format(emoji, name)
        for comm in local_commands:
            choices.append([comm, [comm], None])
        messagecontent = "{}\n{}".format(prompt, outputString)
        result, self.input_buffer = await make_internal_tiebreaker_with_buffer(self.bot, self.user, self.textchannel, choices, buffer=self.input_buffer, message_content=messagecontent, timeout_enable=True, delete_after=True, delete_input_message=True)
        return result

    # OUTPUT
    async def send_order(self, p=True, i=True, c=True):
        content="name"
        name="Game"
        avatar="https://cdn.discordapp.com/attachments/780514923075469313/783805708180389888/pixel-64x64_1.png"
        embeds=[self.player_embed, self.image_embed, self.current_embed]
        if(self.webhook_message!=None):
            print("Webhook Message Found")
            await self.webhook_message.delete()
        self.webhook_message = await self.postMessageAsWebhook(content, name, avatar, embeds)
        # if p:
        #     if self.player_msg!=None:
        #         await self.player_msg.delete()
        #     self.player_msg = await self.textchannel.send(embed=self.player_embed)
        # if i:
        #     if self.image_msg!=None:
        #         await self.image_msg.delete()
        #     self.image_msg = await self.textchannel.send(embed=self.image_embed)
        # if c:
        #     if self.current_msg!=None:
        #         await self.current_msg.delete()
        #     self.current_msg = await self.textchannel.send(embed=self.current_embed)

    async def send_announcement(self, announcement, sent=True):
        self.announceCount=self.announceCount+1
        if sent:
            await self.textchannel.send(announcement)

    async def update_current_message(self, embed):
        # For the current creature's turn.
        self.current_embed = embed


    async def update_player_message(self, embed):
        self.player_embed = embed
        #if(self.player_msg == None):
        #    self.player_msg = await self.textchannel.send("Newly_sent", embed=embed)
        #else:
        #    await self.player_msg.edit(embed=embed)

    async def update_grid_message(self, embed):
        # updates the grid image.
        #embed=discord.Embed(title="Map", colour=discord.Colour(0x7289da), description="Round: {}".format(round))
        # embed.set_image(url="{imgurl}".format(imgurl=iurl))
        self.image_embed = embed
        #if(self.image_msg == None):
        #    self.image_msg = await self.textchannel.send("Newly_sent", embed=embed)
        #else:
        #    await self.image_msg.edit(embed=embed)
    async def send_grid_message(self, embed):
        # updates the grid image.
        #embed=discord.Embed(title="Map", colour=discord.Colour(0x7289da), description="Round: {}".format(round))
        # embed.set_image(url="{imgurl}".format(imgurl=iurl))
        print("SENDING GRID MESSAGE.")
        embed.image=discord.Embed.Empty

        await self.textchannel.send("current_grid_status", embed=embed)

    async def send_pil_image(self, pil):
        # sends pil image, but saves it to a image_binary first
        # returns message
        image_mes = None
        with io.BytesIO() as image_binary:
            pil.save(image_binary, 'PNG')  # Returns pil object.
            image_binary.seek(0)
            image_mes = await self.textchannel.send(content="Preview:", file=discord.File(fp=image_binary, filename='image.png'))
        return image_mes
