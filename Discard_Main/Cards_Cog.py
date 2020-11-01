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
from .classes.Cards.custom import CustomRetrievalClass
from .classes.imagemakingfunctions.imaging import *
from .classes.userservices.userprofile import SingleUserProfile
from .classes.Cards.DeckBuilding import *
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
        author=ctx.message.author;
        channel=ctx.message.channel;

        SingleUser = SingleUserProfile("arg")
        card_id=args[0]
        user_id = author.id
        profile = SingleUser.getByID(user_id)
        result=profile.get_inv_cards_by_id(int(card_id, 16))

        newcard=CardRetrievalClass().getByID(int(card_id, 16))
        card= result[0]
        if(card["custom"]!=None):
            customobject=await CustomRetrievalClass().getByID(card["custom"], bot) #Test
            newcard.apply_custom(custom=customobject)
            embed=newcard.to_DiscordEmbed()
            await channel.send(content="so I'm trying to make the embed below me appear wider.  wiiiiiiiiiiiiiiiiiiiiiiiiider.", embed=embed)


        print("NOTE: NEED TO MAKE CARD EMBED FORMAT CLASS IN CARD.PY")


    @commands.command(pass_context=True)
    async def addCustomold(self, ctx, *args): #A very rudimentary card retrieval system.
        '''
        syntax: cardGet [CardId] CustomId]
        [CardId]: The Card ID you want to get.
        [CustomId]: The CustomId you want to apply to the card.

        '''
        bot=ctx.bot
        auth=ctx.message.author;
        channel=ctx.message.channel;
        leng=len(args)

        cipher=await CustomRetrievalClass().addCustom("TEXT", bot)
        await channel.send(content=cipher)

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

class DeckCog(commands.Cog):
    """Commands for deck management."""
    @commands.command(pass_context=True)
    async def createDeck(self, ctx, *args):
        '''
        syntax: createDeck [Name]
        [Name]: The name of the new deck

        '''
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        SingleUser = SingleUserProfile("arg")

        user_id = author.id
        profile = SingleUser.getByID(user_id)
        if(len(args) == 1):
            deckName = args[0]
            deck = DeckBuilding()
            deck.set_deck_name(deckName)
            for i in profile.get_decks():
                if(i.get_deck_name() == deckName):
                    await cahnnel.send(str("A deck with that name already exist."))
                    return
            profile.add_deck(deck)
        else:
            await channel.send(str("Please enter the command along with a deck name."))

    @commands.command(pass_context=True)
    async def renameDeck(self, ctx, *args):
        '''
        syntax: renameDeck [Name][New_Deck_Name]
        [Name]: The current name of the deck
        [New_Deck_Name]: The new name of the deck you would like to change to

        '''
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        SingleUser = SingleUserProfile("arg")
        user_id = author.id
        profile = SingleUser.getByID(user_id)
        if(len(args) == 2):
            deckName = args[0]
            new_deckName = args[1]
            for j in profile.get_decks():
                if(j.get_deck_name() == new_deckName):
                    await channel.send(str("A deck with that name already exist."))
                    return
            for i in profile.get_decks():
                if(i.get_deck_name() == deckName):
                    i.set_deck_name(new_deckName)
                    return
            await channel.send(str("The deck does not exist."))
        else:
            await channel.send(str("Please enter the command with the deck name along with a new deck name."))


    @commands.command(pass_context=True)
    async def deleteDeck(self, ctx, *args):
        '''
        syntax: deleteDeck [Name]
        [Name]: The current name of the deck

        '''
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        SingleUser = SingleUserProfile("arg")

        user_id = author.id
        profile = SingleUser.getByID(user_id)
        if(len(args) == 1):
            deckName = args[0]
            for i in profile.get_decks():
                if(i.get_deck_name() == deckName):
                    profile.get_decks().remove(i)
                    break
            await channel.send(str("The deck does not exist."))
        else:
            await channel.send(str("Please enter the command with the deck name."))


    @commands.command(pass_context=True)
    async def changeDescription(self, ctx, arg1, *, arg2):
        '''
        syntax: changeDescription [Name][New_Deck_Description]
        [Name]: The current name of the deck
        [New_Deck_Description]: The new description for the deck you would like to change

        '''
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        SingleUser = SingleUserProfile("arg")

        user_id = author.id
        profile = SingleUser.getByID(user_id)
        deckName = arg1
        new_deckDescription = arg2
        for i in profile.get_decks():
            if(i.get_deck_name() == deckName):
                i.set_deck_description(new_deckDescription)
                return
        await channel.send(str("The deck does not exist."))

    @commands.command(pass_context=True)
    async def addCard(self, ctx, *args): #check if card exist in inventory, args can have custom name, card id, and card name
        '''
        syntax: addCard [Name_of_deck][Card in inventory]
        [Name_of_deck]: The current name of the deck
        [Card in inventory]: The card you would like to add

        '''
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        SingleUser = SingleUserProfile("arg")

        user_id = author.id
        profile = SingleUser.getByID(user_id)
        if (len(args) == 2):
            deckName = args[0]

            card = args[1]
            deck = None
            multimatched=card_multimatch(profile, card)

            if (multimatched != None): #check if card exist in player's inventory.
                cardvalue=multimatched[0]
                if(len(multimatched)>1):# Tiebreaker is needed here.
                    print("Place Tiebreaker Here.")#do tiebreaker.
                for i in profile.get_decks():
                    if(i.get_deck_name() == deckName):
                        deck = i
                        break
                if(deck.inDeck(cardvalue) == False):
                    deck.addToDeck(cardvalue) #to be updated when card_multimatch is finished, looks for the unique card_id if given either the same card name. *Use tiebreaker
                else:
                    await channel.send("Hang on, This card is already in your deck!")
            else:
                await channel.send("This card was not found in your inventory.")


    @commands.command(pass_context=True)
    async def removeCard(self, ctx, *args):
        '''
        syntax: removeCard [Name_of_deck][Card in deck]
        [Name_of_deck]: The current name of the deck
        [Card in deck]: The card you would like to remove

        '''
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        SingleUser = SingleUserProfile("arg")

        user_id = author.id
        profile = SingleUser.getByID(user_id)
        if (len(args) == 2):
            deckName = args[0]
            card = args[1]
            deck = None
            multimatched=card_multimatch(profile, card)
            if(multimatched != None):
                for i in profile.get_decks():
                    if(i.get_deck_name() == deckName):
                        deck = i
                        break
                cardvalue=multimatched[0]
                if(len(multimatched)>1):# Tiebreaker is needed here.
                    print("Place Tiebreaker Here.")#do tiebreaker.
                if(deck.inDeck(cardvalue) == True):
                    deck.removeFromDeck(cardvalue)
                else:
                    await channel.send("The card is not in your deck.")
            else:
                await channel.send("The card is not in your deck.")


    @commands.command(pass_context=True)
    async def multi_add(self, ctx, arg1, *, arg2):
        '''
        syntax: multi_add [Name_of_deck][Card in inventory 1][Card in inventory 2]...[Card in inventory n]
        [Name_of_deck]: The current name of the deck
        [Card in inventory]...[Card in inventory n]: The n cards you would like to add to the deck

        '''
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        SingleUser = SingleUserProfile("arg")

        user_id = author.id
        profile = SingleUser.getByID(user_id)
        deckName = arg1
        cards = arg2.split()
        does_not_exist = []
        deck = None
        for j in cards:
            if(card_multimatch(profile, j) == None): #use card_multimatch to check if the cards exist in the inventory
                does_not_exist.append(j)
                cards.remove(j)
        for i in profile.get_decks():
            if(i.get_deck_name() == deckName):
                deck = i
                break
        deck.addListToDeck(cards)
        if(len(does_not_exist) != 0):
            await channel.send("The following cards does not exist in your inventory: {}".format(does_not_exist))


    @commands.command(pass_context=True)
    async def multi_remove(self, ctx, arg1, *, arg2):
        '''
        syntax: multi_remove [Name_of_deck][Card in inventory 1][Card in inventory 2]...[Card in inventory n]
        [Name_of_deck]: The current name of the deck
        [Card in inventory]...[Card in inventory n]: The n cards you would like to remove from the deck

        '''
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        SingleUser = SingleUserProfile("arg")

        user_id = author.id
        profile = SingleUser.getByID(user_id)
        deckName = arg1
        cards = arg2.split()
        does_not_exist = []
        deck = None
        counter = 0
        for j in profile.get_decks():
            if(j.get_deck_name() == deckName):
                deck = j
                break
        for i in cards: #converts all cards regardless of identifier to card_id
            if(card_multimatch(profile, i) == None):
                cards.remove(i)
            else:
                cards[counter] = card_multimatch(profile, i)[0]["card_id"]
            counter = counter + 1
        deck.removeListFromDeck(cards)
