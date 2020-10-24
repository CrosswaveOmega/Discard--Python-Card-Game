
from .. import card
from ..SkillLibrary import skillcluster
class TestCard(card.CardBase):
    """docstring for TestCard."""
    ID=0x000FF          #• ID- The internal ID of the card.
                    #All cards have this, and they should all be unique.
                    #consists of a five digit hexadecimal number
                    #Cards should be referenced by this ID, not their name.
                    #(00000  to FFFFF, makes maximum of 1,048,576 cards.
    def __init__(self):
        self.ID=0x000FF          #• ID- The internal ID of the card.
                            #All cards have this, and they should all be unique.
                            #consists of a five digit hexadecimal number
                            #Cards should be referenced by this ID, not their name.
                            #(00000  to FFFFF, makes maximum of 1,048,576 cards.
        name="Test Name"
        icon="<:thonkang:219069250692841473>"
        image="NA"
        type="None"
        super().__init__(self.ID,name, icon, type, image)


class TestCard2(card.CardBase):
    """docstring for TestCard."""
    ID=0x0000F          #• ID- The internal ID of the card.
                    #All cards have this, and they should all be unique.
                    #consists of a five digit hexadecimal number
                    #Cards should be referenced by this ID, not their name.
                    #(00000  to FFFFF, makes maximum of 1,048,576 cards.
    def __init__(self):
        self.ID=0x0000F          #• ID- The internal ID of the card.
                            #All cards have this, and they should all be unique.
                            #consists of a five digit hexadecimal number
                            #Cards should be referenced by this ID, not their name.
                            #(00000  to FFFFF, makes maximum of 1,048,576 cards.
        name="Test Name 2"
        icon="<:thonkang:219069250692841473>"
        image="NA"
        type="None"
        super().__init__(self.ID,name, icon, type, image)

class TestCreature1(card.CreatureCard):
    """docstring for TestCard."""
    ID=0x00001          #• ID- The internal ID of the card.
                    #All cards have this, and they should all be unique.
                    #consists of a five digit hexadecimal number
                    #Cards should be referenced by this ID, not their name.
                    #(00000  to FFFFF, makes maximum of 1,048,576 cards.
    def __init__(self):
        self.ID=0x00001          #• ID- The internal ID of the card.
                            #All cards have this, and they should all be unique.
                            #consists of a five digit hexadecimal number
                            #Cards should be referenced by this ID, not their name.
                            #(00000  to FFFFF, makes maximum of 1,048,576 cards.
        name="Test Name 2"
        icon="<:thonkang:219069250692841473>"
        image="NA"
        type="None"
        hp=10
        speed=9 #Speed is 0-99.
        #Defining summon cost.
        summonr=3
        summonb=2
        summong=2
        #Defining Skills.
        skill1=BasicAttack("Custom Name 1", "command", ("Adjacent", "Enemy", "x1"), "type", "limit", "Type description here.", damage=12)
        skill2=None #CustomSkill2("Custom Name 2", "trigger", "target", "type", "limit", "Type description here.")
        skill3=None #CustomSkill3("Custom Name 3", "trigger", "target", "type", "limit", "Type description here.")
        #Defining move Style.
        movestyle="STEP 2"
        movelimit=1

        super().__init__(self.ID, name, icon, image=image, \
        hp=hp, speed=2,\
        summoncost_r=summonr, summoncost_b=summonb, summoncost_g=summong, \
        skill_1=skill1, skill_2=skill2, skill_3=skill3, \
        movestyle=movestyle, movelimit=movelimit)
