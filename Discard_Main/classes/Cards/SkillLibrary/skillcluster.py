

from .. import card

class BasicAttack(card.Skill):#Custom Class
    def __init__(self, name="BasicAttacl", trigger="command", target=("Adjacent", "Enemy", "x1"), type="tbd", limit="tbd", description="none", damage=5, damage_tag=""): #there's probably a better way to do this.
        """Init"""
        self.damage=damage #Unique to this skill.
        self.danage_tag=damage_tag #for future functionality.  Just ignore it for now.
        super().__init__(name, trigger, target, type, limit, description)
    def doSkill(self, user, target, game_ref):
        #What the skill will actually do.
        #user is the entity using the skill.
        #target is a LIST what the skill is being used on.
        #Game_ref is a refrence to the Card_Duel's helper class.
        #Use a dictionary.

        warning("INCOMPLETE.")
        dictionary={}
        dictionary["user"]=user
        dictionary["target"]=target
        print("This skill should do "+str(self.damage)+ "Damage to everything in the target parameter.")
        print(self.damage)
        dictionary["damage"]=self.damage
        dictionary["tag"]=self.damage_tag
        for entity in dictionary["target"]:
            print("HERE, IT SHOULD CHECK FOR ANYTHING THAT WOULD effect the skill's activation.  CURRENTLY, IT IS NOT IMPLEMTED.")
            if True: #here, it would check for some kind of effect. for record.
                piece.add_damage(dictionary["damage"])
        print("OPERATION HAS BEEN DONE.")
