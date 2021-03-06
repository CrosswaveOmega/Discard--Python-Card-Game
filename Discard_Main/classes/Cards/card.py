import discord
import operator
import json
import aiohttp
import asyncio
import re
from discord.ext import commands, tasks
from discord.utils import find
from discord import Webhook, AsyncWebhookAdapter

from .CardLibrary.cardcluster1 import *
from .EnumuratedTerms import *
from ..main.target_maker import *


class CardBase():  # Wip.

    def __init__(self, ID, name, icon, type,
                 image="https://media.discordapp.net/attachments/780514923075469313/783759517070131200/default.png"):
        self.ID = ID  # • ID- The internal ID of the card.
        # All cards have this, and they should all be unique.
        # consists of a five digit hexadecimal number
        # Cards should be referenced by this ID, not their name.
        # (00000  to FFFFF, makes maximum of 1,048,576 cards.
        self.name = name  # • Name- The name of the card.  Customizable by a user,
        self.icon = icon  # • Icon- A emoji that will represent this card, placed before.   Customizable by a user,<:thonkang:219069250692841473>
        self.image = image  # • Image- Background image the card displays.   Customizable by a user,
        self.type = type  # • Type- The type of card this is.
        self.custom = ""  # • Custom- Custom if applied to card

    def get_ID(self):
        return self.ID

    def get_name(self):
        return self.name

    def get_icon(self):
        return self.icon

    def get_type(self):
        return self.type

    def can_activate(self):
        return True

    def get_image(self):
        return self.image

    def get_ID(self):
        id_hex = format(self.ID, "05X")
        return id_hex

    def __str__(self):
        # r, b, g = self.make_compact_summon_cost()
        id_hex = format(self.ID, "05X")
        line1 = "{}|`{:20}`|`{}-{}`".format(self.icon,
                                            self.name, id_hex, self.custom)
        return line1
        # return self.icon + "|" + self.name + "|" + self.type + "|"+ str(self.ID)

    def apply_custom(self, custom):
        """Change the set values found in custom."""
        print("Applying Custom")
        if custom == None:
            print("...nevermind, there is no custom.")
            return None
        print(custom.image_url)
        self.custom = custom.ID
        if hasattr(custom, 'name'):
            self.name = custom.name
        if hasattr(custom, 'icon'):
            if (custom.icon != "none"):
                self.icon = custom.icon
        if hasattr(custom, 'image_url'):
            if (custom.image_url != "" or custom.image_url != "None"):
                self.image = custom.image_url
        #if hasattr(custom, 'type'):
        #    self.type = custom.type

    def to_DiscordEmbed(self):
        embed = discord.Embed(title="{icon} {card_name}".format(icon=self.icon, card_name=self.name),
              colour=discord.Colour(0x7289da),
              description="This card is invalid.")
        return embed


"""
Skill Triggers
   • Command- Skill Is triggered on command.
   • Auto- Skill is triggered by some stimuli.

Skill Types
   • Action- Activated by the player, during the creatures turn.  Will usually END turn.
      ‣ Attack- This skill will do some kind of damage to an enemy/enemies, reducing their HP
      ‣ Support- This skill will have some kind of effect to the player's team
   • Ailment- Inflicts a negative ailment on the target
   • Ability- Activated by the player, during the creatures turn.  Will not end turn, but are toggleable.
   • Counter- Skill will activate when creature has been attacked.
   • Reaction- Skill will activate when criteria has been met.
   • Passive- Skill is automatically active.
   • TBD

Skill Limit
  Factors that limit the activation of a skill.
  format: [limitType] [arg]
  1: cooldown.  Internal cooldown value, counts down by 1 every turn.
  2: FP: Requires the player's FP stat to be a certain amount.
"""

"""Target Format:
[Target Range] [Target Scope] [Target Amount] [Target Restrictions]
"""


class Skill():
    # This class is where every skill will decend from.
    def __init__(self, name="No name set.", trigger="command", target=("Adjacent", "Enemy", "x1"), type="tbd",
                 cooldown=1, fp_cost=0, description="tbd"):
        print("tbd")
        self.name = name  # The name of the skill
        self.trigger = trigger  # How the skill will be activated.  Can be "command" or "auto"
        print(target)
        self.target_value = Args_To_Target(
            *target)  # What the skill will target.  Split into Type, Distance, Scope, Amount, and Limit.  Stored as dictionary.
        self.type = type  # The type of skill.
        self.limit = ""  # When the skill can not be used.
        self.cooldown_var =  int(cooldown) #skill cooldown.
        self.fp_cost=int(fp_cost) #FP Cost, if applicable
        self.description = description  # What the skill will say it does.  THIS IS IMPORTATNT
        self.cooldown = 0 #Internal cooldown.


    def get_name(self):
        return self.name
    def get_FP_cost(self):
        return int(self.fp_cost)

    def get_trigger(self):
        return self.trigger

    def decrement_cooldown(self, mod=1):
        #subtract mod from cooldown
        self.cooldown= self.cooldown - mod
        if self.cooldown<=0:
            self.cooldown=0

    def can_use(self, fp=0):
        # Check if skill can be used.
        if self.cooldown==0 and fp>=self.get_FP_cost():
            return True
        return False


    def limit_act(self):
        self.cooldown=self.cooldown_var

    def __str__(self):
        print("TBD.")
        return ""

    def get_target_data(self):
        return self.target_value

    def get_description(self):
        return self.description

    def make_target_string(self):
        #for the representation on the card embed.
        target = self.target_value
        print(json.dumps(target))
        shape=target["shape"]
        dist=target["dist"]
        scope=target["scope"]
        amount=target["amount"]
        rang=""
        if(int(dist)>=2):
            rang= "range " +str(dist)
        strin = "{shape} {dist}, {scope}, {amount}".format(shape=shape, dist=rang, scope=scope, amount=amount)
        return strin

    def get_text_tuple(self):
        #for it's representation on the card.
        trigger = "B"
        if (self.trigger == 'command'):
            trigger = '🔘'
        elif (self.trigger == 'auto'):
            trigger = '✳️️'

        type = self.type

        name = self.name
        target = self.make_target_string()
        desc = self.get_description()
        fp=""
        cool=""
        print(type, name, target, desc)
        if self.get_FP_cost()>0:
            fp="FP: {}".format(self.get_FP_cost())
        if self.cooldown > 0:
            cool="Cooling Down: {} turns left".format(self.cooldown)
        elif self.cooldown_var >1:
            cool="Cooldown: {} turns.".format(self.cooldown_var)
        return trigger, type, name, target, desc, fp, cool

    async def doSkill(self, user, target, game_ref):
        # What the skill will actually do.
        # user is the entity using the skill.
        # target is what the skill is being used on.
        # Game_ref is a refrence to the Card_Duel's helper class.
        # Use a dictionary
        print("Fill this in.")
        dictionary = {}  # Initialization of dictionary
        dictionary["user"] = user
        dictionary["target"] = target
        dictionary["type"] = 'type of skill here'


        print('before')

        dictionary["unique attribute a"] = "a skill's unique attribute should go here."
        dictionary["unique attribute b"] = "Another unique attribute should go here"
        dictionary = await user.check_effects('before', 'as_user', dictionary, game_ref) #Apply before effects by user

        print('during')

        for entity in dictionary["target"]:
            await game_ref.send_announcement("{} uses {} on {} with effect {} and {}.".format(user.get_name(), self.get_name(), entity.get_name())) #announcement
            dictionary["unique attribute a incoming"] = dictionary["unique attribute a"]
            dictionary["continue"]=True
            dictionary = await entity.check_effects('during', 'as_target', dictionary, game_ref) #apply during effects by target
            if dictionary["continue"]:
                print("DO SOMETHING WITH 'entity' HERE!")

        print('after')

        dictionary = await user.check_effects('after', 'as_user', dictionary, game_ref) #apply after effects by user



class CreatureCard(CardBase):
    """docstring for TestCard."""

    def __init__(self, ID, name="Default Name", icon="🐻",
                 image="https://media.discordapp.net/attachments/749673596514730055/772497364816101376/unknown.png",
                 hp=0, speed=0, cost_r=0, cost_b=0, cost_g=0,
                 skill_1=None, skill_2=None, skill_3=None,
                 movestyle="", movelimit=1):
        self.ID = ID  # • ID- The internal ID of the card.
        # All cards have this, and they should all be unique.
        # consists of a five digit hexadecimal number
        # Cards should be referenced by this ID, not their name.
        # (00000  to FFFFF, makes maximum of 1,048,576 cards.
        # name="Test Name"
        # icon="<:thonkang:219069250692841473>"
        # image="NA"
        type = "Creature"
        self.hp = hp
        self.speed = speed
        self.cost_r = cost_r
        self.cost_b = cost_b
        self.cost_g = cost_g

        self.skill_1 = skill_1
        self.skill_2 = skill_2
        self.skill_3 = skill_3

        self.move_style = movestyle
        self.move_limit = movelimit
        super().__init__(self.ID, name, icon, type, image)

    def get_name(self):
        return self.name

    def get_icon(self):
        return self.icon

    def get_type(self):
        return self.type

    def get_image(self):
        return self.image

    def get_hp(self):
        return self.hp

    def get_speed(self):
        return self.speed

    def get_cost_r(self):
        return self.cost_r

    def get_cost_g(self):
        return self.cost_g

    def get_cost_b(self):
        return self.cost_b

    def get_cost_tuple(self):
        return self.cost_r, self.cost_b, self.cost_g

    def can_activate(self, source_r, source_b, source_g, source_u=0):
        r, b, g = self.get_cost_tuple()
        sum = r + b + g
        #if satisfied, d
        diff_r, diff_b, diff_g = max(r-source_r, 0), max(b-source_b, 0), max(g-source_g, 0)
        sum_remain = diff_r + diff_b + diff_g
        if ((source_r >= r) and (source_b >= b) and (source_g >= g)):
            return True
        if ((source_u >= sum_remain)): #universal cp.
            return True
        return False

    def get_skill_1(self):
        return self.skill_1

    def get_skill_2(self):
        return self.skill_2

    def get_skill_3(self):
        return self.skill_3

    def get_move_style(self):
        return self.move_style

    def make_compact_summon_cost(self):

        g_array = ["<:Summon_G_1:773564264823652393>",
                   "<:Summon_G_2:773564265286205450>",
                   "<:Summon_G_3:773564265079635999>",
                   "<:Summon_G_4:773564265252519986>",
                   "<:Summon_G_5:773564265226960896>",
                   "<:Summon_G_6:786615280272670760>",
                   "<:Summon_G_7:786615280288923659>",
                   "<:Summon_G_8:786615280427597914>",
                   "<:Summon_G_9:786615280481599528>"]

        r_array = ["<:Summon_R_1:773564265201139712>",
                   "<:Summon_R_2:773564265214115871>",
                   "<:Summon_R_3:773564265193799710>",
                   "<:Summon_R_4:773564264857862175>",
                   "<:Summon_R_5:773564265273622559>",
                   "<:Summon_R_6:786615280540319744>",
                   "<:Summon_R_7:786615280175677481>",
                   "<:Summon_R_8:786615280515547227>",
                   "<:Summon_R_9:786615280469278790>"]

        b_array = ["<:Summon_B_1:773564265117777960>",
                   "<:Summon_B_2:773564265131016203>",
                   "<:Summon_B_3:773564265230762024>",
                   "<:Summon_B_4:773564265202188388>",
                   "<:Summon_B_5:773564265184755712>",
                   "<:Summon_B_6:786615280146841633>",
                   "<:Summon_B_7:786615280058761227>",
                   "<:Summon_B_8:786615280259301376>",
                   "<:Summon_B_9:786615280234921984>"]

        red_res = "🔳"
        blue_res = "🔳"
        green_res = "🔳"
        if (self.cost_r > 0):
            red_res = r_array[self.cost_r - 1]
        if (self.cost_b > 0):
            blue_res = b_array[self.cost_b - 1]
        if (self.cost_g > 0):
            green_res = g_array[self.cost_g - 1]
        return red_res, blue_res, green_res

    def get_move_limit(self):
        return self.move_limit

    def get_shorthand_string(self):
        r, b, g = self.make_compact_summon_cost()
        id_hex = format(self.ID, "05X")
        custom = ""
        if (self.custom != ""):
            custom = "-`" + self.custom + "`"
        line1 = "[{}|`{}`|`HP:{}`|`SPD:{}`|`{}`{}]".format(self.icon, self.name, self.hp, self.speed, id_hex, custom)
        return line1
    def __str__(self):
        # '{:10}|'.format(item)
        r, b, g = self.make_compact_summon_cost()
        id_hex = self.get_ID()
        custom = ""
        if (self.custom != ""):
            custom = "-`" + self.custom + "`"
        line1 = "{}|`{:25}`|`HP:{:4}`|`SPD:{:3}`|{}{}{}|`{}`{}".format(self.icon, self.name, self.hp, self.speed, r, b,
                                                                        g, id_hex, custom)
        return line1
        # return self.icon + "|" + self.name + "|" + self.type + "|"+ self.hp + "|"+ self.speed + "|"+ str(self.ID)

    def to_DiscordEmbed(self, use_image=True):
        embed = discord.Embed(title="{icon} {card_name}".format(icon=self.icon, card_name=self.name),
                              colour=discord.Colour(0x7289da),
                              description="**HP:** {hp} \n **Speed:** {speed}".format(
                                  hp=self.hp, speed=self.speed))
        print("Image", self.image)
        if (self.image != None and self.image != "None"):
            if (use_image):
                embed.set_image(url="{imgurl}".format(imgurl=self.image))
            embed.set_thumbnail(url=self.image)

        # , icon_url="""https://media.discordapp.net/attachments/763800266855415838/771803875946528788/image.png"""
        # embed.set_author(name="{CardType}".format(CardType=self.type))
        id_hex = self.get_ID()
        embed.set_footer(
            text="Card Id:{card_id} - Custom ID:{custom_id}".format(card_id=id_hex, custom_id=self.custom))
        if (self.skill_1 != None):
            trigger, type, name, target, desc, fp, cool = self.skill_1.get_text_tuple()
            embed.add_field(
                name="{trig}{skill_type}: {skill_name}   {fp}".format(
                    trig=trigger, skill_type=type, skill_name=name, fp=fp),
                value="***target: {target_string_format}***\n{description}\n{cool}".format(target_string_format=target,
                                                                                   description=desc, cool=cool), inline=False)
        if (self.skill_2 != None):
            trigger, type, name, target, desc, fp, cool = self.skill_2.get_text_tuple()
            embed.add_field(
                name="{trig}{skill_type}: {skill_name}   {fp}".format(
                    trig=trigger, skill_type=type, skill_name=name, fp=fp),
                value="***target: {target_string_format}***\n{description}\n{cool}".format(target_string_format=target,
                                                                                   description=desc, cool=cool), inline=False)
        if (self.skill_3 != None):
            trigger, type, name, target, desc, fp, cool = self.skill_3.get_text_tuple()
            embed.add_field(
                name="{trig}{skill_type}: {skill_name}   {fp}".format(
                    trig=trigger, skill_type=type, skill_name=name, fp=fp),
                value="***target: {target_string_format}***\n{description}\n{cool}".format(target_string_format=target,
                                                                                   description=desc, cool=cool), inline=False)
        moveString = make_move_style_for_content(self.move_style)
        embed.add_field(name="Move Style", value=moveString, inline=True)
        embed.add_field(name="Summon Cost",
                        value="Red= {Red}\nBlue = {Blue}\nGreen= {Green}".format(Red=self.cost_r,
                                                                                 Blue=self.cost_b,
                                                                                 Green=self.cost_g), inline=True)
        return embed

class SpellCard(CardBase):

    def __init__(self, ID, name="Default Spell Name", icon="🎴",
                     image="https://media.discordapp.net/attachments/749673596514730055/772497364816101376/unknown.png",
                     subtype=None, fp_cost=0, cost_r=0, cost_b=0, cost_g=0, bp=10, set_time=0
                     ):
        self.ID = ID  # • ID- The internal ID of the card.
        # All cards have this, and they should all be unique.
        # consists of a five digit hexadecimal number
        # Cards should be referenced by this ID, not their name.
        # (00000  to FFFFF, makes maximum of 1,048,576 cards.
        # name="Test Name"
        # icon="<:thonkang:219069250692841473>"
        # image="NA"
        type = "Spell"
        self.spell_state=SpellState.Dormant
        self.fp_cost=fp_cost
        self.cost_r=cost_r
        self.cost_b=cost_b
        self.cost_g=cost_g
        self.base_bp=bp
        self.set_time=0

        super().__init__(self.ID, name, icon, type, image)

    def can_activate(self, user, game_ref=None):
        #user is source piece
        #by default, will use fp, r mana, b mana, and g mana
        return True
    def sub_spell_cost(self, user, game_ref=None):
        """decrement the spell activation cost here."""

    def can_set(self, user):
        return True
    def set_spell(self):
        self.spell_state=SpellState.Dormant
    async def set_effect(self, slot):
        """Do the set effect at the start of each turn."""
        #the set effect.
        print("TBD.")
    async def activate_spell(self, slot, user, game_ref=None):
        """Activate the spell card."""
        """Will return a SpellResult enum."""
        """user is the player's Leader piece."""

        return SpellResult.Finished
