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
    id = inventory_card["card_id"]
    custom = inventory_card["custom"]
    newcard = CardRetrievalClass().getByID(int(id, 16))
    if (custom != None):
        customobject = await CustomRetrievalClass().getByID(custom, bot)  # Test
        newcard.apply_custom(custom=customobject)
    return newcard


async def Create_Room_And_Role(auth, bot, guild, number, letter):  # A example command.
    battle_role_name="battle role {} {}".format(str(number), letter)
    channel_name="room {} {}".format(str(number), letter)
    roles = guild.roles
    channels= guild.channels
    role=None
    for r in roles:
        if r.name==battle_role_name:
            role=r
    if (role==None):
        role=await guild.create_role(name=battle_role_name, hoist=True, reason="For Battle")
    print(role)
    overwrites={
    guild.default_role: discord.PermissionOverwrite(read_messages=False),
    guild.me: discord.PermissionOverwrite(read_messages=True),
    role: discord.PermissionOverwrite(read_messages=True)
    }

    newchannel= await guild.create_text_channel(name=channel_name, overwrites=overwrites)
    await auth.add_roles(role)
    return role, newchannel
