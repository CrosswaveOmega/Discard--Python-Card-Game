import discord
import operator
import csv
from discord.ext import commands, tasks
from discord.utils import find
from discord import Webhook, AsyncWebhookAdapter
from pathlib import Path
import json

from ..Cards.custom import CustomRetrievalClass
from ..Cards.cardretrieval import CardRetrievalClass
from ..Cards.DeckBuilding import Deck

directory = "saveData"


class SingleUserProfile:
    class __SingleUserProfile:  # Singleton Design.  Based on https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html
        def __init__(self, arg="P."):
            self.val = arg
            self.buffer = {}  # Every single loaded userprofile

        def getIDinternal(self, id):
            if(self.checkforidinbuffer(id)):
                return self.buffer[str(id)]
            else:  # ID is not in buffer.
                file = self.get_file_from_directory(id)
                if(file != None):
                    f = file.open(mode='r')
                    string = f.read()
                    self.buffer[str(id)] = UserProfile(
                        user_id=id, dictionary_to_use=json.loads(string))
                    f.close()
                    print("Should initalize new user profile with the dictionary_to_use param set to the translated contents of file, add that into buffer under user id.")
                    return self.buffer[str(id)]
                    # Load contents of file into new UserProfile, add that into buffer.
                else:
                    self.buffer[str(id)] = UserProfile(user_id=id)
                    print(
                        "Should initalize new default user profile, add that into buffer under user id.")
                    return self.buffer[str(id)]
                    # Initalize new file.

        # Saves the UserProfile object at key id in buffer to a file.
        def save_buffer_entry(self, id):
            if(self.checkforidinbuffer(id)):
                # filename from json.
                filename = "userprofile_id_" + str(id) + ".json"
                file = Path(directory + "/" + filename)
                f = file.open(mode="w+")

                string_to_write = json.dumps(
                    self.buffer[str(id)].to_dictionary(), sort_keys=True, indent=4)
                f.write(string_to_write)
                f.close()

        def save_all_internal(self):  # save everything in buffer.
            for i, v in self.buffer.items():
                self.save_buffer_entry(i)

        def checkforidinbuffer(self, id):
            key_to_lookup = str(id)
            if key_to_lookup in self.buffer:
                return True
            else:
                return False

        def get_file_from_directory(self, id):
            # filename from json.
            filename = "userprofile_id_" + str(id) + ".json"
            file = Path(directory + "/" + filename)
            if file.exists():  # check if this file exists.
                return file
            else:
                return None

        def __str__(self):
            return repr(self) + self.val
    instance = None

    # Internally, it keeps a single instance of the __SingleDictionary class in memory.
    def __init__(self, arg="None"):
        if not SingleUserProfile.instance:
            SingleUserProfile.instance = SingleUserProfile.__SingleUserProfile(
                arg)
        else:
            SingleUserProfile.instance.val = arg

    def getByID(self, id):
        # Initial chekc
        return SingleUserProfile.instance.getIDinternal(id)

    def save_all(self):
        SingleUserProfile.instance.save_all_internal()

    def __getattr__(self, name):
        return getattr(self.instance, name)


class UserProfile:
    def __init__(self, user_id, dictionary_to_use=None):
        self.user_id = user_id
        self.cards = {}  # dictionary of ids. every entry in dictionary is dictionary of format
        #{"card_id":card_id, "custom":id_of_custom_applied, "inv_key":new_key_name}
        # new_key_name is the key.
        self.customs = []  # list of customs made by the user.
        # self.cards_customs={} #dictionary.  Key is card Id and
        self.exp = 0
        self.level = 0
        # self.cardcount=0 #irrelivant.
        self.coins = 0
        self.stars = 0
        self.tickets = 0
        self.decks = []  # Max 99.
        # To do: Work out saving/loading for decks. -DONE!

        self.primary_deck = ""

        #From dictionary.
        if(dictionary_to_use != None):
            for i, v in dictionary_to_use.items():
                if hasattr(self, i):
                    if(i == "decks"):
                        for deck_lookup in v:
                            self.decks.append(Deck(dictionary=deck_lookup))
                    else:
                        setattr(self, i, v)

    def to_dictionary(self):
        dictionary = vars(self).copy()
        new_deck_list = []
        for deck in dictionary["decks"]:
            new_deck_list.append(deck.to_dictionary())
        dictionary["decks"] = new_deck_list
        return dictionary

    def get_cards(self):
        return self.cards

    def get_customs(self):
        return self.customs

    def get_decks(self):
        print(self.decks)
        return self.decks

    def get_deck_by_name(self, deckName):
        for i in self.get_decks():
            if (i.get_deck_name() == deckName):
                return i
        return None
    def get_primary_deck(self):
        decks=self.get_decks()
        if len(decks)>=1:
            if self.primary_deck != "":
                return self.get_deck_by_name(self.primary_deck)
        return None
    def set_primary_deck(self, deckname):
        self.primary_deck=deckname
    def get_primary_deck_name(self):
        return self.primary_deck

    def apply_custom(self, key, cipher_id):
        if key in self.cards:
            self.cards[key]['custom'] = cipher_id

    def add_custom(self, cipher_id):
        # cipher id
        self.customs.append(cipher_id)
    def has_card(self, card_id):
        #check if user has card.
        for key, card_value in self.cards.items():  # find first available spot if keyname is gone
            if card_id == card_value["card_id"]:
                return True
        return False
    def add_card(self, card_id):
        current_length = len(self.cards)
        new_key_name = "key" + str(current_length)
        if new_key_name in self.cards:
            current_count = 0
            for key, card_value in self.cards.items():  # find first available spot if keyname is gone
                key_name="key" + str(current_count)
                #print(key_name)
                if not key_name in self.cards: #This key_name is not in self.cards
                    new_key_name=key_name
                    self.cards[new_key_name] = {"card_id": card_id, "custom": None, "inv_key": new_key_name}
                    return
                current_count = current_count + 1
        self.cards[new_key_name] = {
            "card_id": card_id, "custom": None, "inv_key": new_key_name}
    def check_key(self, key):
        if key in self.cards:
            return True
        return False
    def get_inventory_entry_by_key(self, key):
        return self.cards[key]

    def add_deck(self, deck):
        print(str(deck))
        print(self.decks)
        self.decks.append(deck)
        print(self.decks)

    def check_customs_by_id(self, custom):
        if (custom in self.customs):
            return custom
        return None

    def get_inv_cards_by_id(self, card_id):
        returnList = []  # Duplicates exist.  (Returns the dictionary value.)
        for key_name, card_value in self.cards.items():
            if card_id == int(card_value["card_id"], 16):
                tuple = (key_name, card_value)
                returnList.append(card_value)
        print("Getting Return List")
        print(json.dumps(returnList))
        return returnList
    def get_inv_cards_by_customid(self, custom_id):
        returnList = []  # Duplicates exist.  (Returns the dictionary value.)
        for key_name, card_value in self.cards.items():
            if custom_id == card_value["custom"]:
                tuple = (key_name, card_value)
                returnList.append(card_value)
        print("Getting Return List")
        print(json.dumps(returnList))
        return returnList


    def get_inv_cards_by_custom_name(self, name):
        # Duplicates exist.  (Returns a tuple with the key_name)
        returnList = []
        for key_name, card_value in self.cards.items():
            if(card_value["custom"] != None):
                custom_name = CustomRetrievalClass(
                ).retrieve_name(card_value["custom"])
                if(custom_name == name):
                    returnList.append(card_value)
        return returnList

    def get_exp(self):
        return self.exp

    def set_exp(self, value):
        self.exp = value

    def set_level(self, value):
        self.level = value

    def get_level(self):
        return self.level

#    def set_cardcount(self, value):
#        self.cardcount = value

    def get_cardcount(self):
        return len(self.cards)

    def get_customcount(self):
        return len(self.customs)

    def get_deckcount(self):
        return len(self.decks)

    def set_coins(self, value):
        self.coins = value

    def get_coins(self):
        return self.coins

    def set_stars(self, value):
        self.stars = value

    def get_stars(self):
        return self.stars
        
    def get_tickets(self):
        return self.tickets

    def card_name_list(self, custget=None):
        # returns a small list of card names.
        # Duplicates exist.  (Returns a tuple with the key_name)
        returnList = []
        cards = CardRetrievalClass()
        for key_name, card_value in self.cards.items():
            card = cards.getByID(int(card_value["card_id"], 16))
            string = card.get_name()
            if(card_value["custom"] != None):
                custom_name = CustomRetrievalClass(
                ).retrieve_name(card_value["custom"])
                string = "'{}'".format(custom_name)
            returnList.append(string)
        return returnList

    def custom_id_list(self, custget=None):
        # returns a small list of card names.
        # Duplicates exist.  (Returns a tuple with the key_name)
        returnList = []
    #    cards=CardRetrievalClass()
        for cid in self.customs:
            #card=cards.getByID(int(card_value["card_id"], 16))
            string = str(cid)
            returnList.append(string)
        return returnList
