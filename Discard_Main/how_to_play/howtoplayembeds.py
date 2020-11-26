import discord
import operator
import io
import json
import aiohttp
import asyncio
import datetime

from PIL import Image, ImageTk, ImageGrab, ImageDraw, ImageFont
from pathlib import Path
#{"color": 7506394, "type": "rich", "description": "**Description** AS\n **Cards** DF", "title": "This is a name."}
from discord.ext import commands, tasks
from discord.utils import find
from discord import Webhook, AsyncWebhookAdapter
j="""
    {
      "title": "What's all this?",
      "description": "Discohook is a free tool that allows you to build Discord messages and embeds for use in your server.\\n Discohook sends messages using *webhooks*, an API feature that allows third-party services to *blindly* send messages into text channels. While webhooks can send messages, they cannot respond to user interactions such as messages.",
      "color": 7506394
    }
"""
directory = "help"

def get_file_from_directory(id):
    # filename from json.
    filename = str(id) + ".json"
    file = Path(directory + "/" + filename)
    if file.exists():  # check if this file exists.
        return file
    else:
        return None
def get_content(id):
    file = get_file_from_directory(id)
    if(file != None):
        f = file.open(mode='rb')
        #string = f.read()
        dicton=json.load(f)
        f.close()
        return dicton
def make_how_to_play_embeds():
    J="""{"color": 7506394, "type": "rich", "description": "**Description**  AS **Cards** DF", "title": "This is a name."}"""
    embeds=get_content("how")
    lis=get_content("game")
    embed_list=[]
    for d in lis:
        embed=discord.Embed.from_dict(d)
        embed_list.append(embed)
    return embed_list
