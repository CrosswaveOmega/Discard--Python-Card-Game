from .. import card



class BasicAttack(card.Skill):#Custom Class
    def __init__(self, name="BasicAttacl", trigger="command", target=("Adjacent", "Enemy", "x1"), type="tbd", limit="tbd", description="none", damage=5, damage_tag=""): #there's probably a better way to do this.


        self.damage=damage #Unique to this skill.
        self.danage_tag=damage_tag #for future functionality.  Just ignore it for now.
        super().__init__(name, trigger, target, type, limit, description)
    def doSkill(self, user, target, game_ref):
        #What the skill will actually do.
        #user is the entity using the skill.
        #target is a LIST what the skill is being used on.
        #Game_ref is a reference to the Card_Duel's helper class.
        #Use a dictionary.

        warning("INCOMPLETE.")
        dictionary={} #Initialization of dictionary
        dictionary["user"]=user
        dictionary["target"]=target
        print("This skill should do "+str(self.damage)+ "Damage to everything in the target parameter.")
        print(self.damage)

        dictionary["damage"]=self.damage
        dictionary["tag"]=self.damage_tag
        for entity in dictionary["target"]:
            print("HERE, IT SHOULD CHECK FOR ANYTHING THAT WOULD effect the skill's activation.  CURRENTLY, IT IS NOT IMPLEMENTED.")
            if True: #here, it would check for some kind of effect. for record.
                piece.add_damage(dictionary["damage"])
        print("OPERATION HAS BEEN DONE.")

# This class is for a basic healing skill for support types
class BasicHeal(card.Skill):
        def __init__(self, name = "BasicHeal", trigger = "command", target = ("Any", "Ally", "x1"), type = "support", limit = "", description = "", heal_amount = 1):
            super().__init__(name, trigger, target, type, limit, description)
            self.heal_amount = heal_amount
        def doSkill(self, user, target, game_ref):

            # This will replace HP to a piece IF that piece has had its HP decreased by an attack.
            # This is a basic healing skill, and can not buff a targeted ally, thus it will have no effect on a piece which has not lost any HP.
            # If the creature can be healed, it will be healed by the amount that this skill states, or to its max HP, whichever is less.
            heal_dict = {}
            heal_dict["user"] = user
            heal_dict["target"] = target
            heal_dict["heal_amount"] = self.heal_amount
            print("The target piece can be healed by "+str(self.heal_amount)+" at most.")
            # I assume that this skill will be able to call a function within the Piece class to add HP back to the creature being healed, similar to how damage is applied in BasicAttack.
            # I don't want to add to the Piece class because I don't know how these skills are being implemented on that level.

#This class gives certain creatures the ability to diminish the amount of damage they receive from an attack.
#The goal with this class was to be general in nature, so that other types of shielding skills can inherit its properties, and they can shield a creature from different types of attacks which the creature might have better defence against.
class BasicShield(card.Skill):
    def __init__(self, name = "BasicShield", trigger = "auto", target=("This","Ally", "x1"), type="ability", limit = "", description = "Reduce Damage From a incoming Attack by a set amount", shield_amount = 1):

        #This is the amount of damage reduced from the attack when the shield is activated.
        self.shield_amount = shield_amount
        super().__init__(name, trigger, target, type, limit, description)
    def doSkill(self, user, target, game_ref):
        # This is the most basic version of a shield, so it should be designed to block any type of attack by the amount given.
        shield_dict = {}
        shield_dict["user"] = user
        shield_dict["target"] = target
        shield_dict["shield_amount"] = self.shield_amount
        print("The amount of damage that can be shielded by this skill is: "+str(self.shield_amount))
        # I don't quite understand how automatic skills will be implemented, but this skill should be pretty straightforward anyway.
        # As damage is applied to a piece with a shield, if the damage can be diminished(based on the types of attacks the shield blocks), that damage is reduced and then applied to that piece.

# This class allows for attacks which are split into multiple parts
# The idea is that it might be used to attack multiple targets if desired as a part of one total attack sequence.
class MultiAttack(card.Skill):
    def __init__(self, name = "MultiAttack", trigger = "command", target = ("Rectilinear", "Enemy", "x3"), type = "attack", limit = "", description = "", damage = 1, attacks=3, damage_tag=""):

        # This is the amount of damage each single attack will do
        # This damage value will occur 3 times during the duration of the MultiAttack
        self.attacks=attacks
        self.damage = damage
        self.damage_tag = damage_tag
        super().__init__(name, trigger, target, type, limit, description)
    def doSKill(self, user, target, game_ref):

        # This is the most basic version of the multi-stage attack. It strikes three times, but this could easily be changed if necessary.
        # This skill can use some of the functionality of BasicAttack to attack multiple targets, or possibly the same target multiple times.
        # I do not understand how targeting specific enemies works, but this would be the key distinction between a BasicAttack and a MultiAttack.
        # MultiAttack would need to be capable of targeting multiple pieces on the board.
        warning("INCOMPLETE.")
        dictionary={} #Initialization of dictionary
        dictionary["user"]=user
        dictionary["target"]=target
        print("This skill should do "+str(self.damage)+ "Damage to everything in the target parameter.")
        print(self.damage)

        dictionary["damage"]=self.damage
        dictionary["attacks"]=self.damage
        dictionary["tag"]=self.damage_tag
        for entity in dictionary["target"]:
            print("HERE, IT SHOULD CHECK FOR ANYTHING THAT WOULD effect the skill's activation.  CURRENTLY, IT IS NOT IMPLEMENTED.")
            if True: #here, it would check for some kind of effect. for record.
                for count in range(0, dictionary["attacks"]):
                    piece.add_damage(dictionary["damage"]) #Deals damage attacks times
        print("OPERATION HAS BEEN DONE.")
