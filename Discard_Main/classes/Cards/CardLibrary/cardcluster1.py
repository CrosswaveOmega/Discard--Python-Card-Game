
from .. import card

class TestCard(card.CardBase):
    """docstring for TestCard."""
    ID=0x000FF          #• ID- The internal ID of the card.
                    #All cards have this, and they should all be unique.
                    #consists of a five digit hexadecimal number
                    #Cards should be referenced by this ID, not their name.
                    #(00000  to FFFFF, makes maximum of 1,048,576 cards.
    def __init__(self):
        self.ID=0x000FF          #• ID- The internal ID of the card.
                            #All cards have this, and they should all be unique.
                            #consists of a five digit hexadecimal number
                            #Cards should be referenced by this ID, not their name.
                            #(00000  to FFFFF, makes maximum of 1,048,576 cards.
        name="Test Name"
        icon="<:thonkang:219069250692841473>"
        image="NA"
        type="None"
        super().__init__(self.ID,name, icon, type, image)


class TestCard2(card.CardBase):
    """docstring for TestCard."""
    ID=0x0000F          #• ID- The internal ID of the card.
                    #All cards have this, and they should all be unique.
                    #consists of a five digit hexadecimal number
                    #Cards should be referenced by this ID, not their name.
                    #(00000  to FFFFF, makes maximum of 1,048,576 cards.
    def __init__(self):
        self.ID=0x0000F          #• ID- The internal ID of the card.
                            #All cards have this, and they should all be unique.
                            #consists of a five digit hexadecimal number
                            #Cards should be referenced by this ID, not their name.
                            #(00000  to FFFFF, makes maximum of 1,048,576 cards.
        name="Test Name 2"
        icon="<:thonkang:219069250692841473>"
        image="NA"
        type="None"
        super().__init__(self.ID,name, icon, type, image)
