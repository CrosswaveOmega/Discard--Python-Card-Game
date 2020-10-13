import discord
import operator

from discord.ext import commands, tasks
from discord.utils import find
from discord import Webhook, AsyncWebhookAdapter

import inspect
from .CardLibrary import cardcluster1

from .card import *

def itermodule(idToFind): #Currently O(n).  there has to be a better way to do this.
    lista=[m[0] for m in inspect.getmembers(cardcluster1, inspect.isclass) if m[1].__module__ == cardcluster1.__name__]
    for x in lista:
        print(x)
        if vars(getattr(cardcluster1, x))["ID"] == idToFind:
            return getattr(cardcluster1, x)()
    return None

class CardRetrievalClass():  #by no means what the final version should use.
    def setup(self):
        print("TBD")
    def getByID(self, ID):
        val=itermodule(ID)
        if(val!=None):
            return val
        return False
