
from .. import card

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
        summoncost_r=3
        summoncost_b=2
        summoncost_g=2
        #Defining Skills.
        skill1=CustomSkill1("Custom Name 1", "trigger", "target", "type", "limit")
        super().__init__(self.ID, name, icon, image=image, \
        hp=hp, speed=2, summoncost_r=0, summoncost_b=0, summoncost_g=0, \
        skill_1=None, skill_2=None, skill_3=None, \
        movestyle="", movelimit=1)
    class CustomSkill1(card.Skill):#Nested class
        def __init__(self, name="No name set.", trigger="command", target="other", type="tbd", limit="tbd", description="none"): #there's probably a better way to do this.
            super().__init__(name, trigger, target, type, limit)description
        def doSkill(self, user, target, game_ref):
            #What the skill will actually do.
            #user is the entity using the skill.
            #target is what the skill is being used on.
            #Game_ref is a refrence to the Card_Duel's helper class.
            #Use a dictionary.
            print("TBD")
