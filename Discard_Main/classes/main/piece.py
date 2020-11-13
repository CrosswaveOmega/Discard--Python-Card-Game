from .generic.position import Position

class Piece:
    """Base Class for Creature and Leader pieces
    # NOTE: Creatures and Leaders will be Classes decended from this.
    """

    def __init__(self, player, name, hp, speed, move_style, position, img=None):
        self.player=player #the player object this piece belongs to.
        self.name=name
        self.max_hp=hp
        self.damage=0
        #Current HP= max_hp - damage.
        self.speed=speed
        self.move_style=move_style #The multilined text
        self.move_limit=1
        #Speed is 1-100.
        self.position=Position(notation=position)
        self.position=position
        self.display_image=img
        current_options={}
    def generate_options(self):
        pass
    async def get_action(self):#Add other args accordingly.
        await asyncio.sleep(0.4)
        print(self.name)
        return None
    def get_move_options(self, grid): #Wip function.
        """supposed to split move style into list line by line."""
        lines=self.move_style.splitlines()
        move_options=[]
        for line in lines:
            move_options.extend(grid.get_all_movements_in_range(self.position, line))
        return move_options

    def get_hp(self):
        hp = self.max_hp - self.damage
        return hp
    def get_speed(self):
        return self.speed
    def add_damage(self, damage_add=0):

        self.damage=self.damage+ damage_add
        print("Add Damage is incomplete.")

    def change_position(self, new_position_notation):
        self.position=Position(notation=new_position_notation)
    #To Do- String Rep.  Rep will be Icon, Name, and Position

class Creature(Piece):
    """Creature class.  This is what all creatures will be summoned into."""
    def __init__(self):
        print("TBD")

class Leader(Piece):
    """Leader class.  This is the avatar of the players."""
    """Through the leader, the players will do most actions."""
    def __init__(self, player, name, position_notation):
        self.player=player #the player object this piece belongs to.
        self.name=name
        #Current HP= max_hp - damage.
        speed=50
        move_style="STEP 1" #The multilined text
        move_limit=1
        #Speed is 1-100.
        position=position_notation
        #Image is url
        super().__init__(player=player, name=name, hp=20, speed=speed, move_style=move_style, move_limit=1, position=position)
#Driver Code.
if __name__ == "__main__":
    print("MAIN.")
    #testPiece=Piece("LO", "MY_NAME", 5,5, "STEP 1", "B3")
    #print(testPiece.position.x_y())
