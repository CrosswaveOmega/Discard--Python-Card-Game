#from .classes.main import *
from classes.main import *
#The main game.

class Card_Duel:
    """Where the game will be played."""
    def __init__(self):
        self.game_id=0
        self.val=0
        self.players=[]
        self.entity_list=[]

        self.duel_helper=Card_Duel_Helper(self)
        self.grid=Grid(5,5, self.duel_helper)
    def add_piece(self, piece):
        self.entity_list.append(piece)
    def move_piece(self, piece):
        piece.get_move_options(self.grid)

class Card_Duel_Helper():
    #This class will help with processing game events game.
    def __init__(self, Duel):
        print("TBD.  Might do something.")
        self.__card_duel=Duel
    def get_entity_list(self):
        new_list=[]
        for v in self.__card_duel.entity_list:
            new_list.append(v)
        return new_list
#Driver Code.
if __name__ == "__main__":
    duel=Card_Duel()

    testPiece=Piece("LO", "MY_NAME", 5,5, "MOVE?", "B1")
    testPiece2=Piece("LOE", "OTHER", 5,5, "MOVE?", "D3")
    # testPiece3=Piece("LOE", "OTHER5", 5,5, "MOVE?", "A2")
    #
    # duel.add_piece(testPiece2)
    # duel.add_piece(testPiece3)
    # print(testPiece.position.x_y())
    # duel.grid.print_grid()
    # duel.grid.print_grid("south")
    duel.add_piece(testPiece)
    testPiece.change_position("C3")
    duel.move_piece(testPiece)

    duel.grid.print_grid()
    duel.add_piece(testPiece2)
    duel.move_piece(testPiece)

    duel.grid.print_grid()
    # duel.grid.print_grid("south")
    # duel.move_piece(testPiece)
