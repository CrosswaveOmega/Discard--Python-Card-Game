"""because we need a list of skills to make things easier."""

from .. import card

class BasicAttack(card.Skill):#Custom Class
    def __init__(self, name="BasicAttacl", trigger="command", target=("Adjacent", "Enemy", "x1"), type="tbd", limit="tbd", description="none", damage=5): #there's probably a better way to do this.
        self.damage=damage
        super().__init__(name, trigger, target, type, limit, description)
    def doSkill(self, user, target, game_ref):
        #What the skill will actually do.
        #user is the entity using the skill.
        #target is what the skill is being used on.
        #Game_ref is a refrence to the Card_Duel's helper class.
        #Use a dictionary.
        print("TBD")
