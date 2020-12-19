from .. import card
from ..EnumuratedTerms import *
from .effectcluster import GetCommonEffect
import aiohttp
import asyncio
import random

# BasicAttack is an attack that can be done on adjacent enemies.
# It inflicts damage on a target, which diminishes that targets HP.

class BasicAttack(card.Skill):  # Custom Class

    def __init__(self, name="BasicAttack", trigger="command", target=("Adjacent", "Enemy", "x1"),
                 type="attack", cooldown=1, fp_cost=0, description="", damage=5, damage_tag=DTags.Blunt, effect_str="Pow!"):  # there's probably a better way to do this.

        self.damage = damage  # Unique to this skill.
        # for future functionality.  Just ignore it for now.
        self.damage_tag = damage_tag
        self.effect_str=effect_str
        super().__init__(name, trigger, target, type, cooldown, fp_cost, description)

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
        dictionary["effect_str"]= self.effect_str

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
                await game_ref.send_announcement(dictionary["effect_str"])
                to_send="{} suffers damage of {}!".format(entity.get_name(),dictionary["incoming_damage"])
                await game_ref.send_announcement(to_send)
                entity.add_damage(dictionary["incoming_damage"])
        print('after')
        dictionary = await user.check_effects('after', 'as_user', dictionary, game_ref)


# BasicHeal is a skill which replaces lost HP on a game piece.
# It can only replace lost HP, if the target of the heal has lost any.
# BasicHeal cannot be used to buff a target beyond its assigned HP.
class BasicHeal(card.Skill):

    def __init__(self, name="BasicHeal", trigger="command", target=("Any", "Ally", "x1"),
                 type="support", cooldown=1, fp_cost=0, description="", heal_amount=1):
        self.heal_amount = heal_amount

        super().__init__(name, trigger, target, type, cooldown, fp_cost, description)

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
    def __init__(self, name="BasicShield", trigger="auto", target=("This", "Self", "x1"),
                 type="support", cooldown=1, fp_cost=0, description="", shield_amount=1, shield_tag=DCategory.Kinetic):
        # This is the amount of damage reduced from the attack when the shield is activated.
        self.shield_amount = shield_amount
        self.shield_tag= shield_tag
        super().__init__(name, trigger, target, type, cooldown, fp_cost, description)

    def get_description(self):
        return "Applies a shield effect that will reduce incoming {dtag} damage by {shield}.".format(dtag=self.shield_tag, shield=self.shield_amount)

    async def doSkill(self, user, target, game_ref):
        shield_dict = {}
        shield_dict["user"] = user
        shield_dict["target"] = target
        shield_dict["type"] = 'other'
        shield_dict["shield_amount"] = self.shield_amount
        shield_dict["shield_tag"] = self.shield_tag
        print("The amount of damage that can be shielded by this skill is: " +
              str(self.shield_amount))
        print("Okay normally, this skill should reduce incoming damage.")
        print("It will do this with a effect.")


        output = "{} uses {}!".format(user.get_name(), self.get_name())
        await game_ref.send_announcement(output)

        for entity in shield_dict["target"]:
            name, eff =GetCommonEffect().ShieldData(exname=self.get_name(), arg=shield_dict["shield_amount"], arg2=shield_dict["shield_tag"])
            entity.add_effect_direct(name, eff)
            output = "{} will take {} less damage!".format(
                entity.get_name(), str(shield_dict["shield_amount"]))
            await game_ref.send_announcement(output)



# This class allows for attacks which are split into multiple parts.
# It can be used to attack multiple targets if desired as a part of one total attack sequence.
# Each target is stored in a dictionary for look-up when dealing damage across each target.
class MultiAttack(card.Skill):
    def __init__(self, name="MultiAttack", trigger="command", target=("Rectilinear", "Enemy", "x3"),
                 type="attack", cooldown=1, fp_cost=0, description="",
                 damage=1, attacks=3, damage_tag=DTags.Blunt, effect_str="Pow, Blam, Kick!"):

        # This is the amount of damage each single attack will do
        # This damage value will occur 3 times during the duration of the MultiAttack
        self.attacks = attacks
        self.damage = damage
        self.damage_tag = damage_tag
        self.effect_str = effect_str
        super().__init__(name, trigger, target, type, cooldown, fp_cost, description)

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
        dictionary["effect_str"]= self.effect_str
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

            dictionary["continue"] = True
            for count in range(0, dictionary["incoming_attacks"]):
                dictionary = await entity.check_effects('during', 'as_target', dictionary, game_ref)
                if dictionary["continue"]:  # here, it would check for some kind of effect. for record.
                    # Deals damage attacks time
                    await game_ref.send_announcement(self.effect_str)
                    output="{} suffered damage of {}!".format(entity.get_name(), dictionary["incoming_damage"])
                    await game_ref.send_announcement(output)
                    entity.add_damage(dictionary["incoming_damage"])
        print("after")
        print("OPERATION HAS BEEN DONE.")


class BoostAttack(card.Skill):
    def __init__(self, name="BoostAttack", trigger="auto", target=("This", "Self", "x1"),
                type="buff", cooldown=1, fp_cost=0, description="", boost_amount=1, boost_tag=DCategory.Anything):
        #
        self.boost_amount = boost_amount
        self.boost_tag= boost_tag
        super().__init__(name, trigger, target, type, cooldown, fp_cost, description)

    def get_description(self):
        return "Applies a buff effect that will increase outgoing {tag} damage by {boost}.".format(tag=self.boost_tag, boost=self.boost_amount)

    async def doSkill(self, user, target, game_ref):
        boost_dict = {}
        boost_dict["user"] = user
        boost_dict["target"] = target
        boost_dict["type"] = 'other'
        boost_dict["boost_amount"] = self.boost_amount
        boost_dict["boost_tag"] = self.boost_tag
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
                    output = "Damage boost augments damage by {}, for {} damage!".format(
                        boost, dictionary["damage"])
                    await game_ref.send_announcement(output)
            return dictionary

        output = "{} uses {}!".format(user.get_name(), self.get_name())
        if self.trigger=="auto":
            output="{}'s Auto skill {} was activated!".format(user.get_name(), self.get_name())
        await game_ref.send_announcement(output)

        for entity in boost_dict["target"]:
            name, eff =GetCommonEffect().BoostData(arg=boost_dict["boost_amount"], arg2=boost_dict["boost_tag"])
            entity.add_effect_direct(name, eff)
            output = "{}'s next attack will be augmented by {}.".format(
                entity.get_name(), str(boost_dict["boost_amount"]))
            await game_ref.send_announcement(output)
            #entity.add_effect(self.get_name(), 'before', 'as_user',
            #                  boost_effect, boost_dict["boost_amount"], 'times_used', 1, 4)

class Spike(card.Skill):
    def __init__(self, name="Spike", trigger="auto", target=("This", "Self", "x1"),
                 type="counter", cooldown=1, fp_cost=0, description="", damage_returned=3):

        self.damage_returned = damage_returned

        super().__init__(name, trigger, target, type, cooldown, fp_cost, description)

    def get_description(self):
        return "Deal {} damage to any close range attacker.".format(self.damage_returned)

    async def doSkill(self, user, target, game_ref):
        spike_dictionary = {}
        spike_dictionary["user"] = user
        spike_dictionary["target"] = target
        spike_dictionary["type"] = 'other'
        spike_dictionary["damage_returned"] = self.damage_returned


        if self.trigger!="auto":
            output = "{} uses {}!".format(user.get_name(), self.get_name())
            await game_ref.send_announcement(output)

        for entity in spike_dictionary["target"]:
            name, eff =GetCommonEffect().SpikeData(arg=spike_dictionary["damage_returned"])
            entity.add_effect_direct(name, eff)



class FreezeAttack(card.Skill):
    def __init__(self, name="Freeze", trigger="command", target=("Adjacent", "Enemy", "x1"),
                 type="ailment_attack", cooldown=1, fp_cost=0, description="", damage=3, time_frozen=1):
        #
        self.damage = damage
        self.time_frozen = time_frozen
        self.effect_str = "Super Cool."
        super().__init__(name, trigger, target, type, cooldown, fp_cost, description)

    def get_description(self):
        return "Deal {} damage to any close range attacker, and freeze them for {} turns.".format(self.damage, self.time_frozen)

    async def doSkill(self, user, target, game_ref):
        dictionary = {}
        dictionary["user"] = user
        dictionary["target"] = target
        dictionary["type"] = 'attack'
        dictionary["effect_str"]= self.effect_str

        print('before')

        dictionary["damage"] = self.damage
        dictionary["time_frozen"] = self.time_frozen
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
                await game_ref.send_announcement(self.effect_str)
                to_send="{} suffers damage of {}!".format(entity.get_name(),dictionary["incoming_damage"])
                await game_ref.send_announcement(to_send)
                entity.add_damage(dictionary["incoming_damage"])

                name, eff =GetCommonEffect().FreezeData(arg=1, disable_arg=dictionary["time_frozen"])
                entity.add_effect_direct(name, eff)
                to_send="{} is now frozen for {} turns!".format(entity.get_name(),dictionary["incoming_damage"], dictionary["time_frozen"])
                await game_ref.send_announcement(to_send)
        print('after')
        dictionary = await user.check_effects('after', 'as_user', dictionary, game_ref)

class Warp(card.Skill):
    def __init__(self, name="Warp", trigger="command", target=("Adjacent", "Ally", "x1", "noself"),
                 type="support", cooldown=1, fp_cost=0, description="", distance=3):
        #
        self.distance = distance
        self.effect_str = "Warp!"
        super().__init__(name, trigger, target, type, cooldown, fp_cost, description)

    def get_description(self):
        return "Warp a entity to any unoccupied space a Rectilinear distance of {} away.".format(self.distance)

    async def doSkill(self, user, target, game_ref):
        dictionary = {}
        dictionary["user"] = user
        dictionary["target"] = target
        dictionary["type"] = self.type
        dictionary["effect_str"]= self.effect_str

        print('before')

        dictionary["distance"] = self.distance
        #dictionary["time_frozen"] = self.time_frozen
        statement="{} uses {}!".format(user.get_name(), self.get_name())
        await game_ref.send_announcement(statement)
        dictionary = await user.check_effects('before', 'as_user', dictionary, game_ref)

        print('during')
        for entity in dictionary["target"]:

            #dictionary["incoming_damage"] = dictionary["damage"]
            dictionary["range_to"]=user.compute_distance_to(entity.get_position())
            dictionary["continue"] = True
            dictionary = await entity.check_effects('during', 'as_target', dictionary, game_ref)
            warp_options=user.get_move_options(game_ref.get_grid(), "STEP {}".format(dictonary["distance"]))
            if(len(warp_options)==0):
                dictonary["continue"]= False

            if dictionary["continue"]:  # here, it would check for some kind of effect. for record.

                option = await user.player.select_option(move_options, prompt="Where would you like to teleport {} to?".format(entity.get_name()))
                if (option == "back" or option == "timeout" or option=="invalidmessage"):
                    option=random.choice(warp_options)
                entity.change_position(option)
                await game_ref.send_announcement(self.effect_str)
                to_send="{} has been teleported to postion {}.".format(entity.get_name(),option)
                await game_ref.send_announcement(to_send)
        dictionary = await user.check_effects('after', 'as_user', dictionary, game_ref)
