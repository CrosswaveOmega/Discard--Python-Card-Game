import enum


#I realized that it was getting way too easy to misspell some terms.
#so, I began to create enums to eventually replace some of the strings.
class DCategory(enum.Enum):
    """Short for Damage Category.  All the Types of damage there are."""
    Kinetic = 0
    Element = 1
    Polarity = 2
    Anything = 3
    def __str__(self):
        return '{}'.format(self.name)
    def category(self):
        if self.value == 3:
            return DCategory.Anything
        elif self.value==0:
            return DCategory.Kinetic
        elif self.value==1:
            return DCategory.Element
        elif self.value==2:
            return DCategory.Polarity


class DTags(enum.Enum):
    """Short for Damage Tags.  All the Types of damage there are."""
    Absolute = 0
    Blunt = 1
    Slash = 2
    Gun = 3
    Fire = 4
    Ice = 5
    Wind = 6
    Elec = 7
    Mag = 8
    PSI = 9
    Light = 10
    Dark = 11
    def __str__(self):
        return '{}'.format(self.name)
    def category(self):
        if self.value == 0:
            return DCategory.Anything
        elif self.value<=3:
            return DCategory.Kinetic
        elif  self.value<=9:
            return DCategory.Element
        elif self.value <= 11:
            return DCategory.Polarity
