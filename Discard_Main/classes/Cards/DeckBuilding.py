from .CardLibrary import cardcluster1
from .cardretrieval import *
from .card import *
import json

class Deck():

    def __init__(self, deck_name="Brand new deck", deck_description="Enter a description for this deck."):
        self.deck_name = deck_name
        self.deck_description = deck_description

        self.deck_cards = []

    #Setters and Getters
    def set_deck_name(self, deck_name):
        self.deck_name = deck_name

    def get_deck_name(self):
        return self.deck_name

    def get_shorthand_rep(self):
        returnString="[{}|{}]".format(self.deck_name, len(self.deck_cards))
        return returnString

    def set_deck_description(self, deck_description):
        self.deck_description = deck_description

    def get_deck_description(self):
        return self.deck_description

    def get_deck_cards(self):
        return self.deck_cards

    def update_customs(self, user_inv):
        #update a deck's card customs.
        #user_inv is the result returned by a userprofile's get_cards() funciton.
        for i in range(len(self.deck_cards)):
            #if (self.deck_cards[i]["card_id"] == card_id):
            key=self.deck_cards[i]["inv_key"]
            if(user_inv[key]["custom"]!=None):
                self.deck_cards[i]["custom"]=user_inv[key]["custom"]
            if (self.deck_cards[i]["inv_key"] == card_value["inv_key"]):
                return True
        return False

    def inDeck(self, card_value):
        #Check if the card_value is in the current deck

        #Note: Switch to matching based on the inv_key
        for i in range(len(self.deck_cards)):
            #if (self.deck_cards[i]["card_id"] == card_id):
            if (self.deck_cards[i]["inv_key"] == card_value["inv_key"]):
                return True
        return False

    def addToDeck(self, card_value):
        #Add card_id along with its custom_id (if available) to the deck
        #UPDATE: card_id is replaced with card_value.  It has to add from a user's inventory.
        self.deck_cards.append(card_value)

    def removeFromDeck(self, card_value):
        #Searches the deck for the card_id for removal and removes it
        #UPDATE: card_id is replaced with card_value.
        #UPDATE: WILL USE inv_key instead.
        #
        for i in range(len(self.deck_cards)):
            if (self.deck_cards[i]["inv_key"] == card_value["inv_key"]):
                del self.deck_cards[i]
                return

    def addListToDeck(self, cards):
        #[cards] is a list of inv_keys
        #Add a list of cards to the deck
        for i in cards:
            self.deck_cards.append(i)

    def removeListFromDeck(self, cards):
        #[cards] is a list of inv_keys
        #Searches the deck for all the cards corresponding to the list passed by the argument and remove them
        counter = 0
        for i in self.deck_cards:
            if (self.deck_cards[counter]["inv_key"] in cards):
                del self.deck_cards[counter]["inv_key"]
            counter = counter + 1

    def toJson(self):
        return json.dumps(self, default = lambda o: o.__dict__, sort_keys = True, indent = 4)
