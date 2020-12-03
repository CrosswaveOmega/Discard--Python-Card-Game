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



async def add_exp_point(profile, exp=0):  # A example command.
    # Singleton Object that gets a user based on their id.
    profile.set_exp(profile.get_exp() + exp)

    # await channel.send(str(newcard))
async def add_coin(profile, coin=0):
    # increase the coins in user's account by the amount passed in the argument
    # if no argument is passed, then increase the coins by 4
    profile.set_coins(profile.get_coins() + coin)


async def incr_stars(channel, profile):
    # increase the amount of the user's stars by 1 if their coins are greater than or equal to 20
    if (profile.get_coins() >= 20):
        await channel.send("You got a star!")
        profile.set_stars(profile.get_stars() + 1)
        profile.set_coins(profile.get_coins() - 20)

async def incr_level(channel, profile):
    # increase the user's level by 1 if their exp is greater than or equal to 100
    if (profile.get_exp() >= 100):
        await channel.send("You gained a level!")
        profile.set_level(profile.get_level() + 1)
        profile.set_exp(profile.get_exp() - 100)
