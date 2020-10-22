import discord
import operator

from discord.ext import commands, tasks
from discord.utils import find
from discord import Webhook, AsyncWebhookAdapter

import inspect
from .CardLibrary import cardcluster1

from .card import *

#def itermodule(idToFind): #Currently O(n).  there has to be a better way to do this.
#    lista=[m[0] for m in inspect.getmembers(cardcluster1, inspect.isclass) if m[1].__module__ == cardcluster1.__name__]
#    for x in lista:
#        print(x)
#        if vars(getattr(cardcluster1, x))["ID"] == idToFind:
#            return getattr(cardcluster1, x)()
#    return None

class CardRetrievalSingleton:
    class __SingleDictionary: #Singleton Design.  Based on https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html
        def __init__(self, arg="P."):
            self.current_status = arg
            self.internal_Dictionary={}
            self.setAll()
        def setAll(self):
            #Update for all new cardclusters.
            lista=[m[0] for m in inspect.getmembers(cardcluster1, inspect.isclass) if m[1].__module__ == cardcluster1.__name__]
            for x in lista:
                print(x)
                id=vars(getattr(cardcluster1, x))["ID"]
                self.internal_Dictionary[str(id)]=getattr(cardcluster1, x)
                print(str(id))
        def __str__(self):
            return repr(self) + self.current_status
    instance = None
    def __init__(self, arg):  #Internally, it keeps a single instance of the __SingleDictionary class in memory.
        if not CardRetrievalSingleton.instance:
            CardRetrievalSingleton.instance = CardRetrievalSingleton.__SingleDictionary(arg)
        else:
            CardRetrievalSingleton.instance.current_status = arg
    def getByID(self, id):
        return CardRetrievalSingleton.instance.internal_Dictionary[str(id)]() #Average case of python dictionary lookup is O(1), worst case is O(n)
    def __getattr__(self, name):
        return getattr(self.instance, name)




class CardRetrievalClass():  #by no means what the final version should use.
    def setup(self):
        sa=CardRetrievalSingleton("WasSetup") #SA is unused.
    def getByID(self, ID):
        val=CardRetrievalSingleton("Last_Loaded").getByID(ID)
        if(val!=None):
            return val
        return False
