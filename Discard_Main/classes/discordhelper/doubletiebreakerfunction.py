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


async def make_tiebreaker_double(ctx, choices, message=None, timeout_enable=False, delete_after=False,
                                 remove_after=False, clear_after=False, ignore_message=False,
                                 ignore_reaction=False):  # Add card.
    '''
    EXPERIMENTAL.  SUPPOSED TO RETURN WHEN TWO REACTIONS WHERE ADDED.

    '''
    bot = ctx.bot
    auth = ctx.message.author;
    channel = ctx.message.channel;

    output = None

    emoji_list = [
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
    message_dict = {}
    emoji_dict = {}

    def Diff(li1, li2):  # for calculating set difference.
        return (list(list(set(li1) - set(li2)) + list(set(li2) - set(li1))))

    message_to_respond_to = message
    if message == None:
        message_to_respond_to = await channel.send("Tiebreaker!  Please Respond.")
    message_to_respond_to_2 = await channel.send("Tiebreaker!  Please Respond.")
    fetchedmessage = await channel.fetch_message(message_to_respond_to.id)
    reactions = fetchedmessage.reactions
    # print(reactions)
    currentReactions = [str(rea.emoji) for rea in reactions]
    # print(currentReactions)
    # Make dictionaryies
    these_reactions = []
    for ch in choices:
        message_dict[ch[1]] = ch[0]
        emoji_dict[ch[2]] = ch[0]
        if not (ch[2] in currentReactions):
            await message_to_respond_to.add_reaction(ch[2])
            await message_to_respond_to_2.add_reaction(ch[2])
        else:
            await message_to_respond_to.remove_reaction(ch[2], auth)

    def check(m):
        return m.author == auth and m.channel == channel

    rcount = 0

    def checkReaction(reaction, user):
        print(reaction, user)
        return user == auth and reaction.message == message_to_respond_to

    def checkReaction2(reaction, user):
        return user == auth and reaction.message == message_to_respond_to_2

    async def getMessage():
        msg = await bot.wait_for('message', check=check)
        # print("Message ");
        return msg.content

    async def getReaction():  # Get a reaction.
        rea, user = await bot.wait_for('reaction_add', check=checkReaction)
        result = str(rea.emoji)
        return result

    async def getReaction2():  # Get a reaction.
        rea, user = await bot.wait_for('reaction_add', check=checkReaction2)
        result = str(rea.emoji)
        return result

    async def getTwoReactions():
        running = True
        result = None
        middleA, middleB = False, False
        while running:
            print(middleA, middleB)
            ra = asyncio.create_task(getReaction())
            rb = asyncio.create_task(getReaction2())
            tasklist2 = []
            if middleA == False:
                tasklist2.append(ra)
            if middleB == False:
                tasklist2.append(rb)
            done, pending = await asyncio.wait(tasklist2,
                                               return_when=asyncio.FIRST_COMPLETED)  # there's probably a better way to do this.
            #    done, pending2 = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED) #there's probably a better way to do this.
            if ra in done:
                result = ra.result();
                if rb in pending:
                    rb.cancel()
                if rc in pending:
                    rc.cancel()
                middleA = True

            if rb in done:
                result = rb.result();
                if ra in pending:
                    ra.cancel()
                if rc in pending:
                    rc.cancel()
                middleB = True

            if middleA and middleB:
                running = False
        return result

    async def timeoutfunction():  # Get a reaction.
        await asyncio.sleep(30.0)
        return "timeout"

    messagetask = asyncio.create_task(getMessage())
    reactiontask = asyncio.create_task(getTwoReactions())
    timeouttask = asyncio.create_task(timeoutfunction())
    tasklist = [messagetask, reactiontask]
    if ignore_message:
        tasklist = [reactiontask]
    if timeout_enable:
        # print(timeout_enable)
        tasklist.append(timeouttask)
    cont = message_to_respond_to.content
    embed = None
    if (len(message_to_respond_to.embeds) > 0):
        embed = message_to_respond_to.embeds[0]

    # <a:stopwatch:774741008495542284>
    # <a:stopwatch_15:774741008793337856>

    cont = cont + "<a:stopwatch:774741008495542284>"
    await message_to_respond_to.edit(content=cont, embed=embed)
    done, pending = await asyncio.wait(tasklist,
                                       return_when=asyncio.FIRST_COMPLETED)  # there's probably a better way to do this.
    if messagetask in done:
        result = messagetask.result();
        if (result in message_dict):
            output = message_dict[result];
        else:
            print("Invalid Message")
            output = "invalidmessage"
        reactiontask.cancel();
        if timeout_enable:
            timeouttask.cancel();
    if reactiontask in done:
        # print("DONE.")
        result = str(reactiontask.result())
        if (result in emoji_dict):
            output = emoji_dict[result];
        else:
            print("Invalid Reaction")
            output = "invalidreaction"
        if (remove_after):
            await message_to_respond_to.remove_reaction(result, auth)
        messagetask.cancel();
        if timeout_enable:
            timeouttask.cancel();
    if timeouttask in done:
        messagetask.cancel();
        reactiontask.cancel();
        output = timeouttask.result();
    await message_to_respond_to_2.delete()
    if clear_after:
        await message_to_respond_to.clear_reactions()
    if delete_after:
        await message_to_respond_to.delete()
    return output
