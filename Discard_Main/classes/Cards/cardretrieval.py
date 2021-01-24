import discord
import operator

from discord.ext import commands, tasks
from discord.utils import find
from discord import Webhook, AsyncWebhookAdapter

import inspect
from .CardLibrary import cardcluster1, cardcluster2

from .card import *


# def itermodule(idToFind): #Currently O(n).  there has to be a better way to do this.
#    lista=[m[0] for m in inspect.getmembers(cardcluster1, inspect.isclass) if m[1].__module__ == cardcluster1.__name__]
#    for x in lista:
#        print(x)
#        if vars(getattr(cardcluster1, x))["ID"] == idToFind:
#            return getattr(cardcluster1, x)()
#    return None

class CardRetrievalSingleton:
    class __SingleDictionary:  # Singleton Design.  Based on https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html
        def __init__(self, arg="P."):
            self.current_status = arg
            self.internal_Dictionary = {}
            self.setAll()

        def setCardCluster(self, cardclust):
            # Update for all new cardclusters.
            lista = [m[0] for m in inspect.getmembers(cardclust, inspect.isclass) if
                     m[1].__module__ == cardclust.__name__]
            for x in lista:
                print(x)
                id = vars(getattr(cardclust, x))["ID"]
                self.internal_Dictionary[str(id)] = getattr(cardclust, x)
                print(str(id))

        def setAll(self):
            self.setCardCluster(cardcluster1)

        def __str__(self):
            return repr(self) + self.current_status

    instance = None

    # Internally, it keeps a single instance of the __SingleDictionary class in memory.
    def __init__(self, arg):
        if not CardRetrievalSingleton.instance:
            CardRetrievalSingleton.instance = CardRetrievalSingleton.__SingleDictionary(
                arg)
        else:
            CardRetrievalSingleton.instance.current_status = arg

    def getByID(self, id):
        return CardRetrievalSingleton.instance.internal_Dictionary[
            str(id)]()  # Average case of python dictionary lookup is O(1), worst case is O(n)

    def getAllCards(self):
        list = []
        for id, value in CardRetrievalSingleton.instance.internal_Dictionary.items():
            print(id)
            list.append(value())
        return list

    def __getattr__(self, name):
        return getattr(self.instance, name)


class CardRetrievalClass():  # by no means what the final version should use.
    def setup(self):
        sa = CardRetrievalSingleton("WasSetup")  # SA is unused.

    def getByID(self, ID):
        val = CardRetrievalSingleton("Last_Loaded").getByID(ID)
        if (val != None):
            return val
        return False

    def getMeanSpeed(self):
        print("Starting...")
        cards = CardRetrievalSingleton("GetAllCards").getAllCards()
        total_speed = 0
        card_count = 0
        print("Start")
        for card in cards:
            if(card.get_type() == "Creature"):
                print(card.get_speed())
                total_speed = total_speed + card.get_speed()
                card_count = card_count + 1
        average = total_speed / card_count
        print('end')
        return int(average)

    def getAllCards(self):
        # list = []
        # for name, obj in inspect.getmembers(cardcluster1):
        #    if inspect.isclass(obj):
        #        list.append(getByID(obj.ID))
        print("Starting...")
        return CardRetrievalSingleton("GetAllCards").getAllCards()
