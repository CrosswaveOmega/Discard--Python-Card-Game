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

directory="saveData"





class SingleUserProfile:
    class __SingleUserProfile: #Singleton Design.  Based on https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html
        def __init__(self, arg="P."):
            self.val = arg
            self.buffer={} #Every single loaded userprofile
        def getIDinternal(self, id):
            if(self.checkforidinbuffer(id)):
                return self.buffer[str(id)]
            else: #ID is not in buffer.
                file=self.get_file_from_directory(id)
                if(file!= None):
                    f= file.open(mode='r');
                    string=f.read();
                    self.buffer[str(id)]=UserProfile(user_id=id, dictonary_to_use=json.loads(string))
                    f.close()
                    print("Should initalize new user profile with the dictonary_to_use param set to the translated contents of file, add that into buffer under user id.")
                    return self.buffer[str(id)]
                    #Load contents of file into new UserProfile, add that into buffer.
                else:
                    self.buffer[str(id)]=UserProfile(user_id=id)
                    print("Should initalize new default user profile, add that into buffer under user id.")
                    return self.buffer[str(id)]
                    #Initalize new file.
        def save_buffer_entry(self, id): #Saves the UserProfile object at key id in buffer to a file.
            if(self.checkforidinbuffer(id)):
                filename="userprofile_id_"+str(id)+".json" #filename from json.
                file= Path(directory + "/"+ filename)
                f=file.open(mode="w+")

                string_to_write=json.dumps(self.buffer[str(id)].to_dictionary(), sort_keys=True, indent=4)
                f.write(string_to_write)
                f.close()
        def save_all_internal(self): #save everything in buffer.
            for i, v in self.buffer.items():
                self.save_buffer_entry(i)

        def checkforidinbuffer(self, id):
            key_to_lookup = str(id)
            if key_to_lookup in self.buffer:
              return True
            else:
              return False
        def get_file_from_directory(self, id):
            filename="userprofile_id_"+str(id)+".json" #filename from json.
            file= Path(directory + "/"+ filename)
            if file.exists():#check if this file exists.
                return file
            else:
                return None
        def __str__(self):
            return repr(self) + self.val
    instance = None
    def __init__(self, arg="None"):  #Internally, it keeps a single instance of the __SingleDictionary class in memory.
        if not SingleUserProfile.instance:
            SingleUserProfile.instance = SingleUserProfile.__SingleUserProfile(arg)
        else:
            SingleUserProfile.instance.val = arg
    def getByID(self, id):
        #Initial chekc
        return SingleUserProfile.instance.getIDinternal(id)
    def save_all(self):
        SingleUserProfile.instance.save_all_internal()

    def __getattr__(self, name):
        return getattr(self.instance, name)


class UserProfile:
    def __init__(self, user_id, dictonary_to_use=None):
        self.user_id=user_id
        self.cards={} #dictionary of ids. every entry in list is dictionary of format {"card_id":card_id, "custom":id_of_custom_applied}
        self.customs=[] #list of customs made by the user.
        #self.cards_customs={} #dictionary.  Key is card Id and
        self.exp=0
        self.level=0
        #self.cardcount=0 #irrelivant.
        self.coins=0
        self.stars=0



        self.decks=[] #Max 99.

        if(dictonary_to_use!=None):
            for i, v in dictonary_to_use.items():
                if hasattr(self, i):
                    setattr(self, i, v)

    def to_dictionary(self):
        return vars(self)

    def get_cards(self):
        return self.cards

    def get_customs(self):
        return self.customs

    def get_decks(self):
        return self.decks

    def apply_custom(self, key, cipher_id):
        if key in self.cards:
            self.cards[key]['custom']=cipher_id

    def add_custom(self, cipher_id):
        #cipher id
        self.customs.append(cipher_id)

    def add_card(self, card_id):
        current_length=len(self.cards)
        new_key_name="key"+str(current_length)
        if new_key_name in self.cards: #
            current_count=0
            for key, card_value in self.cards: #find first available spot if keyname is gone
                if card_id == card_value["card_id"]:
                    returnList.append(key,card_value)
                    key_name="key"+str(count)
                    if not key_name in self.cards:
                        new_key_name=key_name
                    count=count + 1
        self.cards[new_key_name]={"card_id":card_id, "custom":None, "inv_key":new_key_name}

    def get_inventory_entry_by_key(self, key):
        return self.cards[key]

    def add_deck(self, deck):
        self.decks.append(deck)

    def check_customs_by_id(self, custom):
        if (custom in self.customs):
            return custom
        return None

    def get_inv_cards_by_id(self, card_id):
        returnList = [] #Duplicates exist.  (Returns the dictonary value.)
        for key_name, card_value in self.cards.items():
            if card_id == int(card_value["card_id"], 16):
                tuple=(key_name,card_value)
                returnList.append(card_value)
        print("Getting Return List")
        print(json.dumps(returnList))
        return returnList

    def get_inv_cards_by_custom_name(self, name):
        returnList = [] #Duplicates exist.  (Returns a tuple with the key_name)
        for key_name, card_value in self.cards.items():
            if(card_value["custom"]!=None):
                custom_name=CustomRetrievalClass().retrieve_name(card_value["custom"])
                if(custom_name==name):
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

    def card_name_list(self, custget=None):
        #returns a small list of card names.
        returnList = [] #Duplicates exist.  (Returns a tuple with the key_name)
        cards=CardRetrievalClass()
        for key_name, card_value in self.cards.items():
            card=cards.getByID(int(card_value["card_id"], 16))
            string=card.get_name()
            if(card_value["custom"]!=None):
                custom_name=CustomRetrievalClass().retrieve_name(card_value["custom"])
                string="'{}'".format(custom_name)
            returnList.append(string)
        return returnList

    def custom_id_list(self, custget=None):
        #returns a small list of card names.
        returnList = [] #Duplicates exist.  (Returns a tuple with the key_name)
    #    cards=CardRetrievalClass()
        for cid in self.customs:
            #card=cards.getByID(int(card_value["card_id"], 16))
            string=str(cid)
            returnList.append(string)
        return returnList
