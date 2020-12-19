from .GameEvaluator import *

class Condition:
    def __init__(self, object="", property="", operator="",value=0, dictionary=None):
        self.numberof=1
        self.object=object #can be player game team _equal
        self.property=property
        self.operator=operator
        self.value=value
        if (dictionary !=None ):
            self.from_dictionary(dictionary)
        print("TBD")
    def evaluate_condition(self, to_find_from):
        if self.object=="game":
            return duel_evaluator(to_find_from, self.property, self.operator, self.value)
        elif self.object=="team":
            return False
        elif self.object=="player":
            return False
        return False
    def get_object(self):
        return self.object

    def from_dictionary(self, dictionary):
        for i, v in dictionary.items():
            if hasattr(self, i):
                setattr(self, i, v)
    def to_dictionary(self):
        dictionary = vars(self).copy()
        return dictionary




class Settings:
    def __init__(self, dictionary=None):
        # The columns and rows of the grid can be any value between 1-26, inclusive
        self.grid_columns = 6
        self.grid_rows = 5

        # What it takes to win, lose, and end the game
        # These conditions are a list
        self.win_condition = []
        self.lose_condition = []
        self.end_condition = [Condition("game", "active_teams", "<", 2)] #implimented

        # That amount of creatures that can be controlled by a player
        self.creature_limit = 5

        # The amount of creatures that can be summoned on the leader's turn
        self.creatures_summonable_per_turn = 1 #implimented

        # Whether summoning creatures will require card points
        self.card_point_summons = True #implimented

        # If True, the game will use the 3 flavor system
        # If False, the game will use the 1 flavor system
        self.card_point_flavors = True

        # If true, card points will be dropped onto the board at random points
        self.card_point_grid_drop = False

        self.requires_deck_size = False
        # How big each player's deck must be at the start of the game.
        # optional
        self.deck_size = 0

        # If True, the player will be eliminated upon decking out
        self.deck_out = False

    def from_dictionary(self, dictionary):
        for i, v in dictionary.items():
            if hasattr(self, i):
                if(i == "win_condition"):
                    self.win_condition=[]
                    for diction in v:
                        self.win_condition.append(Condition(dictionary=diction))
                elif(i == "lose_condition"):
                    self.lose_condition=[]
                    for diction in v:
                        self.lose_condition.append(Condition(dictionary=diction))
                elif(i == "end_condition"):
                    self.end_condition=[]
                    for diction in v:
                        self.end_condition.append(Condition(dictionary=diction))
                else:
                    setattr(self, i, v)
    def to_dictionary(self):
        dictionary = vars(self).copy()
        return dictionary

    def check_setting(self, setting):
        print(setting)
        if hasattr(self, setting):
            #print('found')
            #print(getattr(self, setting))
            return getattr(self, setting)
        return None

    def set_grid_columns(self, columns):
        self.grid_columns = columns

    def get_grid_columns(self):
        return self.grid_columns

    def set_grid_rows(self, rows):
        self.grid_rows = rows

    def get_grid_rows(self):
        return self.grid_rows

    def set_win_condition(self, win_cond):
        self.win_condition = win_cond

    def get_win_condition(self):
        return self.win_condition

    def set_lose_condition(self, lose_cond):
        self.lose_condition = lose_cond

    def get_lose_condition(self):
        return self.lose_condition

    def set_end_condition(self, end_cond):
        self.end_condition = end_cond

    def get_end_condition(self):
        return self.end_condition

    def set_creature_limit(self, creat_limit):
        self.creature_limit = creat_limit

    def get_creature_limit(self):
        return self.creature_limit

    def set_creatures_summonable_per_turn(self, cs_per_turn):
        self.creatures_summonable_per_turn = cs_per_turn

    def get_creatures_summonable_per_turn(self):
        return self.creatures_summonable_per_turn

    def set_card_point_summons(self, summons):
        self.card_point_summons = summons

    def get_card_point_summons(self):
        return self.card_point_summons

    def set_card_point_flavors(self, flavors):
        self.card_point_flavors = flavors

    def get_card_point_flavors(self):
        return self.card_point_flavors

    def set_card_point_drop(self, card_drop):
        self.card_point_grid_drop = card_drop

    def get_card_point_drop(self):
        return self.card_point_drop

    def set_requires_deck_size(self, requires_deck_size):
        self.requires_deck_size=requires_deck_size

    def set_deck_size(self, size):
        self.deck_size = size

    def get_deck_size(self):
        return self.deck_size

    def set_deck_out(self, deck_out):
        self.deck_out = deck_out

    def get_deck_out(self):
        return self.deck_out
