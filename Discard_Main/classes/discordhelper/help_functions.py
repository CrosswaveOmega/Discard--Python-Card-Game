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
from ..Cards.cardretrieval import CardRetrievalClass
from ..Cards.custom import CustomRetrievalClass


def changeDisplayAllHelp():
    name="changeDisplayAll"
    desc= "Changes the name, icon, and image of a card in your inventory"
    usage="[card_id] [new_name] <emoji>"
    parameters="""
    [card_id] : the card id of the card in your inventory you want to edit.
    [new_name] : The new name of the card, surrounded in single or double quotes.
    <emoji> : Optional.  A new icon for this card.
    Upload a image with this command to set that as the new image of the card!
    """
    example="""
    example: `>changeDisplayAll 00001 "New Name" 💛`
    Changes the card with id:`00001`'s Name to "New Name", and it's icon to '💛'.
    00001 is the card_id
    "New Name" is the new name to change to.
    💛 is the new icon to set.

    If you have multiple cards with a id of 00001, a tiebreaker will be returned.
    Reminder, again, you can upload a image with this command to set it's image to that.
    """
    embed = discord.Embed(title="help: {}".format(name),
                          colour=discord.Colour(0x7289da),
                          description=desc)
    embed.add_field(name="Usage",value="**>{}** {}".format(name, usage), inline=False)

    embed.add_field(name="parameters",value="{}".format(parameters), inline=False)
    embed.add_field(name="Example",value="{}".format(example), inline=False)

    return embed
