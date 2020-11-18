from .. import card
from ..SkillLibrary.skillcluster import *


class TestCard(card.CardBase):
    """docstring for TestCard."""
    ID = 0x000FF  # • ID- The internal ID of the card.

    # All cards have this, and they should all be unique.
    # consists of a five digit hexadecimal number
    # Cards should be referenced by this ID, not their name.
    # (00000  to FFFFF, makes maximum of 1,048,576 cards.
    def __init__(self):
        self.ID = 0x000FF  # • ID- The internal ID of the card.
        # All cards have this, and they should all be unique.
        # consists of a five digit hexadecimal number
        # Cards should be referenced by this ID, not their name.
        # (00000  to FFFFF, makes maximum of 1,048,576 cards.
        name = "Test Name"
        icon = "🎴"
        image = "NA"
        type = "None"
        super().__init__(self.ID, name, icon, type, image)


class TestCard2(card.CardBase):
    """docstring for TestCard."""
    ID = 0x0000F  # • ID- The internal ID of the card.

    # All cards have this, and they should all be unique.
    # consists of a five digit hexadecimal number
    # Cards should be referenced by this ID, not their name.
    # (00000  to FFFFF, makes maximum of 1,048,576 cards.
    def __init__(self):
        self.ID = 0x0000F  # • ID- The internal ID of the card.
        # All cards have this, and they should all be unique.
        # consists of a five digit hexadecimal number
        # Cards should be referenced by this ID, not their name.
        # (00000  to FFFFF, makes maximum of 1,048,576 cards.
        name = "Test Name 2"
        icon = "🎴"
        image = "NA"
        type = "None"
        super().__init__(self.ID, name, icon, type, image)


class TestCreature1(card.CreatureCard):
    """docstring for TestCard."""
    ID = 0x00001  # • ID- The internal ID of the card.

    # All cards have this, and they should all be unique.
    # consists of a five digit hexadecimal number
    # Cards should be referenced by this ID, not their name.
    # (00000  to FFFFF, makes maximum of 1,048,576 cards.
    def __init__(self):
        self.ID = 0x00001  # • ID- The internal ID of the card.
        # All cards have this, and they should all be unique.
        # consists of a five digit hexadecimal number
        # Cards should be referenced by this ID, not their name.
        # (00000  to FFFFF, makes maximum of 1,048,576 cards.
        name = "Test Name For A Creature"
        icon = "🐻"
        image = "NA"
        type = "None"
        hp = 10
        speed = 9  # Speed is 0-99.
        # Defining summon cost.
        summonr = 3
        summonb = 2
        summong = 2
        # Defining Skills.
        skill1 = BasicAttack(name="Custom Name 1", trigger="command", target=("Adjacent", "Enemy", "x1"), type="type",
                             limit="limit", description="Type description here.", damage=12)
        skill2 = None  # CustomSkill2("Custom Name 2", "trigger", "target", "type", "limit", "Type description here.")
        skill3 = None  # CustomSkill3("Custom Name 3", "trigger", "target", "type", "limit", "Type description here.")
        # Defining move Style.
        movestyle = "STEP 2"
        movelimit = 1

        super().__init__(self.ID, name, icon, image=image, \
                         hp=hp, speed=2, \
                         summoncost_r=summonr, summoncost_b=summonb, summoncost_g=summong, \
                         skill_1=skill1, skill_2=skill2, skill_3=skill3, \
                         movestyle=movestyle, movelimit=movelimit)


class TestCreatureAlpha(card.CreatureCard):
    # This is test creature alpha, so its ID is A for now.
    ID = 0x0000A

    def __init__(self):
        self.ID = 0x0000A
        name = "Alpha"
        icon = "🐻"
        image = "https://media.discordapp.net/attachments/749673596514730055/772497364816101376/unknown.png"
        type = ""
        hp = 5
        speed = 20

        # The summoning cost of this creature
        summonr = 2
        summonb = 2
        summong = 2

        # These are the creature's skills
        skill1 = MultiAttack("Multi Attacks", "command", ("Rectilinear", "Enemy", "x3"), "attack", "limit",
                             "description", damage=1, attacks=3, damage_tag="")
        skill2 = BasicShield(name="Shield", shield_amount=2)
        skill3 = BasicHeal("BasicHeal", "command", ("Any", "Ally", "x1"), "support", "limit", "description",
                           heal_amount=1)

        # This defines the creature's move style
        move_style = "STEP 1"
        movelimit = 1

        super().__init__(self.ID, name, icon, image=image, hp=hp, speed=speed, summoncost_r=summonr,
                         summoncost_b=summonb, summoncost_g=summong,
                         skill_1=skill1, skill_2=skill2, skill_3=skill3, movestyle=move_style, movelimit=movelimit)


class TestCreatureBeta(card.CreatureCard):
    # This is test creature beta, so its ID is B for now.
    ID = 0x0000B

    def __init__(self):
        self.ID = 0x0000B
        name = "Beta"
        icon = "🐻"
        image = "https://media.discordapp.net/attachments/749673596514730055/772497364816101376/unknown.png"
        type = ""
        hp = 15
        speed = 4

        # The summoning cost of this creature
        summonr = 3
        summonb = 3
        summong = 3

        # These are the creature's skills
        skill1 = MultiAttack("Multi Attacks", "command", ("Rectilinear", "Enemy", "x3"), "attack", "limit",
                             "description", damage=1, attacks=3, damage_tag="")
        skill2 = BasicShield("Shield", "command", ("self", "Ally", "x1"), "limit", "description", shield_amount=2)
        skill3 = BasicHeal("BasicHeal", "command", ("Any", "Ally", "x1"), "support", "limit", "description",
                           heal_amount=1)

        # This defines the creature's move style
        move_style = "SAME COLUMN LIMIT 3"
        movelimit = 1

        super().__init__(self.ID, name, icon, image=image, hp=hp, speed=speed, summoncost_r=summonr,
                         summoncost_b=summonb, summoncost_g=summong,
                         skill_1=skill1, skill_2=skill2, skill_3=skill3, movestyle=move_style, movelimit=movelimit)


class TestCreatureDelta(card.CreatureCard):
    # This is test creature delta, so its ID is D for now.
    ID = 0x0000D

    def __init__(self):
        self.ID = 0x0000D
        name = "Delta"
        icon = "🐻"
        image = "https://media.discordapp.net/attachments/749673596514730055/772497364816101376/unknown.png"
        type = ""
        hp = 9
        speed = 8

        # The summoning cost of this creature
        summonr = 1
        summonb = 2
        summong = 1

        # These are the creature's skills
        skill1 = BasicAttack("Custom Name 1", "command", ("Adjacent", "Enemy", "x1"), "type", "limit",
                             "Type description here.", damage=5)
        skill2 = BasicShield("Shield", "command", ("self", "Ally", "x1"), "limit", "description", shield_amount=2)
        skill3 = BasicHeal("BasicHeal", "command", ("Any", "Ally", "x1"), "support", "limit", "description",
                           heal_amount=1)

        # This defines the creature's move style
        move_style = "SAME DIAGONAL LIMIT 2"
        movelimit = 1

        super().__init__(self.ID, name, icon, image=image, hp=hp, speed=speed, summoncost_r=summonr,
                         summoncost_b=summonb, summoncost_g=summong,
                         skill_1=skill1, skill_2=skill2, skill_3=skill3, movestyle=move_style, movelimit=movelimit)


class TestCreature2(card.CreatureCard):
    # This is test creature 2, so its ID is 2 for now.
    ID = 0x00002

    def __init__(self):
        self.ID = 0x00002
        name = "Creature2"
        icon = "🐻"
        image = "https://media.discordapp.net/attachments/749673596514730055/772497364816101376/unknown.png"
        type = ""
        hp = 7
        speed = 9

        # The summoning cost of this creature
        summonr = 2
        summonb = 4
        summong = 1

        # These are the creature's skills
        skill1 = BasicAttack("Custom Name 1", "command", ("Adjacent", "Enemy", "x1"), "type", "limit",
                             "Type description here.", damage=6)
        skill2 = BasicShield("Shield", "auto", ("self", "Ally", "x1"), "type", "limit", "description", shield_amount=1)
        skill3 = BasicHeal("BasicHeal", "command", ("Any", "Ally", "x1"), "support", "limit", "description",
                           heal_amount=2)

        # This defines the creature's move style
        move_style = "STEP 2"
        movelimit = 1

        super().__init__(self.ID, name, icon, image=image, hp=hp, speed=speed, summoncost_r=summonr,
                         summoncost_b=summonb, summoncost_g=summong,
                         skill_1=skill1, skill_2=skill2, skill_3=skill3, movestyle=move_style, movelimit=movelimit)


class TestCreature3(card.CreatureCard):
    # This is test creature 3, so its ID is 3 for now.
    ID = 0x00003

    def __init__(self):
        self.ID = 0x00003
        name = "creature 3"
        icon = "🐻"
        image = "https://media.discordapp.net/attachments/749673596514730055/772497364816101376/unknown.png"
        type = ""
        hp = 9
        speed = 8

        # The summoning cost of this creature
        summonr = 3
        summonb = 2
        summong = 3

        # These are the creature's skills
        skill1 = BasicAttack("Custom Name 1", "command", ("Adjacent", "Enemy", "x1"), "type", "limit",
                             "Type description here.", damage=8)
        skill2 = BasicShield("Shield", "command", ("self", "Ally", "x1"), "limit", "description", shield_amount=1)
        skill3 = BasicHeal("BasicHeal", "command", ("Any", "Ally", "x1"), "support", "limit", "description",
                           heal_amount=3)

        # This defines the creature's move style
        move_style = "HOP X -2 Y -2"
        movelimit = 1

        super().__init__(self.ID, name, icon, image=image, hp=hp, speed=speed, summoncost_r=summonr,
                         summoncost_b=summonb, summoncost_g=summong,
                         skill_1=skill1, skill_2=skill2, skill_3=skill3, movestyle=move_style, movelimit=movelimit)
