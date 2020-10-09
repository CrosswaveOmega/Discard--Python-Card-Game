from .main.grid import *
from .main.piece import *

#The main game.

class Card_Duel:
    """Where the game will be played."""
    def __init__(self):
        self.game_id=0
        self.val=0
        self.players=[]
        self.entity_list=[]
        self.grid=Grid(5,5, self)
    def add_piece(self, piece):
        self.entity_list.append(piece)
    def move_piece(self, piece):
        piece.get_move_options(self.grid)


#Driver Code.
if __name__ == "__main__":
    duel=Card_Duel()

    testPiece=Piece("LO", "MY_NAME", 5,5, "MOVE?", "B1")
    testPiece2=Piece("LOE", "OTHER", 5,5, "MOVE?", "D1")
    testPiece3=Piece("LOE", "OTHER5", 5,5, "MOVE?", "A2")
    duel.add_piece(testPiece)
    duel.add_piece(testPiece2)
    duel.add_piece(testPiece3)
    print(testPiece.position.x_y())
    duel.grid.print_grid()
    duel.grid.print_grid("south")
    duel.move_piece(testPiece)
    testPiece.change_position("C2")
    duel.grid.print_grid()
    duel.grid.print_grid("south")
    duel.move_piece(testPiece)
