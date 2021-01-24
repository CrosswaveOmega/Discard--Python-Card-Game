from .. import card
from ..EnumuratedTerms import *
from ..SkillLibrary.skillcluster import *


class Thunder(card.SpellCard):
    """docstring for TestCard."""
    ID = 0x00020  # • ID- The internal ID of the card.

    # All cards have this, and they should all be unique.
    # consists of a five digit hexadecimal number
    # Cards should be referenced by this ID, not their name.
    # (00000  to FFFFF, makes maximum of 1,048,576 cards.
    def __init__(self):
        self.ID = 0x00020  # • ID- The internal ID of the card.
        # All cards have this, and they should all be unique.
        # consists of a five digit hexadecimal number
        # Cards should be referenced by this ID, not their name.
        # (00000  to FFFFF, makes maximum of 1,048,576 cards.
        name = "Thunder"
        #image = "https://media.discordapp.net/attachments/780514923075469313/783759517070131200/default.png"
        type = "None"
        super().__init__(self.ID, name=name)
