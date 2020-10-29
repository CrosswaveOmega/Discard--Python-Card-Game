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



async def multimatch(user, tbd):
    print("")

async def make_tiebreaker(ctx, choices, message=None, timeout=False, delete_after=False, clear_after=False): #Add card.
    '''
    This function's sole purpose is to help with what I call a "tiebreaker."

    It takes in a list of choices, and gets the user's input on them.

    If a valid input was not sent, it returns None.

    If timeout is specified, it will terminate after 30 seconds.


    '''
    bot=ctx.bot
    auth=ctx.message.author;
    channel=ctx.message.channel;

    output=None

    emoji_list=[
    "<:_0:754494641050615809>",
    "<:_1:754494641096622153>",
    "<:_2:754494640752951307>",
    "<:_3:754494641264394301>",
    "<:_4:754494641117855792>",
    "<:_5:754494641084301472>",
    "<:_6:754494640865935391>",
    "<:_7:754494640870129712>",
    "<:_8:754494641151148032>",
    "<:_9:754494641105272842>"
    ]
    message_dict={}
    emoji_dict={}

    message_to_respond_to=message
    if message==None:
        message_to_respond_to=await channel.send("Tiebreaker!  Please Respond.")
    for ch in choices:
        message_dict[ch[1]]=ch[0]
        emoji_dict[ch[2]]=ch[0]
        await message_to_respond_to.add_reaction(ch[2])

    def check(m):
        return m.author == auth and m.channel == channel
    def checkReaction(reaction, user):
        return user == auth

    async def getMessage():
        msg=await bot.wait_for('message', check=check)
        print("Message ");
        return msg.content
    async def getReaction(): #Get a reaction.
        rea, user=await bot.wait_for('reaction_add', check=checkReaction)
        result= str(rea.emoji)
        print("REACT.")
        return rea.emoji
    async def timeout(): #Get a reaction.
        await asyncio.sleep(30.0)
        return "Timeout..."
    messagetask = asyncio.create_task(getMessage())
    reactiontask = asyncio.create_task(getReaction())
    timeouttask =asyncio.create_task(timeout())

    tasklist=[messagetask, reactiontask]
    if timeout:
        tasklist.append(timeouttask)
    done, pending = await asyncio.wait(tasklist, return_when=asyncio.FIRST_COMPLETED) #there's probably a better way to do this.
    if messagetask in done:
        result=messagetask.result();
        output=message_dict[result];
        reactiontask.cancel();
        if timeout:
            timeouttask.cancel();
    if reactiontask in done:
        print("DONE.")
        result=str(reactiontask.result())
        output=emoji_dict[result];
        messagetask.cancel();
        if timeout:
            timeouttask.cancel();
    if timeouttask in done:
        messagetask.cancel();
        reactiontask.cancel();
        output=timeouttask.result();
    if clear_after:
        await message_to_respond_to.clear_reactions()
    if delete_after:
        await message_to_respond_to.delete()
    return output
