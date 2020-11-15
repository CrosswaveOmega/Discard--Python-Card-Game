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

async def inventory_entry_to_card_object(bot, inventory_card):
    "With a inventory entry, returns a card."
    id=inventory_card["card_id"]
    custom=inventory_card["custom"]
    newcard=CardRetrievalClass().getByID(int(id, 16))
    if(custom!=None):
        customobject=await CustomRetrievalClass().getByID(custom, bot) #Test
        newcard.apply_custom(custom=customobject)
    return newcard
