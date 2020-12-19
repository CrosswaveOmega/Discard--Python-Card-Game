from .. import card
from ..EnumuratedTerms import *
import aiohttp
import asyncio

from ...main.effect import Effect


class GetCommonEffect():
    #for common effects, this does not Initialize anything/

    def ShieldData(self, exname="Shield", arg=1, arg2=DTags.Blunt, disable_cond='times_used', disable_arg=1, ico="🛡️"):
        #Decreases incoming damage.
        name=exname
        time="during"
        context="as_target"
        icon=ico
        async def effect_res(dictionary, game_ref, aug, aug2):
            if dictionary["type"] == 'attack':
                if "incoming_damage" in dictionary:
                    if "tag" in dictionary:
                        check=(aug2 == DCategory.Anything) or (dictonary["tag"] == aug2) or (dictionary["tag"].category()==aug2)
                        if check:
                            dictionary["incoming_damage"] = dictionary["incoming_damage"] - aug
                            if dictionary["incoming_damage"] < 0:
                                dictionary["incoming_damage"] = 0
                            output = "Shield activated!  Damage reduced by {}...".format(
                                aug)
                            await game_ref.send_announcement(output)
            return dictionary
        disable_condition=disable_cond
        description="Reduces incoming damage by {}.".format(disable_arg)
        return name, Effect(time, context, effect_res, arg, disable_condition, disable_arg, function_arg_2=arg2, level=4, description=description, icon=icon)

    def BoostData(self, exname="DamageBoost", arg=1,arg2=DCategory.Anything, disable_cond='times_used', disable_arg=1, ico="⚔️️"):
        #Increases damage of next few attack(s).
        name=exname
        time="before"
        context="as_user"
        icon=ico
        async def boost_effect(dictionary, game_ref, boost, tag=DCategory.Anything):
            if dictionary["type"] == 'attack':
                if "damage" in dictionary:
                    if "tag" in dictionary:
                        check=(tag == DCategory.Anything) or (dictionary["tag"] == tag) or (dictionary["tag"].category()==tag)
                        if check:
                            dictionary["damage"] = dictionary["damage"] + boost
                            if dictionary["damage"] < 0:
                                dictionary["damage"] = 0
                            output = "Damage boost augments damage by {}, for {} damage!".format(
                                boost, dictionary["damage"])
                            await game_ref.send_announcement(output)
            return dictionary
        disable_condition=disable_cond
        description="Reduces incoming damage by {}.".format(disable_arg)
        return name, Effect(time, context, boost_effect, arg, disable_condition, disable_arg, function_arg_2=arg2, level=4, description=description, icon=icon)

    def SpikeData(self, exname="Spike", arg=1, disable_arg=3):
        #Stops the piece from doing anything this turn
        name=exname
        time="during"
        context="as_target"
        icon="❇️"
        async def spike_attack(dictionary, game_ref, returned_damage, arg2=None):
            #time: 'during'
            #context: 'as_target'
            if dictionary["type"] == 'attack':
                if dictionary["range_to"] in dictionary:
                    if dictionary["range_to"] <= 1:
                        #dictionary["damage"] = dictionary["damage"] + boost
                        dictionary["user"].add_damage(returned_damage)
                        dictionary["continue"] = False
                        output = "Ouch, Spike activated.  {} damage was returned instead.".format(
                            returned_damage)
                        await game_ref.send_announcement(output)
            return dictionary
        disable_condition='times_used'
        description="negate any attack preformed at close range, and return {} damage to the attacker.".format(arg)
        return name, Effect(time, context, spike_attack, arg, disable_condition, disable_arg, level=3, description=description, icon="❄️")


    def FreezeData(self, arg=1, disable_arg=1):
        #Stops the piece from doing anything this turn
        name="Freeze"
        time="before"
        print("DISABLE ARG ",disable_arg)
        context="turn"
        icon="❄️"
        async def effect_res(dictionary, game_ref, arg, arg2=None):
            #dictionary should just contain user.
            if 'this_piece' in dictionary:
                piece=dictionary['this_piece']
                for key, value in piece.current_actions.items():
                    if key != "END":
                        piece.current_actions[key]=0
                await game_ref.send_announcement("Frozen!  Can't move.")
            else:
                await game_ref.send_announcement("error, did not set 'this_piece'...")
            return dictionary
        disable_condition='turns_passed'
        description="Frozen for {} turns.".format(disable_arg)
        return name, Effect(time, context, effect_res, arg, disable_condition, disable_arg, level=3, description=description, icon="❄️")
