
#The player class
class Player:
    def __init__(self, player_type=""):
        self.PlayerType=player_type
        self.id=1234
        self.deck=[] #Should be a stack of cards.
        self.hand=[] #Cards in hand.
        self.team=1#The team the player is on.
    #Se
