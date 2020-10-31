from .CardLibrary import cardcluster1
from .cardretrieval import *
from .card import *

class Deck():

    def __init__(self, deck_name, deck_description):
        self.deck_name = deck_name
        self.deck_description = deck_description

        self.deck_cards = []

    def set_deck_name(self, deck_name):
        self.deck_name = deck_name

    def get_deck_name(self):
        return self.deck_name

    def set_deck_description(self, deck_description):
        self.deck_description = deck_description

    def get_deck_description(self):
        return self.deck_description

    def get_deck_cards(self):
        return self.deck_cards

    def get_card(self, card_id):
        return CardRetrievalClass().getByID(int(card_id, 16))

    def addToDeck(self, card_id):
        self.deck_cards.append({"card_id":card_id, "custom":None})

    def removeFromDeck(self, card_id):
        for i in range(len(self.deck_cards)):
            if self.deck_cards[i]["card_id"] == card_id:
                del self.deck_cards[i]
                break

    def addListToDeck(self, cards): #list of cards to add
        for i in cards:
            self.deck_cards.append(i)

    def removeListFromDeck(self, cards): #List of cards to remove
        return 
