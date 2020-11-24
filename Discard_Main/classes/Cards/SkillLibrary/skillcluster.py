from .. import card
import aiohttp
import asyncio


# BasicAttack is an attack that can be done on adjacent enemies.
# It inflicts damage on a target, which diminishes that targets HP.

class BasicAttack(card.Skill):  # Custom Class

    def __init__(self, name="BasicAttacl", trigger="command", target=("Adjacent", "Enemy", "x1"), type="attack",
                 limit="tbd", description="", damage=5, damage_tag=""):  # there's probably a better way to do this.

        self.damage = damage  # Unique to this skill.
        # for future functionality.  Just ignore it for now.
        self.damage_tag = damage_tag
        super().__init__(name, trigger, target, type, limit, description)

    def get_description(self):
        return "Deal {damage} {tag} damage to target.".format(damage=self.damage, tag=self.damage_tag)

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
        dictionary["type"] = 'attack'
        print('before')

        dictionary["damage"] = self.damage
        dictionary["tag"] = self.damage_tag

        statement="{} uses {}!".format(user.get_name(), self.get_name())
        await game_ref.send_announcement(statement)
        dictionary = await user.check_effects('before', 'as_user', dictionary, game_ref)

        print('during')
        for entity in dictionary["target"]:

            dictionary["incoming_damage"] = dictionary["damage"]
            dictionary["range_to"]=user.compute_distance_to(entity.get_position())
            dictionary["continue"] = True
            dictionary = await entity.check_effects('during', 'as_target', dictionary, game_ref)

            if dictionary["continue"]:  # here, it would check for some kind of effect. for record.
                to_send="{} suffers damage of {}!".format(entity.get_name(),dictionary["incoming_damage"])
                await game_ref.send_announcement(to_send)
                entity.add_damage(dictionary["incoming_damage"])
        print('after')


# BasicHeal is a skill which replaces lost HP on a game piece.
# It can only replace lost HP, if the target of the heal has lost any.
# BasicHeal cannot be used to buff a target beyond its assigned HP.
class BasicHeal(card.Skill):

    def __init__(self, name="BasicHeal", trigger="command", target=("Any", "Ally", "x1"), type="support", limit="",
                 description="", heal_amount=1):
        self.heal_amount = heal_amount

        super().__init__(name, trigger, target, type, limit, description)

    def get_description(self):
        return "Heal {heal_amount} hp to target.".format(heal_amount=self.heal_amount)

    async def doSkill(self, user, target, game_ref):

        heal_dict = {}
        heal_dict["user"] = user
        heal_dict["target"] = target
        heal_dict["type"] = 'support'
        heal_dict["heal_amount"] = self.heal_amount
        print("The target piece can be healed by " +
              str(self.heal_amount) + " at most.")
        for entity in heal_dict["target"]:
            heal_dict["continue"] = True
            if heal_dict["continue"]:  # here, it would check for some kind of effect. for record.
                await game_ref.send_announcement(
                    "The " + entity.get_name() + " piece was healed by " + str(self.heal_amount) + ".")
                entity.heal_damage(heal_dict["heal_amount"])


# This class gives certain creatures the ability to diminish the amount of damage they receive from an attack.
# BasicShield can shield a creature from different types of attacks which the creature might have better defence against
# It is of type other because its effective area is not relevant to the board.
class BasicShield(card.Skill):
    def __init__(self, name="BasicShield", trigger="auto", target=("This", "Self", "x1"), type="other", limit="",
                 description="", shield_amount=1):
        # This is the amount of damage reduced from the attack when the shield is activated.
        self.shield_amount = shield_amount
        super().__init__(name, trigger, target, type, limit, description)

    def get_description(self):
        return "Applies a shield effect that will reduce incoming damage by {shield}.".format(shield=self.shield_amount)

    async def doSkill(self, user, target, game_ref):
        shield_dict = {}
        shield_dict["user"] = user
        shield_dict["target"] = target
        shield_dict["type"] = 'other'
        shield_dict["shield_amount"] = self.shield_amount
        print("The amount of damage that can be shielded by this skill is: " +
              str(self.shield_amount))
        print("Okay normally, this skill should reduce incoming damage.")
        print("It will do this with a effect.")

        async def shield_effect(dictionary, game_ref, aug):
            if dictionary["type"] == 'attack':
                if "incoming_damage" in dictionary:
                    dictionary["incoming_damage"] = dictionary["incoming_damage"] - aug
                    if dictionary["incoming_damage"] < 0:
                        dictionary["incoming_damage"] = 0
                    output = "Shield activated!  Damage reduced by {}...".format(
                        aug)
                    await game_ref.send_announcement(output)
            return dictionary

        output = "{} uses {}!".format(user.get_name(), self.get_name())
        await game_ref.send_announcement(output)

        for entity in shield_dict["target"]:
            output = "{} will take {} less damage!".format(
                entity.get_name(), str(shield_dict["shield_amount"]))
            await game_ref.send_announcement(output)
            entity.add_effect(self.get_name(), 'during', 'as_target',
                              shield_effect, shield_dict["shield_amount"], 'times_used', 1, 4)


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

    def get_description(self):
        return "Deals {damage} {tag} damage to target {attacks} times.".format(damage=self.damage, tag=self.damage_tag,
                                                                               attacks=self.attacks)

    async def doSkill(self, user, target, game_ref):

        # This is the most basic version of the multi-stage attack.
        # It strikes three times, but this could easily be changed if necessary.
        dictionary = {}  # Initialization of dictionary
        dictionary["user"] = user
        dictionary["target"] = target
        dictionary["type"] = 'attack'
        print("before")

        dictionary["damage"] = self.damage
        dictionary["attacks"] = self.attacks
        dictionary["tag"] = self.damage_tag
        output = "{} uses {}!".format(user.get_name(), self.get_name())
        await game_ref.send_announcement(output)
        dictionary = await user.check_effects('before', 'as_user', dictionary, game_ref)

        print("during")
        output="Attacking {} times.".format(dictionary["attacks"])
        await game_ref.send_announcement(output)
        for entity in dictionary["target"]:
            print(
                "HERE, IT SHOULD CHECK FOR ANYTHING THAT WOULD effect the skill's activation.  CURRENTLY, IT IS NOT IMPLEMENTED.")
            #await game_ref.send_announcement(output)
            dictionary["incoming_attacks"] = dictionary["attacks"]
            dictionary["incoming_damage"] = dictionary["damage"]
            dictionary["range_to"]=user.compute_distance_to(entity.get_position())
            dictionary = await entity.check_effects('during', 'as_target', dictionary, game_ref)
            dictionary["continue"] = True
            if dictionary["continue"]:  # here, it would check for some kind of effect. for record.
                for count in range(0, dictionary["incoming_attacks"]):
                    # Deals damage attacks time
                    output="{} suffered damage of {}!".format(entity.get_name(), dictionary["incoming_damage"])
                    await game_ref.send_announcement(output)
                    entity.add_damage(dictionary["incoming_damage"])
        print("after")
        print("OPERATION HAS BEEN DONE.")


class BoostAttack(card.Skill):
    def __init__(self, name="BoostAttack", trigger="auto", target=("This", "Self", "x1"), type="other", limit="",
                 description="", boost_amount=1):
        #
        self.boost_amount = boost_amount
        super().__init__(name, trigger, target, type, limit, description)

    def get_description(self):
        return "Applies a buff effect that will increase outgoing damage by {boost}.".format(boost=self.boost_amount)

    async def doSkill(self, user, target, game_ref):
        boost_dict = {}
        boost_dict["user"] = user
        boost_dict["target"] = target
        boost_dict["type"] = 'other'
        boost_dict["boost_amount"] = self.boost_amount
        print("The amount of damage that an attack will be boosted by this skill is: " +
              str(self.boost_amount))
        print("Okay normally, this skill should increase outgoing damage.")
        print("It will do this with a effect.")

        async def boost_effect(dictionary, game_ref, boost):
            if dictionary["type"] == 'attack':
                if "damage" in dictionary:
                    dictionary["damage"] = dictionary["damage"] + boost
                    if dictionary["damage"] < 0:
                        dictionary["damage"] = 0
                    output = "Boost activated!  Damage increased by {}...".format(
                        boost)
                    await game_ref.send_announcement(output)
            return dictionary

        output = "{} uses {}!".format(user.get_name(), self.get_name())
        await game_ref.send_announcement(output)

        for entity in boost_dict["target"]:
            output = "{} will give {} more damage!".format(
                entity.get_name(), str(boost_dict["boost_amount"]))
            await game_ref.send_announcement(output)
            entity.add_effect(self.get_name(), 'before', 'as_user',
                              boost_effect, boost_dict["boost_amount"], 'times_used', 1, 4)

class Spike(card.Skill):
    def __init__(self, name="Spike", trigger="auto", target=("This", "Self", "x1"), type="other", limit="",
                 description="", damage_returned=3):
        #
        self.damage_returned = damage_returned
        super().__init__(name, trigger, target, type, limit, description)

    def get_description(self):
        return "Deal {} damage to any close range attacker.".format(self.damage_returned)

    async def doSkill(self, user, target, game_ref):
        spike_dictionary = {}
        spike_dictionary["user"] = user
        spike_dictionary["target"] = target
        spike_dictionary["type"] = 'other'
        spike_dictionary["damage_returned"] = self.damage_returned

        async def spike_attack(dictionary, game_ref, boost):
            #time: 'during'
            #context: 'as_target'
            if dictionary["type"] == 'attack':
                if dictionary["range_to"] in dictionary:
                    if dictionary["range_to"] <= 1:
                        #dictionary["damage"] = dictionary["damage"] + boost
                        dictionary["user"].add_damage(boost)
                        dictionary["continue"] = False
                        output = "Ouch, spike activated.  {} damage was returned instead.".format(
                            boost)
                        await game_ref.send_announcement(output)
            return dictionary

        output = "{} uses {}!".format(user.get_name(), self.get_name())
        await game_ref.send_announcement(output)

        for entity in spike_dictionary["target"]:
            #output = "{} will give {} more damage!".format(
            #    entity.get_name(), str(boost_dict["boost_amount"]))
            #await game_ref.send_announcement(output)
            entity.add_effect(self.get_name(), 'during', 'as_target',
                              spike_attack, spike_dictionary["boost_amount"], 'times_used', 3, 4)
