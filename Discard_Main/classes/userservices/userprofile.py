import discord
import operator
import csv
from discord.ext import commands, tasks
from discord.utils import find
from discord import Webhook, AsyncWebhookAdapter
from pathlib import Path
import pickle

class SingleDictionary:
    class __SingleDictionary: #Singleton Design.  Based on https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html
        def __init__(self, arg="P."):
            self.val = arg
            self.buffer={} #A buffer of all.
        def setAll(self):
            #Update for all new cardclusters.
            print("tbd")

        def checkforidinbuffer(self, id):
            key_to_lookup = id
            if key_to_lookup in self.internal_Dictionary:
              return True
            else:
              return False
        def get_file_from_directory(self, id):
            filename="userprofile_id_"+str(id)+".json" #filename from json.
            file= Path(directory + "/"+ filename)
            if file.exists():
                return file
        def __str__(self):
            return repr(self) + self.val
    instance = None
    def __init__(self, arg):  #Internally, it keeps a single instance of the __SingleDictionary class in memory.
        if not SingleDictionary.instance:
            SingleDictionary.instance = SingleDictionary.__SingleDictionary(arg)
        else:
            SingleDictionary.instance.val = arg
    def getByID(self, id):
        return  #Average case of python dictionary lookup is O(1), worst case is O(n)
    def __getattr__(self, name):
        return getattr(self.instance, name)


class UserProfile:
    def __init__(self, dictonary_to_use=None):
        self.cards=[] #List of ids.
        self.customs=[] #list of customs.
        self.exp=0
        self.level=0
        self.cardcount=0
        self.coins=0
        self.stars=0

        if(dictonary_to_use!=None):
            for i, v in dictonary_to_use.items():
                if hasattr(self, i):
                    setattr(self, i, v)

    def to_dictionary(self):
        return vars(self)
