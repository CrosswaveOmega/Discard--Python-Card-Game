from string import ascii_lowercase
import re

LETTERS = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10, 'K': 11, 'L': 12, 'M': 13,
           'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18, 'S': 19, 'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25,
           'Z': 26}
NUMBERS = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I', 10: 'J', 11: 'K', 12: 'L', 13: 'M',
           14: 'N', 15: 'O', 16: 'P', 17: 'Q', 18: 'R', 19: 'S', 20: 'T', 21: 'U', 22: 'V', 23: 'W', 24: 'X', 25: 'Y',
           26: 'Z'}


def space_notation_to_value_list(text):
    '''Converts a SINGLE space notation (A1, C2, D5, etc) into a tuple containing the column and row.'''
    split = text.split()
    res = []
    for tex in split:
        col, row = space_notation_to_value(tex)
        res.append((col, row))
    return res


def space_notation_to_value(notation):
    '''Converts a SINGLE space notation (A1, C2, D5, etc) into a tuple containing the column and row.'''
    tex = notation.upper()
    rows = re.findall(r'\d+', tex)
    columns = [LETTERS[character] for character in tex if character in LETTERS]
    column, row = int(columns[0]), int(rows[0])
    return column, row


def get_letter(number):
    return NUMBERS[number]


def to_notation(column, row):
    letter = NUMBERS[column]
    return "" + letter + str(row)


# Driver Code.
if __name__ == "__main__":
    print(space_notation_to_value_list('A0 B4'))
    print(space_notation_to_value('A2 A5'))
    print(space_notation_to_value('C3'))
    print(to_notation(4, 3))
