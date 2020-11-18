class Condition:
    def __init__(self):
        condition_list = []
        print("TBD")


class Settings:
    def __init__(self):
        # The columns and rows of the grid can be any value between 1-26, inclusive
        self.grid_columns = 0
        self.grid_rows = 0

        # What it takes to win, lose, and end the game
        # These conditions are a list
        self.win_condition = []
        self.lose_condition = []
        self.end_condition = []

        # That amount of creatures that can be summoned by a player at one time
        self.creature_limit = 0

        # The amount of creatures that can be summoned on the leader's turn
        self.creatures_summonable_per_turn = 0

        # Whether summoning creatures will require card points
        self.card_point_summons = False

        # If True, the game will use the 3 flavor system
        # If False, the game will use the 1 flavor system
        self.card_point_flavors = False

        # If true, card points will be dropped onto the board at random points
        self.card_point_grid_drop = False

        # How big each player's deck must be at the start of the game
        self.deck_size = 0

        # If True, the player will be eliminated upon decking out
        self.deck_out = False

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

    def set_deck_size(self, size):
        self.deck_size = size

    def get_deck_size(self):
        return self.deck_size

    def set_deck_out(self, deck_out):
        self.deck_out = deck_out

    def get_deck_out(self):
        return self.deck_out
