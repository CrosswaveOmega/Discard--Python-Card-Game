
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
        summonr=3
        summonb=2
        summong=2
        #Defining Skills.
        skill1=CustomSkill1("Custom Name 1", "trigger", "target", "type", "limit", "Type description here.")
        skill2=CustomSkill2("Custom Name 2", "trigger", "target", "type", "limit", "Type description here.")
        skill3=CustomSkill3("Custom Name 2", "trigger", "target", "type", "limit", "Type description here.")
        #Defining move Style.
        movestyle="STEP 2"
        movelimit=1

        super().__init__(self.ID, name, icon, image=image, \
        hp=hp, speed=2,\
        summoncost_r=summonr, summoncost_b=summonb, summoncost_g=summong, \
        skill_1=skill1, skill_2=skill2, skill_3=skill3, \
        movestyle=movestyle, movelimit=movelimit)
    class CustomSkill1(card.Skill):#Nested class
        def __init__(self, name="No name set.", trigger="command", target="other", type="tbd", limit="tbd", description="none"): #there's probably a better way to do this.
            super().__init__(name, trigger, target, type, limit, description)
        def doSkill(self, user, target, game_ref):
            #What the skill will actually do.
            #user is the entity using the skill.
            #target is what the skill is being used on.
            #Game_ref is a refrence to the Card_Duel's helper class.
            #Use a dictionary.
            print("TBD")
    class CustomSkill2(card.Skill):#Nested class
        def __init__(self, name="No name set.", trigger="command", target="other", type="tbd", limit="tbd", description="none"): #there's probably a better way to do this.
            super().__init__(name, trigger, target, type, limit, description)
        def doSkill(self, user, target, game_ref):
            #What the skill will actually do.
            #user is the entity using the skill.
            #target is what the skill is being used on.
            #Game_ref is a refrence to the Card_Duel's helper class.
            #Use a dictionary.
            print("TBD")
    class CustomSkill3(card.Skill):#Nested class
        def __init__(self, name="No name set.", trigger="command", target="other", type="tbd", limit="tbd", description="none"): #there's probably a better way to do this.
            super().__init__(name, trigger, target, type, limit, description)
        def doSkill(self, user, target, game_ref):
            #What the skill will actually do.
            #user is the entity using the skill.
            #target is what the skill is being used on.
            #Game_ref is a refrence to the Card_Duel's helper class.
            #Use a dictionary.
            print("TBD")
