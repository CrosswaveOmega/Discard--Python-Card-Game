from ..DiscordPlayerInputOutputSystem import *
#The player class.  FOR THE GAME.
class Player:
    def __init__(self, player_type="", deck=[], team=1):
        self.PlayerType=player_type
        self.id="" #I don't know why we have this one.
        self.deck=deck #Should be a list of cards. Initalization prior might be useful.
        self.hand=[] #Cards in hand.
        self.graveyard=[]#All cards in the graveyard.
        self.team=team#The team the player is on.
        #Initialize any other gameplay variables here as we need them.
    def get_input(self):
        return "TBD"
    def get_output(self):
        #Ask for infomation here.
        print("TBD")
    #Se

class DiscordPlayer(Player):

    def __init__(self, deck, team):
        player_type="Discord"
        self.id=1234
        super().__init__(player_type="Discord", deck=deck, team=team)
    #Se
