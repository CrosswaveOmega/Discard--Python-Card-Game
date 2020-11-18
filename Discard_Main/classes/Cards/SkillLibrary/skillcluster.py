from .. import card
import aiohttp
import asyncio


# BasicAttack is an attack that can be done on adjacent enemies.
# It inflicts damage on a target, which diminishes that targets HP.

class BasicAttack(card.Skill):  # Custom Class

    def __init__(self, name="BasicAttacl", trigger="command", target=("Adjacent", "Enemy", "x1"), type="tbd",
                 limit="tbd", description="none", damage=5, damage_tag=""):  # there's probably a better way to do this.

        self.damage = damage  # Unique to this skill.
        self.danage_tag = damage_tag  # for future functionality.  Just ignore it for now.
        super().__init__(name, trigger, target, type, limit, description)

    async def doSkill(self, user, target, game_ref):
        """
         What the skill will actually do.
         user is the entity using the skill.
         target is a LIST of entities the skill is being used on.
         game_ref is a reference to the Card_Duel's helper class.
         Use a dictionary."""

        print("INCOMPLETE.")
        dictionary = {}  # Initialization of dictionary
        dictionary["user"] = user
        dictionary["target"] = target
        print("This skill should do " + str(self.damage) + "Damage to everything in the target parameter.")
        print(self.damage)

        dictionary["damage"] = self.damage
        dictionary["tag"] = self.damage_tag

        for entity in dictionary["target"]:
            await game_ref.send_announcement(
                "{} uses {} on {} for {} damage.".format(user.get_name(), self.get_name(), entity.get_name(),
                                                         dictionary["damage"]))
            print(
                "HERE, IT SHOULD CHECK FOR ANYTHING THAT WOULD effect the skill's activation.  CURRENTLY, IT IS NOT IMPLEMENTED.")
            if True:  # here, it would check for some kind of effect. for record.
                entity.add_damage(dictionary["damage"])
        print("OPERATION HAS BEEN DONE.")


# BasicHeal is a skill which replaces lost HP on a game piece.
# It can only replace lost HP, if the target of the heal has lost any.
# BasicHeal cannot be used to buff a target beyond its assigned HP.
class BasicHeal(card.Skill):

    def __init__(self, name="BasicHeal", trigger="command", target=("Any", "Ally", "x1"), type="support", limit="",
                 description="", heal_amount=1):
        super().__init__(name, trigger, target, type, limit, description)
        self.heal_amount = heal_amount

    async def doSkill(self, user, target, game_ref):

        heal_dict = {}
        heal_dict["user"] = user
        heal_dict["target"] = target
        heal_dict["heal_amount"] = self.heal_amount
        print("The target piece can be healed by " + str(self.heal_amount) + " at most.")
        for entity in heal_dict["target"]:
            print(
                "HERE, IT SHOULD CHECK FOR ANYTHING THAT WOULD effect the skill's activation.  CURRENTLY, IT IS NOT IMPLEMENTED.")
            if True:  # here, it would check for some kind of effect. for record.
                await game_ref.send_announcement("The" +entity.get_name()+" piece can be healed by " + str(self.heal_amount) + " at most.")
                entity.heal_damage(dictionary["damage"])


# This class gives certain creatures the ability to diminish the amount of damage they receive from an attack.
# BasicShield can shield a creature from different types of attacks which the creature might have better defence against
# It is of type other because its effective area is not relevant to the board.
class BasicShield(card.Skill):
    def __init__(self, name="BasicShield", trigger="auto", target=("This", "Ally", "x1"), type="other", limit="",
                 description="Reduce Damage From a incoming Attack by a set amount", shield_amount=1):
        # This is the amount of damage reduced from the attack when the shield is activated.
        self.shield_amount = shield_amount
        super().__init__(name, trigger, target, type, limit, description)

    async def doSkill(self, user, target, game_ref):
        shield_dict = {}
        shield_dict["user"] = user
        shield_dict["target"] = target
        shield_dict["shield_amount"] = self.shield_amount
        print("The amount of damage that can be shielded by this skill is: " + str(self.shield_amount))
        print("Okay normally, this skill should reduce incoming damage.")
        print("It will do this with a effect.")


# This class allows for attacks which are split into multiple parts.
# It can be used to attack multiple targets if desired as a part of one total attack sequence.
# Each target is stored in a dictionary for look-up when dealing damage across each target.
class MultiAttack(card.Skill):
    def __init__(self, name="MultiAttack", trigger="command", target=("Rectilinear", "Enemy", "x3"), type="attack",
                 limit="", description="", damage=1, attacks=3, damage_tag=""):

        # This is the amount of damage each single attack will do
        # This damage value will occur 3 times during the duration of the MultiAttack
        self.attacks = attacks
        self.damage = damage
        self.damage_tag = damage_tag
        super().__init__(name, trigger, target, type, limit, description)

    async def doSkill(self, user, target, game_ref):

        # This is the most basic version of the multi-stage attack.
        # It strikes three times, but this could easily be changed if necessary.
        warning("INCOMPLETE.")
        dictionary = {}  # Initialization of dictionary
        dictionary["user"] = user
        dictionary["target"] = target
        print("This skill should do " + str(self.damage) + "Damage to everything in the target parameter.")
        print(self.damage)

        dictionary["damage"] = self.damage
        dictionary["attacks"] = self.damage
        dictionary["tag"] = self.damage_tag
        for entity in dictionary["target"]:
            output="{} uses {} on {}!  Dealing {} damage {} times!".format(user.get_name(), self.get_name(), entity.get_name(), dictionary["damage"], dictionary["attacks"])
            await game_ref.send_announcement(output)

            print(
                "HERE, IT SHOULD CHECK FOR ANYTHING THAT WOULD effect the skill's activation.  CURRENTLY, IT IS NOT IMPLEMENTED.")
            if True:  # here, it would check for some kind of effect. for record.
                for count in range(0, dictionary["attacks"]):
                    entity.add_damage(dictionary["damage"])  # Deals damage attacks times
        print("OPERATION HAS BEEN DONE.")
