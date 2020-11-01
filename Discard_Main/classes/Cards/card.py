import discord
import operator
import json
from discord.ext import commands, tasks
from discord.utils import find
from discord import Webhook, AsyncWebhookAdapter


from .CardLibrary.cardcluster1 import *
from ..main.target_maker import *


class CardBase():  #Wip.

    def __init__(self, ID, name, icon, type, image="https://media.discordapp.net/attachments/749673596514730055/772497364816101376/unknown.png"):
        self.ID=ID          #• ID- The internal ID of the card.
                            #All cards have this, and they should all be unique.
                            #consists of a five digit hexadecimal number
                            #Cards should be referenced by this ID, not their name.
                            #(00000  to FFFFF, makes maximum of 1,048,576 cards.
        self.name=name      #• Name- The name of the card.  Customizable by a user,
        self.icon=icon      #• Icon- A emoji that will represent this card, placed before.   Customizable by a user,<:thonkang:219069250692841473>
        self.image=image    #• Image- Background image the card displays.   Customizable by a user,
        self.type=type      #• Type- The type of card this is.
        self.custom= ""     #• Custom- Custom if applied to card

    def get_ID(self):
        return self.ID

    def get_name():
        return self.name

    def get_icon(self):
        return self.icon

    def get_type(self):
        return self.type

    def get_image(self):
        return self.image

    def __str__(self):
        return self.icon + "|" + self.name + "|" + self.type + "|"+ str(self.ID)

    def apply_custom(self, custom):
        """Change the set values found in custom."""
        print("Applying Custom")
        print(custom.image_url)
        self.custom=custom.ID
        if hasattr(custom, 'name'):
            self.name=custom.name
        if hasattr(custom, 'icon'):
            self.icon=custom.icon
        if hasattr(custom, 'image_url'):
            if(custom.image_url!=""):
                self.image=custom.image_url
        if hasattr(custom, 'type'):
            self.type=custom.type
    def to_DiscordEmbed(self):
        print("TBD")
"""
Skill Triggers
   • Command- Skill Is triggered on command.
   • Auto- Skill is triggered by some stimuli.

Skill Types
   • Action- Activated by the player, during the creatures turn.  Will usually END turn.
      ‣ Attack- This skill will do some kind of damage to an enemy/enemies, reducing their HP
      ‣ Support- This skill will have some kind of effect to the player's team
   • Ability- Activated by the player, during the creatures turn.  Will not end turn, but are toggleable.
   • Counter- Skill will activate when creature has been attacked.
   • Reaction- Skill will activate when criteria has been met.
   • TBD
"""

"""Target Format:
[Target Range] [Target Scope] [Target Amount] [Target Restrictions]
"""
class Skill():
    #This class is where every skill will decend from.
    def __init__(self, name="No name set.", trigger="command", target=("Adjacent", "Enemy", "x1"), type="tbd", limit="tbd", description="tbd"):
        print("tbd")
        self.name= name #The name of the skill
        self.trigger = trigger # How the skill will be activated.  Can be "command" or "auto"
        print(target)
        self.target_value = Args_To_Target(*target) #What the skill will target.  Split into Type, Distance, Scope, Amount, and Limit.  Stored as dictionary.
        self.type= type #The type of skill.
        self.limit= limit #When the skill can not be used.
        self.description= description # What the skill will say it does.

    def __str__(self):
        print("TBD.")
        return ""

    def make_target_string(self):
        target=self.target_value
        print(json.dumps(target))
        strin="{shape} range {dist}, {scope}, {amount}".format(shape=target["shape"], dist=target["dist"], scope= target["scope"], amount=target["amount"])
        return strin
    def get_text_tuple(self):
        trigger="B"
        if(self.trigger=='command'):
            trigger='8️⃣'
        elif(self.trigger=='auto'):
            trigger='✳️'


        type=self.type

        name=self.name
        target=self.make_target_string()
        desc=self.description
        print(type, name, target, desc)
        return trigger, type, name, target, desc

    def doSkill(self, user, target, game_ref):
        #What the skill will actually do.
        #user is the entity using the skill.
        #target is what the skill is being used on.
        #Game_ref is a refrence to the Card_Duel's helper class.
        #Use a dictionary.
        print("Fill this in.")

class CreatureCard(CardBase):
    """docstring for TestCard."""
    def __init__(self,  ID, name="Default Name", icon="Default_Icon", image="https://media.discordapp.net/attachments/749673596514730055/772497364816101376/unknown.png", \
    hp=0, speed=0, summoncost_r=0, summoncost_b=0, summoncost_g=0, \
    skill_1=None, skill_2=None, skill_3=None, \
    movestyle="", movelimit=1):
        self.ID=ID          #• ID- The internal ID of the card.
                            #All cards have this, and they should all be unique.
                            #consists of a five digit hexadecimal number
                            #Cards should be referenced by this ID, not their name.
                            #(00000  to FFFFF, makes maximum of 1,048,576 cards.
        # name="Test Name"
        # icon="<:thonkang:219069250692841473>"
        # image="NA"
        type="Creature"
        self.hp=hp
        self.speed=speed
        self.summoncost_r=summoncost_r
        self.summoncost_b=summoncost_b
        self.summoncost_g=summoncost_g

        self.skill_1=skill_1
        self.skill_2=skill_2
        self.skill_3=skill_3

        self.move_style=movestyle
        self.move_limit=movelimit
        super().__init__(self.ID,name, icon, type, image)

    def get_ID(self):
        return self.ID

    def get_name():
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

    def get_summoncost_r(self):
        return self.summoncost_r

    def get_summoncost_g(self):
        return self.summoncost_g

    def get_summoncost_b(self):
        return self.summoncost_b

    def get_skill_1(self):
        return self.skill_1

    def get_skill_2(self):
        return self.skill_2

    def get_skill_3(self):
        return self.skill_3

    def get_move_style(self):
        return self.move_style

    def get_move_limit(self):
        return self.move_limit

    def __str__(self):
        return self.icon + "|" + self.name + "|" + self.type + "|"+ self.hp + "|"+ self.speed + "|"+ str(self.ID)

    def to_DiscordEmbed(self):
        embed = discord.Embed(title="{icon} {card_name}".format(icon=self.icon, card_name=self.name), colour=discord.Colour(0x7289da), description="HP: <:_9:754494641105272842><:_9:754494641105272842> {hp}  \n ```OKAY SO THING IS, I MAY NEED TO FIND A WAY TO MAKE THIS DESCRIPTION WIDER.  WIIIIIIDER.  MAYBE.  IDK.  I'M TRYING TO STOP THE SKILLS FROM CLUSTERING NEXT TO EACH OTHER.```".format(hp=self.hp))
        print(self.image)
        embed.set_image(url="{imgurl}".format(imgurl=self.image))
        embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")

        #, icon_url="""https://media.discordapp.net/attachments/763800266855415838/771803875946528788/image.png"""
        embed.set_author(name="{CardType}".format(CardType=self.type))
        id_hex=format(self.ID, "05X")
        embed.set_footer(text="{card_id} - {custom_id}".format(card_id=id_hex, custom_id=self.custom))
        if(self.skill_1 != None):
            trigger, type, name, target, desc =  self.skill_1.get_text_tuple()
            embed.add_field(name="{trig}{skill_type}: {skill_name}".format(trig=trigger, skill_type=type, skill_name=name), value="***target: {target_string_format}***\n{description}".format(target_string_format=target, description=desc), inline=False)
        if(self.skill_2 != None):
            trigger, type, name, target, desc =  self.skill_2.get_text_tuple()
            embed.add_field(name="{trig}{skill_type}: {skill_name}".format(trig=trigger, skill_type=type, skill_name=name), value="***target: {target_string_format}***\n{description}".format(target_string_format=target, description=desc), inline=False)
        if(self.skill_3 != None):
            trigger, type, name, target, desc =  self.skill_3.get_text_tuple()
            embed.add_field(name="{trig}{skill_type}: {skill_name}".format(trig=trigger, skill_type=type, skill_name=name), value="***target: {target_string_format}***\n{description}".format(target_string_format=target, description=desc), inline=False)
        embed.add_field(name="Speed", value="{speed}".format(speed=self.speed), inline=True)
        embed.add_field(name="Move Style", value="⬜⬜🟦⬜⬜\n⬜🟦🟦🟦⬜\n🟦🟦🟩🟦🟦\n⬜🟦🟦🟦⬜\n⬜⬜🟦⬜⬜", inline=True)
        embed.add_field(name="Summon_Cost", value="Red= {Red}\nBlue = {Blue}\nGreen= {Green}".format(Red=self.summoncost_r,Blue=self.summoncost_b,Green=self.summoncost_g), inline=True)
        return embed
