from .. import card
from ..EnumuratedTerms import *
from ..SkillLibrary.skillcluster import *


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
        image = "https://media.discordapp.net/attachments/780514923075469313/783759517070131200/default.png"
        type = "None"
        hp = 10
        speed = 9  # Speed is 0-99.
        # Defining summon cost.
        summonr = 3
        summonb = 2
        summong = 2
        # Defining Skills.
        skill1 = BasicAttack(name="Strong Bash", trigger="command", target=("Adjacent", "Enemy", "x1"), type="attack",
                             cooldown=1, damage=12)
        # CustomSkill2("Custom Name 2", "trigger", "target", "type", "limit", "Type description here.")
        skill2 = None
        # CustomSkill3("Custom Name 3", "trigger", "target", "type", "limit", "Type description here.")
        skill3 = None
        # Defining move Style.
        movestyle = """HOP X 1 Y 2
HOP X 2 Y 1
HOP X -1 Y 2
HOP X -2 Y 1
HOP X 1 Y -2
HOP X 2 Y -1
HOP X -1 Y -2
HOP X -2 Y -1
"""
        movelimit = 1

        super().__init__(self.ID, name, icon, image=image,
                         hp=hp, speed=2,
                         cost_r=summonr, cost_b=summonb, cost_g=summong,
                         skill_1=skill1, skill_2=skill2, skill_3=skill3,
                         movestyle=movestyle, movelimit=movelimit)


class TestCreatureAlpha(card.CreatureCard):
    # This is test creature alpha, so its ID is A for now.
    ID = 0x0000A

    def __init__(self):
        self.ID = 0x0000A
        name = "Alpha"
        icon = "🐻"
        image = "https://media.discordapp.net/attachments/780514923075469313/783759517070131200/default.png"
        type = ""
        hp = 5
        speed = 20

        # The summoning cost of this creature
        summonr = 2
        summonb = 2
        summong = 2

        # These are the creature's skills
        skill1 = MultiAttack(name="Multi Attacks", trigger="command", target=(
            "Rectilinear", "Enemy", "x3"), type="attack", cooldown=1, fp_cost=0, damage=3, attacks=3, damage_tag=DTags.Slash)
        skill2 = BasicShield(name="Shield", trigger="command", shield_amount=5, fp_cost=3, cooldown=4, target=("Rectilinear", "3", "Ally", "x3"))
        skill3 = BasicHeal(name="BasicHeal", trigger="command", target=("Any", "Ally", "x1"), type="support",
                           heal_amount=5, fp_cost=4)

        # This defines the creature's move style
        move_style = "STEP 1"
        movelimit = 1

        super().__init__(self.ID, name, icon, image=image, hp=hp, speed=speed, cost_r=summonr,
                         cost_b=summonb, cost_g=summong,
                         skill_1=skill1, skill_2=skill2, skill_3=skill3, movestyle=move_style, movelimit=movelimit)


class TestCreatureBeta(card.CreatureCard):
    # This is test creature beta, so its ID is B for now.
    ID = 0x0000B

    def __init__(self):
        self.ID = 0x0000B
        name = "Beta"
        icon = "🐻"
        image = "https://media.discordapp.net/attachments/780514923075469313/783759517070131200/default.png"
        type = ""
        hp = 15
        speed = 4

        # The summoning cost of this creature
        summonr = 3
        summonb = 3
        summong = 3

        # These are the creature's skills
        skill1 = MultiAttack(name="Multi Attacks", trigger="command", target=( "Rectilinear", "Enemy", "x3"),
         type="attack", cooldown=2, fp_cost=5, damage=4, attacks=3, damage_tag=DTags.Slash)
        skill2 = BasicShield(name="Super Shield.", trigger="command", target=(
            "Any", "Ally", "x1"), cooldown=1, fp_cost=8, description="description", shield_amount=8)
        skill3 = BasicHeal(name="Super Heal", trigger="command", target=(
            "Any", "Ally", "x1"), type="support", cooldown=5, fp_cost=10, heal_amount=9)

        # This defines the creature's move style
        move_style = "SAME COLUMN LIMIT 2"
        movelimit = 1

        super().__init__(self.ID, name, icon, image=image, hp=hp, speed=speed, cost_r=summonr,
                         cost_b=summonb, cost_g=summong,
                         skill_1=skill1, skill_2=skill2, skill_3=skill3, movestyle=move_style, movelimit=movelimit)


class TestCreatureDelta(card.CreatureCard):
    # This is test creature delta, so its ID is D for now.
    ID = 0x0000D

    def __init__(self):
        self.ID = 0x0000D
        name = "Delta"
        icon = "🐻"
        image = "https://media.discordapp.net/attachments/780514923075469313/783759517070131200/default.png"
        type = ""
        hp = 9
        speed = 8

        # The summoning cost of this creature
        summonr = 1
        summonb = 2
        summong = 1

        # These are the creature's skills
        skill1 = BasicAttack(name="Bash", trigger="command", target=("Adjacent", "Enemy", "x1"),
            type="type", cooldown=1, fp_cost=0, damage=5)
        skill2 = BasicShield(name="Shield", trigger="command", target=(
            "Any", "Ally", "x1"), cooldown=1, fp_cost=3, shield_amount=5)
        skill3 = BasicHeal(name="BasicHeal", trigger="command", target=(
            "Any", "Ally", "x1"), type="support", cooldown=3, fp_cost=0, description="description", heal_amount=4)

        # This defines the creature's move style
        move_style = "SAME DIAGONAL LIMIT 2"
        movelimit = 1

        super().__init__(self.ID, name, icon, image=image, hp=hp, speed=speed, cost_r=summonr,
                         cost_b=summonb, cost_g=summong,
                         skill_1=skill1, skill_2=skill2, skill_3=skill3, movestyle=move_style, movelimit=movelimit)


class TestCreature2(card.CreatureCard):
    # This is test creature 2, so its ID is 2 for now.
    ID = 0x00002

    def __init__(self):
        self.ID = 0x00002
        name = "Creature2"
        icon = "🐻"
        image = "https://media.discordapp.net/attachments/780514923075469313/783759517070131200/default.png"
        type = ""
        hp = 7
        speed = 9

        # The summoning cost of this creature
        summonr = 2
        summonb = 4
        summong = 1

        # These are the creature's skills
        skill1 = BasicAttack(name="Bash", trigger="command", target=("Adjacent", "Enemy", "x1"), type="attack",
                             cooldown=1, damage=6)
        skill2 = BasicShield(name="Shield", trigger="command", target=("Any", "Ally", "x1"),
                             type="passive",  shield_amount=8)
        skill3 = BasicHeal(name="BasicHeal", trigger="command", target=("Any", "Ally", "x1"),
                           heal_amount=2)

        # This defines the creature's move style
        move_style = "STEP 2"
        movelimit = 1

        super().__init__(self.ID, name, icon, image=image, hp=hp, speed=speed, cost_r=summonr,
                         cost_b=summonb, cost_g=summong,
                         skill_1=skill1, skill_2=skill2, skill_3=skill3, movestyle=move_style, movelimit=movelimit)


class TestCreature3(card.CreatureCard):
    # This is test creature 3, so its ID is 3 for now.
    ID = 0x00003

    def __init__(self):
        self.ID = 0x00003
        name = "creature 3"
        icon = "🐻"
        image = "https://media.discordapp.net/attachments/780514923075469313/783759517070131200/default.png"
        type = ""
        hp = 9
        speed = 8

        # The summoning cost of this creature
        summonr = 3
        summonb = 2
        summong = 3

        # These are the creature's skills
        skill1 = BasicAttack(name="Firebrand", trigger="command", target=("Adjacent", "Enemy", "x1"),
            type="attack", cooldown=1, fp_cost=0,  description="deal damage", damage=8, damage_tag=DTags.Fire)

        skill2 = BoostAttack(name="Heat Up.", trigger="command", target=("Rectilinear", "Ally", "x1", "3"),
            type="buff", cooldown=4, boost_amount=8, boost_tag=DTags.Fire)
        skill3 = Warp(name="Warp")
         #type="support", cooldown=1, fp_cost=0, heal_amount=3)

        # This defines the creature's move style
        move_style = """STEP 2"""
        movelimit = 1

        super().__init__(self.ID, name, icon, image=image, hp=hp, speed=speed,
                         cost_r=summonr, cost_b=summonb, cost_g=summong,
                         skill_1=skill1, skill_2=skill2, skill_3=skill3, movestyle=move_style, movelimit=movelimit)


class TestCreature4(card.CreatureCard):
    ID = 0x00004

    def __init__(self):
        self.ID = 0x00004
        name = "creature 4"
        icon = "🐻"
        image = "https://media.discordapp.net/attachments/780514923075469313/783759517070131200/default.png"
        type = ""
        hp = 5
        speed = 4

        # The summoning cost of this creature
        summonr = 4
        summonb = 4
        summong = 4

        # These are the creature's skills
        skill1 = BasicAttack(name="Slash", trigger="command", target=("Adjacent", "Enemy", "x1"), type="attack", cooldown=1, fp_cost=0,
                             description="deal damage", damage=8, damage_tag=DTags.Slash)

        skill2 = BasicHeal(name="BasicHeal", trigger="command", target=("Any", "Ally", "x1"), type="support", cooldown=1, fp_cost=0, description="description",
                           heal_amount=2)
        skill3 = BoostAttack(name="Attack Boost", trigger="auto", target=("This", "Self", "x1"), type="other", cooldown=5, fp_cost=0,
                             description="", boost_amount=4, boost_tag=DTags.Slash)

        # This defines the creature's move style
        move_style = """STEP 2"""
        movelimit = 1

        super().__init__(self.ID, name, icon, image=image, hp=hp, speed=speed, cost_r=summonr,
                         cost_b=summonb, cost_g=summong,
                         skill_1=skill1, skill_2=skill2, skill_3=skill3, movestyle=move_style, movelimit=movelimit)


class Sharpshooter(card.CreatureCard):
    ID = 0x00005

    def __init__(self):
        self.ID = 0x00005
        name = "Sharpshooter"
        icon = "🐻"
        image = "https://media.discordapp.net/attachments/780514923075469313/783759517070131200/default.png"
        type = ""
        hp = 3
        speed = 21

        # The summoning cost of this creature
        summonr = 2
        summonb = 2
        summong = 5

        # These are the creature's skills
        skill1 = BasicAttack(name="Snipe", trigger="command", target=("Rectilinear", "Enemy", "x1", "4"), type="attack", cooldown=1, fp_cost=0,
                             description="deal damage", damage=8, damage_tag=DTags.Gun, effect_str="Ka-Click.  Bang!")

        skill2 = BasicAttack(name="Showdown", trigger="command", target=("Rectilinear", "Enemy", "x9", "4"), type="attack", cooldown=3, fp_cost=0,
                             description="deal damage to group.", damage=2, damage_tag=DTags.Gun)
        skill3 = BoostAttack(name="Attack Boost", trigger="auto", target=("This", "Self", "x1"), type="other", cooldown=1, fp_cost=0,
                             description="", boost_amount=1, boost_tag=DTags.Gun)

        # This defines the creature's move style
        move_style = """STEP 2"""
        movelimit = 1

        super().__init__(self.ID, name, icon, image=image, hp=hp, speed=speed,
                         cost_r=summonr, cost_b=summonb, cost_g=summong,
                         skill_1=skill1, skill_2=skill2, skill_3=skill3, movestyle=move_style, movelimit=movelimit)


class Spiney(card.CreatureCard):
    ID = 0x00006

    def __init__(self):
        self.ID = 0x00006
        name = "Spiney"
        icon = "🐻"
        image = "https://media.discordapp.net/attachments/780514923075469313/780515725365346354/Spiny_Artwork_-_New_Super_Mario_Bros.png"
        type = ""
        hp = 7
        speed = 2

        # The summoning cost of this creature
        summonr = 4
        summonb = 4
        summong = 2

        # These are the creature's skills
        skill1 = BasicAttack(name="Bash", trigger="command", target=("Rectilinear", "Enemy", "x1"), type="attack", cooldown=1, fp_cost=0,
                             description="deal damage", damage=1, damage_tag=DTags.Gun)
        skill2 = Spike(name="Spikes", trigger="auto", target=("This", "Self", "x1"), type="other", cooldown=1, fp_cost=0,
                       description="", damage_returned=4)
        skill3 = None

        # This defines the creature's move style
        move_style = """STEP 1"""
        movelimit = 1

        super().__init__(self.ID, name, icon, image=image, hp=hp, speed=speed, cost_r=summonr,
                         cost_b=summonb, cost_g=summong,
                         skill_1=skill1, skill_2=skill2, skill_3=skill3, movestyle=move_style, movelimit=movelimit)


class Seven(card.CreatureCard):
    ID = 0x00007

    def __init__(self):
        self.ID = 0x00007
        name = "Seven"
        icon = "🐻"
        image = ""
        type = ""
        hp = 7
        speed = 7

        # The summoning cost of this creature
        summonr = 1
        summonb = 5
        summong = 2

        # These are the creature's skills
        skill1 = BasicAttack(name="Chill", trigger="command", target=("Rectilinear", "Enemy", "x1"),
            type="attack", cooldown=1, fp_cost=0, damage=5, damage_tag=DTags.Ice)
        skill2 = FreezeAttack(name="Freeze", target=("Rectilinear", "3", "Enemy", "x1"),
            cooldown=3, fp_cost=3, damage=3, time_frozen=3)
        skill3 = None

        # This defines the creature's move style
        move_style = """SAME DIAGONAL LIMIT 2"""
        movelimit = 1

        super().__init__(self.ID, name, icon, image=image, hp=hp, speed=speed, cost_r=summonr,
                         cost_b=summonb, cost_g=summong,
                         skill_1=skill1, skill_2=skill2, skill_3=skill3, movestyle=move_style, movelimit=movelimit)

class Magnetism(card.CreatureCard):
    ID = 0x00015

    def __init__(self):
        self.ID = 0x00015
        name = "Magnetism Man"
        icon = "🐻"
        image = ""
        type = ""
        hp = 14
        speed = 13

        # The summoning cost of this creature
        summonr = 2
        summonb = 1
        summong = 0

        # These are the creature's skills
        skill1 = BasicAttack(name="Thunder", trigger="command", target=("Rectilinear", "Enemy", "x1", "5"),
            type="attack", cooldown=1, fp_cost=0, damage=5, damage_tag=DTags.Elec)
        skill2 = BoostAttack(name="Boost Attack", trigger="command", target=("Rectilinear", "3", "Ally", "x1"),
            cooldown=3, fp_cost=3, boost_amount=3)
        skill3 = BasicAttack(name="Magnets", trigger="command", target=("Rectilinear", "Enemy", "x1", "2"),
            type="attack", cooldown=1, fp_cost=0, damage=5, damage_tag=DTags.Mag)

        # This defines the creature's move style
        move_style = """STEP 2"""
        movelimit = 1

        super().__init__(self.ID, name, icon, image=image, hp=hp, speed=speed, cost_r=summonr,
                         cost_b=summonb, cost_g=summong,
                         skill_1=skill1, skill_2=skill2, skill_3=skill3, movestyle=move_style, movelimit=movelimit)
