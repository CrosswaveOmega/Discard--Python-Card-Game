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
from .classes.discordhelper.tiebreaker import make_tiebreaker, card_multimatch
from .classes.discordhelper.pagesystem import *
from .classes.Cards.custom import CustomRetrievalClass
from .classes.imagemakingfunctions.imaging import *
from .classes.userservices.userprofile import SingleUserProfile
from .classes.Cards.DeckBuilding import *


# from discord.ext.tasks import loop


# <a:stopwatch:774741008495542284>
# <a:stopwatch_15:774741008793337856>


class CardCog2(commands.Cog):
    """Commands for testing system goes here."""

    @commands.command()
    async def pagetest(self, ctx, *args):  # Add card.
        '''
        syntax: pagetest
        This function is for testing the page system.
        '''
        bot = ctx.bot
        auth = ctx.message.author
        channel = ctx.message.channel
        await pages(ctx, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 7,
                    header="Test of pages, ", content="This is some content")

    @commands.command()
    async def stopwatches(self, ctx, *args):  # Add card.
        '''
        syntax: pagetest
        This function is for testing the page system.
        '''
        bot = ctx.bot
        auth = ctx.message.author
        channel = ctx.message.channel
        await ctx.channel.send("<a:stopwatch:774741008495542284>\n <a:stopwatch_15:774741008793337856>")

    @commands.command()
    async def tiebreaker(self, ctx, *args):  # Add card.
        '''
        syntax: tiebreaker
        This function is for testing the Tiebreaker system.

        The tiebreaker system, when presented with a list, will send
        '''
        bot = ctx.bot
        auth = ctx.message.author
        channel = ctx.message.channel
        choices = [
            ["Case 0", "0", "<:_0:754494641050615809>"],
            ["Case 1", "1", "<:_1:754494641096622153>"],
            ["Case 2", "2", "<:_2:754494640752951307>"],
            ["Case 3", "3", "<:_3:754494641264394301>"],
            ["Case 4", "4", "<:_4:754494641117855792>"],
            ["Case 5", "5", "<:_5:754494641084301472>"],
            ["Case 6", "6", "<:_6:754494640865935391>"],
            ["Case 7", "7", "<:_7:754494640870129712>"],
            ["Case 8", "8", "<:_8:754494641151148032>"],
            ["Case 9", "9", "<:_9:754494641105272842>"]
        ]
        message = await channel.send(
            "This is a test of the Reaction+Message based user responce system.  \n Respond to this message with a single number or a reaction.")
        cont = await make_tiebreaker(ctx, choices, message=message, clear_after=True)
        if (cont != None):
            await channel.send(cont)
        else:
            await channel.send("Invalid input.")
        message = await channel.send(
            "This is a test of the Reaction+Message based user responce system, with a 30 second timeout.  \n Respond to this message with a single number or a reaction.")
        cont = await make_tiebreaker(ctx, choices, message=message, timeout_enable=False, clear_after=True)
        if (cont != None):
            await channel.send(cont)
        else:
            await channel.send("Invalid input.")


class CardCog(commands.Cog):
    """Commands for cards."""

    @commands.command(pass_context=True, aliases=['stampV'])
    async def stamp(self, ctx, *args):
        bot = ctx.bot
        auth = ctx.message.author
        channel = ctx.message.channel
        leng = len(args)

    @commands.command(pass_context=True)
    async def numbertoimage(self, ctx, *args):
        bot = ctx.bot
        auth = ctx.message.author
        channel = ctx.message.channel
        leng = len(args)
        number = None
        if (leng == 1):
            number = int(args[0])
        if (number != None):
            with io.BytesIO() as image_binary:
                # Returns pil object.
                makeNumber(number).save(image_binary, 'PNG')
                image_binary.seek(0)
                await channel.send(file=discord.File(fp=image_binary, filename='image.png'))

    @commands.command(pass_context=True)
    async def inventory(self, ctx):
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        SingleUser = SingleUserProfile("arg")

        user_id = author.id
        profile = SingleUser.getByID(user_id)
        list = []
        for key, card in profile.get_cards().items():
            newCard = CardRetrievalClass().getByID(int(card["card_id"], 16))
            if (card["custom"] != None):
                custom = await CustomRetrievalClass().getByID(card["custom"], bot)
                newCard.apply_custom(custom)
            list.append(str(newCard))
        message_content = ""

        # for i in list:
        #    message_content=message_content+str(i)+"\n"

        if (len(list) == 0):
            await channel.send("NO CARDS IN INVENTORY.")
        else:
            await pages(ctx, list)
            # await channel.send(content=message_content)

    @commands.command(pass_context=True)
    async def myprofile(self, ctx, *args):
        """Returns the User's Profile."""
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel

        user_id = author.id
        leng = len(args)
        profile = SingleUserProfile("B").getByID(user_id)
        diction_profile = profile.to_dictionary()
        number = None
        embed = discord.Embed(title="Card Profile", colour=discord.Colour(0xce48e9),
                              description=" I dunno what should be the description.  Stuff I guess.  Makes it look a bit WIIIDER.",
                              timestamp=datetime.datetime.now())
        embed.set_image(url=author.avatar_url)
        print(author.avatar_url)
        # embed.set_thumbnail(url=author.avatar_url)
        personal_retrieval = CustomRetrievalClass(bot)

        cardhead = "Cards: {}".format(profile.get_cardcount())
        card_list = ''.join([' {},'.format(item[0:32])
                             for item in profile.card_name_list()])
        card_list = "{:400}".format(card_list[:-1])

        customhead = "Customs: {}".format(profile.get_customcount())
        custom_list = ''.join([' {},'.format(item[0:32])
                               for item in profile.custom_id_list()])
        custom_list = "{:400}".format(custom_list[:-1])

        embed.set_author(name=author.name, icon_url=author.avatar_url)
        embed.set_footer(text="myprofile command",
                         icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        embed.add_field(name="**Inventory**",
                        value="{}\n```{}```{}\n```{}```\n".format(
                            cardhead, card_list, customhead, custom_list),
                        inline=False)

        deckhead = "Decks: {}".format(profile.get_deckcount())
        deck_list = ''.join([' {},'.format(item.get_shorthand_rep())
                             for item in profile.get_decks()])
        deck_list = "{:400}".format(deck_list[:-1])
        embed.add_field(name=deckhead, value="```{}```".format(
            deck_list), inline=False)

        embed.add_field(name="Coins", value=str(
            profile.get_coins()), inline=True)
        embed.add_field(name="Stars", value=str(
            profile.get_stars()), inline=True)
        embed.add_field(name="TBD", value=str(
            profile.get_stars()), inline=True)
        # embed.add_field(name="custom", value="Custom was applied.",)
        embed.add_field(name="Exp", value=str(profile.get_exp()), inline=True)
        embed.add_field(name="Level", value=str(
            profile.get_level()), inline=True)
        embed.add_field(name="TBD", value=str(
            profile.get_stars()), inline=True)

        mess = await channel.send(content="", embed=embed)

    @commands.command(pass_context=True, aliases=['cardtest'])
    async def getimage(self, ctx, *args):
        """Get a image and return it."""
        bot = ctx.bot
        auth = ctx.message.author
        channel = ctx.message.channel
        leng = len(args)
        with io.BytesIO() as image_binary:
            # Returns pil object.
            make_summon_cost(1, 1, 1).save(image_binary, 'PNG')
            image_binary.seek(0)
            await channel.send(file=discord.File(fp=image_binary, filename='image.png'))

    @commands.command(pass_context=True)
    # A very rudimentary card retrieval system.
    async def viewcard(self, ctx, *args):
        '''
        syntax: viewcard [CardId]
        [CardId]: The Card ID you want to get.
        Gets the card_id specified out of your inventory
        '''
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel

        SingleUser = SingleUserProfile("arg")
        card_id = args[0]
        user_id = author.id
        profile = SingleUser.getByID(user_id)
        result = profile.get_inv_cards_by_id(int(card_id, 16))

        newcard = CardRetrievalClass().getByID(int(card_id, 16))
        print(
            "\n Viewcard command.  Ideally, this will return multiple cards if the user has a duplicate.  Not now though. \n")
        for card in result:
            if (card["custom"] != None):
                # Test
                customobject = await CustomRetrievalClass().getByID(card["custom"], bot)
                newcard.apply_custom(custom=customobject)
                embed = newcard.to_DiscordEmbed()
                await channel.send(content=str(newcard), embed=embed)
        if (len(result) == 0):
            embed = newcard.to_DiscordEmbed()
            await channel.send(content=str(newcard), embed=embed)

        print("NOTE: NEED TO MAKE CARD EMBED FORMAT CLASS IN CARD.PY")

    @commands.command(pass_context=True)
    # A very rudimentary card retrieval system.
    async def addCustomold(self, ctx, *args):
        '''
        syntax: cardGet [CardId] CustomId]
        [CardId]: The Card ID you want to get.
        [CustomId]: The CustomId you want to apply to the card.

        '''
        bot = ctx.bot
        auth = ctx.message.author
        channel = ctx.message.channel
        leng = len(args)

        cipher = await CustomRetrievalClass().addCustom("TEXT", bot)
        await channel.send(content=cipher)

    @commands.command(pass_context=True)
    # A very rudimentary card retrieval system.
    async def carddex(self, ctx, *args):
        '''
        syntax: carddex

        Returns a list of every single card in the game.
        '''
        bot = ctx.bot
        auth = ctx.message.author
        channel = ctx.message.channel
        leng = len(args)
        param1 = 0
        if (leng >= 1):
            param1 = args[0]
        newcardlist = CardRetrievalClass().getAllCards()
        list = [str(card) for card in newcardlist]
        await pages(ctx, list, header="Carddex", content="Below: Every Card Currently in the game.", perpage=10)
        # for card in newcardlist:
        #    await channel.send(str(card))

    @commands.command(pass_context=True)
    # A very rudimentary card retrieval system.
    async def cardGet(self, ctx, *args):
        '''
        syntax: cardGet [CardId] CustomId]
        [CardId]: The Card ID you want to get.
        [CustomId]: The CustomId you want to apply to the card.

        '''
        bot = ctx.bot
        auth = ctx.message.author
        channel = ctx.message.channel
        leng = len(args)
        if (leng >= 1):
            id = args[0]
            newcard = CardRetrievalClass().getByID(int(id, 16))
            await channel.send(str(newcard))
            if newcard != False and leng >= 2:
                text = await CustomRetrievalClass().getByID(args[1], bot)

                #    print(text.toCSV())

                newcard.apply_custom(custom=text)
                #    print(text)
                await channel.send(str(newcard))

                text.name = "Daikon 02"
                await CustomRetrievalClass().updateCustomByID(text, bot)
