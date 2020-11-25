import discord
import operator
import aiohttp
import asyncio

from .CardLibrary import cardcluster1
from .cardretrieval import *
from .custom import *
from .card import *
import json


class Deck():
    def __init__(self, deck_name="Brand new deck", deck_description="Enter a description for this deck.",
                 dictionary=None):
        self.deck_name = deck_name
        self.deck_description = deck_description
        self.deck_cards = []

        if (dictionary != None):  # initalizing from dictionary
            for i, v in dictionary.items():
                if hasattr(self, i):
                    setattr(self, i, v)

    # Setters and Getters
    def set_deck_name(self, deck_name):
        self.deck_name = deck_name

    def get_deck_name(self):
        return self.deck_name

    def get_shorthand_rep(self):
        returnString = "[{}|{}]".format(self.deck_name, len(self.deck_cards))
        return returnString

    def set_deck_description(self, deck_description):
        self.deck_description = deck_description

    def get_deck_description(self):
        return self.deck_description

    def get_deck_cards(self):
        return self.deck_cards

    def get_card_count(self):
         return len(self.deck_cards)

    def update_customs(self, user_inv):
        # update a deck's card customs.
        # user_inv is the result returned by a userprofile's get_cards() funciton.
        for i in range(len(self.deck_cards)):
            # if (self.deck_cards[i]["card_id"] == card_id):
            key = self.deck_cards[i]["inv_key"]
            if (user_inv[key]["custom"] != None):
                self.deck_cards[i]["custom"] = user_inv[key]["custom"]
        return False

    def inDeck(self, card_value):
        # Check if the card_value is in the current deck

        # Note: Switch to matching based on the inv_key
        for i in range(len(self.deck_cards)):
            # if (self.deck_cards[i]["card_id"] == card_id):
            if (self.deck_cards[i]["inv_key"] == card_value["inv_key"]):
                return True
        return False

    def addToDeck(self, card_value):
        # Add card_id along with its custom_id (if available) to the deck
        # UPDATE: card_id is replaced with card_value.  It has to add from a user's inventory.
        self.deck_cards.append(card_value)

    def removeFromDeck(self, card_value):
        # Searches the deck for the card_id for removal and removes it
        # UPDATE: card_id is replaced with card_value.
        # UPDATE: WILL USE inv_key instead.
        #
        for i in range(len(self.deck_cards)):
            if (self.deck_cards[i]["inv_key"] == card_value["inv_key"]):
                del self.deck_cards[i]
                return

    def addListToDeck(self, cards):
        # [cards] is a list of inv_keys
        # Add a list of cards to the deck
        for i in cards:
            self.deck_cards.append(i)

    def removeListFromDeck(self, cards):
        # [cards] is a list of inv_keys
        # Searches the deck for all the cards corresponding to the list passed by the argument and remove them
        counter = 0
        for i in self.deck_cards:
            if (self.deck_cards[counter]["inv_key"] in cards):
                del self.deck_cards[counter]["inv_key"]
            counter = counter + 1

    def to_dictionary(self):
        return vars(self)

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __str__(self):
        # String representation for loading.
        string = "{},{},{}".format(
            self.deck_name, self.deck_description, len(self.deck_cards))
        return string

    async def to_embed(self, cards=[]):
        embed = discord.Embed(title="Deck: {deck_name}".format(deck_name=self.get_deck_name()),
              colour=discord.Colour(0x7289da),
              description="**Description:** {}\n **Cards:** {}".format(self.get_deck_description(), self.get_card_count()))
        this_set=""
        count=0
        for cardobj in cards:
        #    cardobj=await inventory_entry_to_card_object(bot, card)
            string=cardobj.get_shorthand_string() + "\n"
            length=len(string)
            if ( (len(this_set)+length)>1024):
                embed.add_field(name=str(count), value=this_set, inline=False)
                this_set=""
                count=count+1
            this_set = this_set + string
        embed.add_field(name=str(count), value=this_set, inline=False)

        return embed
