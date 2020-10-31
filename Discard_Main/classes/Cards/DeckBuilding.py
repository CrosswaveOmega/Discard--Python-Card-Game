from .CardLibrary import cardcluster1
from .cardretrieval import *
from .card import *

class Deck():

    def __init__(self, deck_name, deck_description):
        self.deck_name = deck_name
        self.deck_description = deck_description

        self.deck_cards = []

    #Setters and Getters
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

    #def get_card(self, card_id):
        #return CardRetrievalClass().getByID(int(card_id, 16))

    def inDeck(self, card_id):
        #Check if the card_id is in the current deck
        for i in range(len(self.deck_cards)):
            if (self.deck_cards[i]["card_id"] == card_id):
                return True
        return False

    def addToDeck(self, card_id):
        #Add card_id along with its custom_id (if available) to the deck
        self.deck_cards.append({"card_id":card_id, "custom":None})

    def removeFromDeck(self, card_id):
        #Searches the deck for the card_id for removal and removes it
        for i in range(len(self.deck_cards)):
            if (self.deck_cards[i]["card_id"] == card_id):
                del self.deck_cards[i]
                return

    def addListToDeck(self, cards):
        #[cards] is a list of card_ids
        #Add a list of cards to the deck
        for i in cards:
            self.deck_cards.append(i)

    def removeListFromDeck(self, cards):
        #[cards] is a list of card_ids
        #Searches the deck for all the cards corresponding to the list passed by the argument and remove them
        counter = 0
        for i in self.deck_cards:
            if (self.deck_cards[counter]["card_id"] in cards):
                del self.deck_cards[counter]["card_id"]
            counter = counter + 1
