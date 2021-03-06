import discord
import operator
import io
import json
import aiohttp
import asyncio
import csv
import datetime
import random
from PIL import Image, ImageTk, ImageGrab, ImageDraw, ImageFont

from discord.ext import commands, tasks
from discord.utils import find
from discord import Webhook, AsyncWebhookAdapter
from .classes.Cards.cardretrieval import CardRetrievalClass
from .classes.discordhelper import *
#from .classes.discordhelper.tiebreaker import make_tiebreaker, card_multimatch
from .classes.Cards.custom import CustomRetrievalClass
from .classes.imagemakingfunctions.imaging import *
from .classes.userservices.userprofile import SingleUserProfile
from .classes.Cards.DeckBuilding import *


# from discord.ext.tasks import loop

# Primary area with commands.


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
        if (len(args) == 1):
            deckName = args[0]
            deck = Deck()
            deck.set_deck_name(deckName)
            for i in profile.get_decks():
                if (i.get_deck_name() == deckName):
                    await channel.send(str("A deck with that name already exist."))
                    return
            print(str(deck))
            profile.add_deck(deck)
            await channel.send("Deck '{}' has been added!".format(deckName))
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
        if (len(args) == 2):
            deckName = args[0]
            new_deckName = args[1]
            for j in profile.get_decks():
                if (j.get_deck_name() == new_deckName):
                    await channel.send(str("A deck with that name already exist."))
                    return
            for i in profile.get_decks():
                if (i.get_deck_name() == deckName):
                    i.set_deck_name(new_deckName)
                    await channel.send("Deck '{}' has been renamed to {}.".format(deckName, new_deckName))
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
        if (len(args) == 1):
            deckName = args[0]
            for i in profile.get_decks():
                if (i.get_deck_name() == deckName):
                    profile.get_decks().remove(i)
                    await channel.send("Deck '{}' has been deleted.".format(deckName))
                    return
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
            if (i.get_deck_name() == deckName):
                i.set_deck_description(new_deckDescription)
                await channel.send(str("The description has been changed!"))
                return
        await channel.send(str("The deck does not exist."))

    @commands.command(pass_context=True)
    async def addToDeck(self, ctx,
                            *args):  # check if card exist in inventory, args can have custom name, card id, and card name
        '''
        syntax: addToDeck [Name_of_deck][Card in inventory]
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
            multimatched = card_multimatch(profile, card)
            list = []
            # check if card exist in player's inventory.
            if (multimatched != None):
                cardvalue = multimatched[0]
                if (len(multimatched) > 1):  # Tiebreaker is needed here.
                    print("Place Tiebreaker Here.")  # do tiebreaker.
                for i in profile.get_decks():
                    if (i.get_deck_name() == deckName):
                        deck = i
                        break
                if (deck == None):  # if the deck entered does not correspond with a deck name in user profile. End the operation
                    await channel.send(str("The deck you've entered does not exist."))
                    return
                print(cardvalue)
                if (deck.inDeck(cardvalue) == False):
                    deck.addToDeck(
                        cardvalue)  # to be updated when card_multimatch is finished, looks for the unique card_id if given either the same card name. *Use tiebreaker
                    await channel.send("Card has been added to '{}' with no problems!".format(deckName))
                else:
                    await channel.send(str("Hang on, This card is already in your deck!"))

                for card in deck.get_deck_cards(): #display deck after successfully or unsuccessfully add card to deck
                    cardobj=await inventory_entry_to_card_object(bot, card)
                    #cardobj = CardRetrievalClass().getByID(int(card["card_id"], 16))
                    list.append(cardobj)
                message_content = ""
                for j in list:
                    message_content = message_content + str(j) + "\n"
                if (len(list) == 0):
                    await channel.send("NO CARDS IN DECK.")
                else:
                    await channel.send(content=message_content)

            else:
                await channel.send(str("This card was not found in your inventory."))
        else:
            await channel.send(str("Please enter the command with the deck name and the card you would like to add."))

    @commands.command(pass_context=True)
    async def removeFromDeck(self, ctx, *args):
        '''
        syntax: removeFromDeck [Name_of_deck][Card in deck]
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
            list = []
            multimatched = card_multimatch(profile, card)
            if (multimatched != None):
                for i in profile.get_decks():
                    if (i.get_deck_name() == deckName):
                        deck = i
                        break
                if (deck == None):  # if the deck entered does not correspond with a deck name in user profile. End the operation
                    await channel.send(str("The deck you've entered does not exist."))
                    return
                cardvalue = multimatched[0]
                if (len(multimatched) > 1):  # Tiebreaker is needed here.
                    print("Place Tiebreaker Here.")  # do tiebreaker.
                if (deck.inDeck(cardvalue) == True):
                    deck.removeFromDeck(cardvalue)
                    await channel.send(str("Card has been removed from deck!"))
                else:
                    await channel.send(str("The card is not in your deck."))
            else:
                await channel.send(str("The card is not in your deck."))

            for card in deck.get_deck_cards():
                cardobj=await inventory_entry_to_card_object(bot, card)
                #cardobj = CardRetrievalClass().getByID(int(card["card_id"], 16))
                list.append(cardobj)
            message_content = ""
            for j in list:
                message_content = message_content + str(j) + "\n"
            if (len(list) == 0):
                await channel.send("NO CARDS IN DECK.")
            else:
                await channel.send(content=message_content)

        else:
            await channel.send(str("Please enter the command with the deck name and the card you would like to add."))

    @commands.command(pass_context=True)
    async def multiAdd(self, ctx, arg1, *, arg2):
        '''
        syntax: multiAdd [Name_of_deck][Card in inventory 1][Card in inventory 2]...[Card in inventory n]
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
        for j in range(len(cards)):
            if (card_multimatch(profile, cards[j]) == None):  # use card_multimatch to check if the cards exist in the inventory
                does_not_exist.append(cards[j])
                cards.remove(cards[j])
            else:
                cards[j] = card_multimatch(profile, cards[j])[0]["inv_key"]
        for i in profile.get_decks():
            if (i.get_deck_name() == deckName):
                deck = i
                break
        if (deck == None):  # if the deck entered does not correspond with a deck name in user profile. End the operation
            await channel.send(str("The deck you've entered does not exist."))
            return
        deck.addListToDeck(cards)
        if (len(does_not_exist) != 0):
            await channel.send(str("The following cards does not exist in your inventory: {}".format(does_not_exist)))
        else:
            await channel.send(str("All the cards have been added to your deck!"))

    @commands.command(pass_context=True)
    async def multiRemove(self, ctx, arg1, *, arg2):
        '''
        syntax: multiRemove [Name_of_deck][Card in inventory 1][Card in inventory 2]...[Card in inventory n]
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
            if (j.get_deck_name() == deckName):
                deck = j
                break
        if (deck == None):  # if the deck entered does not correspond with a deck name in user profile. End the operation
            await channel.send(str("The deck you've entered does not exist."))
            return
        for i in cards:  # converts all cards regardless of identifier to inv_key
            if (card_multimatch(profile, i) == None):
                cards.remove(i)
            else:
                cards[counter] = card_multimatch(profile, i)[0]["inv_key"]
            counter = counter + 1
        deck.removeListFromDeck(cards)
        await channel.send(str("All the cards have been removed from your deck!"))

    @commands.command(pass_context=True)
    async def AllDecks(self, ctx):
        '''
        syntax: AllDecks

        '''
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        SingleUser = SingleUserProfile("arg")

        user_id = author.id
        profile = SingleUser.getByID(user_id)
        list = []
        for i in profile.get_decks():
            list.append(i.get_deck_name())
        message_content = ""
        for j in list:
            message_content = message_content + str(j) + "\n"
        if (len(list) == 0):
            await channel.send("NO DECKS IN USER PROFILE.")
        else:
            await channel.send(content=message_content)

    @commands.command(pass_context=True)
    async def viewDescription(self, ctx, arg):
        '''
        syntax: viewDescription [Name_of_deck]
        [Name_of_deck]: The current name of the deck

        '''
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        SingleUser = SingleUserProfile("arg")

        user_id = author.id
        profile = SingleUser.getByID(user_id)
        deckName = arg
        for i in profile.get_decks():
            if (i.get_deck_name() == deckName):
                await channel.send(str(i.get_deck_description()))
                return
        await channel.send("The deck you've entered does not exist.")

    @commands.command(pass_context=True)
    async def updateDeckCards(self, ctx, *args):
        '''
        syntax: updateDeckCards
        reflect changes in inventory to your Deck.

        '''
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        SingleUser = SingleUserProfile("arg")
        user_id = author.id
        profile = SingleUser.getByID(user_id)
        for i in profile.get_decks():
            i.update_customs(profile.get_cards())

    @commands.command(pass_context=True)
    async def setPrimaryDeck(self, ctx, arg):
        '''
        syntax: setPrimaryDeck [Name_of_deck]
        Set a primary deck.  Primary Decks let you add cards using the >inventory_zoom command
        [Name_of_deck]: The name of the deck you want to set as your Primary Deck.
        <:Deck:782390648702763029>
        '''
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        SingleUser = SingleUserProfile("arg")

        user_id = author.id
        profile = SingleUser.getByID(user_id)
        deckName = arg
        deck = None
        list = []
        for i in profile.get_decks():
            if (i.get_deck_name() == deckName):
                deck = i
                break
        if (deck == None):  # if the deck entered does not correspond with a deck name in user profile. End the operation
            await channel.send(str("The deck you've entered does not exist."))
            return
        profile.set_primary_deck(deckName)
        await channel.send(content="Primary Deck set to {}".format(deckName))


    @commands.command(pass_context=True)
    async def viewCardsInDeck(self, ctx, arg):
        '''
        syntax: viewCardsInDeck [Name_of_deck]
        [Name_of_deck]: The current name of the deck

        '''
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        SingleUser = SingleUserProfile("arg")

        user_id = author.id
        profile = SingleUser.getByID(user_id)
        deckName = arg
        deck = None
        list = []
        for i in profile.get_decks():
            if (i.get_deck_name() == deckName):
                deck = i
                break
        if (deck == None):  # if the deck entered does not correspond with a deck name in user profile. End the operation
            await channel.send(str("The deck you've entered does not exist."))
            return
        for card in deck.get_deck_cards():
            cardobj=await inventory_entry_to_card_object(bot, card)
            #cardobj = CardRetrievalClass().getByID(int(card["card_id"], 16))
            list.append(cardobj)
        message_content = ""
        for j in list:
            message_content = message_content + str(j) + "\n"
        if (len(list) == 0):
            await channel.send("NO CARDS IN DECK.")
        else:
            embed=await deck.to_embed(list)
            await channel.send(content="", embed=embed)

    @commands.command(pass_context=True)
    async def randomAdd(self, ctx, arg):
        '''
        syntax: randomAdd [Name_of_deck]
        [Name_of_deck]: The current name of the deck
        adds a random card in your inventory to the specified deck
        '''
        bot = ctx.bot
        author = ctx.message.author
        channel = ctx.message.channel
        SingleUser = SingleUserProfile("arg")

        user_id = author.id
        profile = SingleUser.getByID(user_id)
        deckName = arg
        deck = None
        for i in profile.get_decks():
            if (i.get_deck_name() == deckName):
                deck = i
                break
        if (deck == None):  # if the deck entered does not correspond with a deck name in user profile. End the operation
            await channel.send(str("The deck you've entered does not exist."))
            return
        inventoryList = list(profile.get_cards().values())
        random_entry = random.choice(inventoryList)
        if(random_entry["inv_key"] in deck) == False:
            deck.addToDeck(random_entry["inv_key"])
        else:
            while True:
                random_entry = random.choice(inventoryList)
                if(random_entry["inv_key"] in deck) == False:
                    deck.addToDeck(random_entry["inv_key"])
                    return
