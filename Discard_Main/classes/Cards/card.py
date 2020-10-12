import discord
import operator

from discord.ext import commands, tasks
from discord.utils import find
from discord import Webhook, AsyncWebhookAdapter


from .CardLibrary.cardcluster1 import *



class CardBase():  #Wip.

    def __init__(self, ID, name, icon, type, image="None"):
        self.ID=ID          #• ID- The internal ID of the card.
                            #All cards have this, and they should all be unique.
                            #consists of a five digit hexadecimal number
                            #Cards should be referenced by this ID, not their name.
                            #(00000  to FFFFF, makes maximum of 1,048,576 cards.
        self.name=name      #• Name- The name of the card.  Customizable by a user,
        self.icon=icon      #• Icon- A emoji that will represent this card, placed before.   Customizable by a user,<:thonkang:219069250692841473>
        self.image=image    #• Image- Background image the card displays.   Customizable by a user,
        self.type=type      #• Type- The type of card this is.

    def __str__(self):
        return self.icon + "|" + self.name + "|" + self.type + "|"+ str(self.ID)

    def apply_custom(self, custom):
        """Change the set values found in custom."""
        if hasattr(custom, 'name'):
            self.name=custom.name
        if hasattr(custom, 'icon'):
            self.icon=custom.icon
        if hasattr(custom, 'image'):
            self.icon=custom.icon
        if hasattr(custom, 'type'):
            self.type=custom.type



class CreatureCard(card.CardBase):
    """docstring for TestCard."""
    def __init__(self,  ID, name, icon, type, image="None", hp=0, speed=0):
        self.ID=0x000FF          #• ID- The internal ID of the card.
                            #All cards have this, and they should all be unique.
                            #consists of a five digit hexadecimal number
                            #Cards should be referenced by this ID, not their name.
                            #(00000  to FFFFF, makes maximum of 1,048,576 cards.
        name="Test Name"
        icon="<:thonkang:219069250692841473>"
        image="NA"
        type="Creature"
        self.hp=hp
        self.speed=speed

        super().__init__(self.ID,name, icon, type, image)
        self.arg = arg





#Driver Code.
if __name__ == "__main__":
    print(str(CardRetrievalClass().getByID(0xFFFFFFFF)))
