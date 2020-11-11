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
def card_multimatch_with_type(profile, to_match="", match_by_custom_name=True, match_by_card_id=True, match_by_custom_id=True):
    """
    returns: type of match, match result
    """
    print("TODO: ADD MATCH BY INV KEY.")
    list1= profile.get_inv_cards_by_custom_name(str(to_match)) #returns {"card_id":card_id, "custom":[custom id if applicable], "inv_key":new_key_name}
    list2= profile.get_inv_cards_by_id(int(to_match, 16)) #returns {"card_id":card_id, "custom":[custom id if applicable], "inv_key":new_key_name}
    custom= profile.check_customs_by_id(str(to_match)) #returns {"card_id":card_id, "custom":[custom id if applicable], "inv_key":new_key_name}
    if (len(list1)>=1 and match_by_custom_name):
        return "custom_name", list1
    elif (len(list2)>=1 and match_by_card_id):
        print(list2)
        return "card_id", list2
    elif custom!=None and match_by_custom_id:
        return "custom_id", custom
    return "No_Match_Found", None

def card_multimatch(profile, to_match="", match_by_custom_name=True, match_by_card_id=True, match_by_custom_id=True):
    print("TODO: THIS FUNCTION SHOULD DETERMINE WHICH ELEMENT to_match is.  for now, it will only check if custom_name matches or if card_id matches")
    list1= profile.get_inv_cards_by_custom_name(to_match) #returns {"card_id":card_id, "custom":[custom id if applicable], "inv_key":new_key_name}
    list2= profile.get_inv_cards_by_id(int(to_match, 16)) #returns {"card_id":card_id, "custom":[custom id if applicable], "inv_key":new_key_name}
    custom= profile.check_customs_by_id(to_match) #returns {"card_id":card_id, "custom":[custom id if applicable], "inv_key":new_key_name}
    if (len(list1)>=1 and match_by_custom_name):
        return list1
    elif (len(list2)>=1 and match_by_card_id):
        return list2
    elif custom!=None:
        return custom
    return None

async def make_tiebreaker_with_inventory_entries(ctx, inventory_entries):
    # choices=[
    # ["Case 0","0","<:_0:754494641050615809>"],
    # ["Case 1","1","<:_1:754494641096622153>"],
    # ["Case 2","2","<:_2:754494640752951307>"],
    # ["Case 3","3","<:_3:754494641264394301>"],
    # ["Case 4","4","<:_4:754494641117855792>"],
    # ["Case 5","5","<:_5:754494641084301472>"],
    # ["Case 6","6","<:_6:754494640865935391>"],
    # ["Case 7","7","<:_7:754494640870129712>"],
    # ["Case 8","8","<:_8:754494641151148032>"],
    # ["Case 9","9","<:_9:754494641105272842>"]
    # ]
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
    choices=[]
    defchoice=["exit","back", '🔙']
    choices.append(defchoice)
    current_count=0
    message=""
    ##In hindsight, not the best way to impliment this.
    message=message+"{}:{}".format(defchoice[2], str(defchoice[0]))
    for i in inventory_entries:
        print(i)
        choice=[i,str(current_count), emoji_list[current_count]]
        choices.append(choice)
        newcard=CardRetrievalClass().getByID(int(i["card_id"], 16))
        if(i["custom"]!=None):
            customobject=await CustomRetrievalClass().getByID(i["custom"], ctx.bot) #Test
            newcard.apply_custom(custom=customobject)
        line="{}{}".format(emoji_list[current_count], str(newcard))
        message=message+"\n"+line
        current_count=current_count+1
    message_to_respond_to=await ctx.channel.send(content=message+"\nTiebreaker!  Please Respond.")
    cont=await make_tiebreaker(ctx, choices, message=message_to_respond_to, clear_after=True)
    return cont





async def make_tiebreaker(ctx, choices, message=None, timeout_enable=False, delete_after=False, remove_after=False, clear_after=False, ignore_message=False, ignore_reaction=False): #Add card.
    '''
    This function's sole purpose is to help with what I call a "tiebreaker."

    It takes in a list of choices, and gets the user's input on them.

    If a valid input was not sent, it returns None.

    If timeout is specified, it will terminate after 15 or 30 seconds.


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

    def Diff(li1, li2): #for calculating set difference.
        return (list(list(set(li1)-set(li2)) + list(set(li2)-set(li1))))

    message_to_respond_to=message
    if message==None:
        message_to_respond_to=await channel.send("Tiebreaker!  Please Respond.")

    fetchedmessage=await channel.fetch_message(message_to_respond_to.id)
    reactions=fetchedmessage.reactions
    #print(reactions)
    currentReactions= [str(rea.emoji) for rea in reactions]
    #print(currentReactions)
    #Make dictionaryies
    these_reactions=[]
    for ch in choices:
        message_dict[ch[1]]=ch[0]
        emoji_dict[ch[2]]=ch[0]
        if not (ch[2] in currentReactions):
            await message_to_respond_to.add_reaction(ch[2])
        else:
            await message_to_respond_to.remove_reaction(ch[2], auth)


    def check(m):
        return m.author == auth and m.channel == channel
    def checkReaction(reaction, user):
        return user == auth

    async def getMessage():
        msg=await bot.wait_for('message', check=check)
        #print("Message ");
        return msg.content
    async def getReaction(): #Get a reaction.
        rea, user=await bot.wait_for('reaction_add', check=checkReaction)
        result= str(rea.emoji)
        #print("REACT.")
        return result
    async def timeoutfunction(): #Get a reaction.
        await asyncio.sleep(30.0)
        return "timeout"

    messagetask = asyncio.create_task(getMessage())
    reactiontask = asyncio.create_task(getReaction())
    timeouttask =asyncio.create_task(timeoutfunction())
    tasklist=[messagetask, reactiontask]
    if ignore_message:
        tasklist=[reactiontask]
    if timeout_enable:
        #print(timeout_enable)
        tasklist.append(timeouttask)
    cont=message_to_respond_to.content
    embed=None
    if(len(message_to_respond_to.embeds)>0):
        embed=message_to_respond_to.embeds[0]

    #<a:stopwatch:774741008495542284>
    #<a:stopwatch_15:774741008793337856>
    oldcont= cont
    cont=oldcont+ "<a:stopwatch:774741008495542284>"
    await message_to_respond_to.edit(content=cont, embed=embed)
    done, pending = await asyncio.wait(tasklist, return_when=asyncio.FIRST_COMPLETED) #there's probably a better way to do this.
    if messagetask in done:
        result=messagetask.result();
        if(result in message_dict):
            output=message_dict[result];
        else:
            print("Invalid Message")
            output = "invalidmessage"
        reactiontask.cancel();
        if timeout_enable:
            timeouttask.cancel();
    if reactiontask in done:
        #print("DONE.")
        result=str(reactiontask.result())
        if(result in emoji_dict):
            output=emoji_dict[result];
        else:
            print("Invalid Reaction")
            output="invalidreaction"
        if(remove_after):
            await message_to_respond_to.remove_reaction(result, auth)
        messagetask.cancel();
        if timeout_enable:
            timeouttask.cancel();
    if timeouttask in done:
        messagetask.cancel();
        reactiontask.cancel();
        output=timeouttask.result();
    await message_to_respond_to.edit(content=oldcont, embed=embed)
    if clear_after:
        await message_to_respond_to.clear_reactions()
    if delete_after:
        await message_to_respond_to.delete()
    return output
