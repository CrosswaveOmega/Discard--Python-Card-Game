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
    def __init__(self,  ID, name, icon, image="None", \
    hp=0, speed=0, summoncost_r=0, summoncost_b=0, summoncost_g=0, \
    skill_1=None, skill_2=None, skill_3=None, \
    movestyle="", movelimit=1):
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
        self.summoncost_r=summoncost_r
        self.summoncost_b=summoncost_b
        self.summoncost_g=summoncost_g

        self.skill_1=skill_1
        self.skill_2=skill_2
        self.skill_3=skill_3

        self.move_style=movestyle
        self.move_limit=movelimit
        super().__init__(self.ID,name, icon, type, image)





#Driver Code.
if __name__ == "__main__":
    print(str(CardRetrievalClass().getByID(0xFFFFFFFF)))
