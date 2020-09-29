import discord
import operator
import io

import unicodedata
from asyncio import gather


def checkInteger(value):
    try:
        value = int(value)
        return True;
    except ValueError:
        print("NOT A INTEGER")
        return False
        pass  # it was a string, not an int.

async def getMessage(auth, chan):
    def check(m):
        return m.author == auth and m.channel == chan
    msg=await bot.wait_for('message', check=check)
    print("clear");
    print(msg.content)
    return msg

async def getInput(ctx):
    msg=await getMessage(ctx.message.author, ctx.message.channel)
#    print(reactionFirst, messageFirst);
    cont=""
    cont=msg.Content
    print("RUNNING")
    await msg.delete()
    return cont
async def confirm(ctx):
    bot=ctx.bot
    auth=ctx.message.author;
    channel=ctx.message.channel;
    confirmLoop=True
    topicMessage=await channel.send(content="Are you sure?  type y for yes and n for no:")
    value=False
    while confirmLoop:
        dictionary={"BALLOT BOX WITH CHECK":"yes", "NO ENTRY SIGN":"no"}
        choice=await getInput(ctx)
        #valid reactions:
        if(choice=="yes" or choice=="y" or choice=="Yes" or choice=="Y"):
            confirmLoop=False;
            value= True;
        if(choice=="no" or choice=="n" or choice=="No" or choice=="N"):
            confirmLoop=False;
            value= False;
        await topicMessage.edit(content="Please type y, yes, n, or no...")
    topicMessage.delete()
    return value

async def sendAndDelete(chan, content, seconds=1.2):
    errorMess=await chan.send(content)
    await asyncio.sleep(seconds)
    await errorMess.delete()
