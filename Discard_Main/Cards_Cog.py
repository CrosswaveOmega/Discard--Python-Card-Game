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
from .classes.Cards.cardretrieval import CardRetrievalClass
from .classes.discordhelper.tiebreaker import make_tiebreaker
from .classes.Cards.custom import CustomRetrievalClass
from .classes.imagemakingfunctions.imaging import *
from .classes.userservices.userprofile import SingleUserProfile
#from discord.ext.tasks import loop

#Primary area with commands.

class CardCog2(commands.Cog):
    """Commands for testing system goes here."""
    @commands.command()
    async def tiebreaker(self, ctx, *args): #Add card.
        '''
        syntax: tiebreaker
        This function is for testing the Tiebreaker system.

        The tiebreaker system, when presented with a list, will send
        '''
        bot=ctx.bot
        auth=ctx.message.author;
        channel=ctx.message.channel;
        choices=[
        ["Case 0","0","<:_0:754494641050615809>"],
        ["Case 1","1","<:_1:754494641096622153>"],
        ["Case 2","2","<:_2:754494640752951307>"],
        ["Case 3","3","<:_3:754494641264394301>"],
        ["Case 4","4","<:_4:754494641117855792>"],
        ["Case 5","5","<:_5:754494641084301472>"],
        ["Case 6","6","<:_6:754494640865935391>"],
        ["Case 7","7","<:_7:754494640870129712>"],
        ["Case 8","8","<:_8:754494641151148032>"],
        ["Case 9","9","<:_9:754494641105272842>"]
        ]
        message=await channel.send("This is a test of the Reaction+Message based user responce system.  \n Respond to this message with a single number or a reaction.")
        cont=await make_tiebreaker(ctx, choices, message=message, clear_after=True)
        if(cont!=None):
            await channel.send(cont)
        else:
            await channel.send("Invalid input.")
        message=await channel.send("This is a test of the Reaction+Message based user responce system, with a 30 second timeout.  \n Respond to this message with a single number or a reaction.")
        cont=await make_tiebreaker(ctx, choices, message=message, timeout=True, clear_after=True)
        if(cont!=None):
            await channel.send(cont)
        else:
            await channel.send("Invalid input.")
class CardCog(commands.Cog):
    """Commands for cards."""
    @commands.command(pass_context=True, aliases=['stampV'])
    async def stamp(self, ctx, *args):
        bot=ctx.bot
        auth=ctx.message.author;
        channel=ctx.message.channel;
        leng=len(args)
    @commands.command(pass_context=True)
    async def numbertoimage(self, ctx, *args):
            bot=ctx.bot
            auth=ctx.message.author;
            channel=ctx.message.channel;
            leng=len(args)
            number=None
            if(leng==1):
                number=int(args[0])
            if(number!=None):
                with io.BytesIO() as image_binary:
                    makeNumber(number).save(image_binary, 'PNG') #Returns pil object.
                    image_binary.seek(0)
                    await channel.send(file=discord.File(fp=image_binary, filename='image.png'))

    @commands.command(pass_context=True)
    async def my_profile(self, ctx, *args):
        """Returns the User's Profile."""
        bot=ctx.bot
        author=ctx.message.author;
        channel=ctx.message.channel;

        user_id=author.id
        leng=len(args)
        profile=SingleUserProfile("B").getByID(user_id)
        diction_profile=profile.to_dictionary()
        number=None
        embed = discord.Embed(title=author.name, colour=discord.Colour(0xce48e9), description=" I dunno what should be the description.  Stuff I guess.  Makes it look a bit WIIIDER.", timestamp=datetime.datetime.today())
        embed.set_image(url=author.avatar_url)
        embed.set_thumbnail(url=author.avatar_url)
        embed.set_author(name="profile", icon_url=author.avatar_url)
        embed.set_footer(text="myprofile command", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        embed.add_field(name="Coins", value= str(profile.get_coins()), inline=False)
        embed.add_field(name="Stars", value=str(profile.get_stars()), inline=False)
#embed.add_field(name="custom", value="Custom was applied.",)
        embed.add_field(name="Exp", value=str(profile.get_exp()), inline=True)
        embed.add_field(name="Level", value=str(profile.get_level()), inline=True)


        mess=await channel.send(content="", embed=embed)

    @commands.command(pass_context=True, aliases=['cardtest'])
    async def getimage(self, ctx, *args):
        """Get a image and return it."""
        bot=ctx.bot
        auth=ctx.message.author;
        channel=ctx.message.channel;
        leng=len(args)
        with io.BytesIO() as image_binary:
            make_summon_cost(1,1,1).save(image_binary, 'PNG') #Returns pil object.
            image_binary.seek(0)
            await channel.send(file=discord.File(fp=image_binary, filename='image.png'))


    @commands.command(pass_context=True)
    async def viewcard(self, ctx, *args): #A very rudimentary card retrieval system.
        '''
        syntax: viewcard [CardId]
        [CardId]: The Card ID you want to get.

        '''
        bot=ctx.bot
        auth=ctx.message.author;
        channel=ctx.message.channel;

        SingleUser = SingleUserProfile("arg")
        card_id=args[0]
        user_id = author.id
        profile = SingleUser.getByID(user_id)
        result=profile.get_inv_cards_by_id(int(card_id, 16)):

        newcard=CardRetrievalClass().getByID(int(card_id, 16))
        if(result["custom"]!=None):
            customtext=await CustomRetrievalClass().getByID(result["custom"], bot)
            newcard.apply_custom(custom=customtext)


        print("NOTE: NEED TO MAKE CARD EMBED FORMAT CLASS IN CARD.PY")



    @commands.command(pass_context=True)
    async def cardGet(self, ctx, *args): #A very rudimentary card retrieval system.
        '''
        syntax: cardGet [CardId] CustomId]
        [CardId]: The Card ID you want to get.
        [CustomId]: The CustomId you want to apply to the card.

        '''
        bot=ctx.bot
        auth=ctx.message.author;
        channel=ctx.message.channel;
        leng=len(args)
        if(leng>=1):
            id=args[0]
            newcard=CardRetrievalClass().getByID(int(id, 16))
            await channel.send(str(newcard))
            if newcard!=False and leng>=2:
                text=await CustomRetrievalClass().getByID(args[1], bot)

                print(text.toCSV())

                newcard.apply_custom(custom=text)
            #    print(text)
                await channel.send(str(newcard))

                text.name="Daikon 02"
                await CustomRetrievalClass().updateCustomByID(text, bot)
