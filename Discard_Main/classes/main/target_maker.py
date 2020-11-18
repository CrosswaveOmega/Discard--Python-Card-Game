from .generic.notationhelp import space_notation_to_value, to_notation, get_letter
from .generic.position import Position
from .GridClass import Grid

import json

helpDictionary = {
    "shape": "Type of Range",
    "dist": "The Number of Spaces covered.",
    "scope": "The Scope of the target.",
    "amount": "The amount of entities within target.",
    "limit": ["Additional Conditions"]
}
optionsDictionary = {
    "shape": ["Cardinal", "Diagonal", "Omni", "Adjacent", "Rectilinear", "Row", "Column", "Any", "Other", "This"],
    "dist": "",  # jUST A NUMBER
    "scope": ["Enemy", "Ally", "Both", "Self", "Else"],
    "amount": ["Single", "x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9", "All"],
    "limit": ["None"]
}


def Args_To_Target(*args):
    new_dictionary = {
        "shape": "",  # required
        "dist": 1,
        "scope": "",  # required
        "amount": "",  # required
        "limit": [],  # optional
    }
    number_of_args = len(args)  # min is 3,
    # match based on universal list.
    shapematch = False
    distmatch = False
    scopematch = False
    amountmatch = False
    print(args)
    for element in args:
        print(element)
        if not shapematch:
            if (element in optionsDictionary["shape"]):
                new_dictionary["shape"] = element
                shapematch = True
        if not scopematch:
            if (element in optionsDictionary["scope"]):
                new_dictionary["scope"] = element
                scopematch = True
        if not amountmatch:
            if (element in optionsDictionary["amount"]):
                new_dictionary["amount"] = element
                amountmatch = True
        if not distmatch:
            stringvertotest = str(element)
            if (stringvertotest.isnumeric()):
                new_dictionary["dist"] = int(stringvertotest)
                distmatch = True
        if (element in optionsDictionary["limit"]):
            new_dictionary["limit"].append(element)
    return new_dictionary


def make_move_style_for_content(movestyle_str):
    def adjust_grid(grid_a, listiterate, emoji):
        for val in listiterate:
            x, y = Position(notation=val).x_y()
            grid_a[y - 1][x - 1] = emoji
        return grid_a

    lines = movestyle_str.splitlines()
    col = 5
    row = 5
    grid = Grid(row, col)
    position = Position(notation="C3")
    SameStyles = []
    HopStyles = []
    StepStyles = []
    for line in lines:
        moves = line.split(' ')
        print(moves)
        type = moves[0]
        list = []
        if type == 'SAME':  # type same
            # ['SAME', 'SCOPE', LIMIT, VALUE]
            SameStyles.extend(grid.get_same_movements(position, moves))
        if type == 'HOP':  # type same
            # ['HOP', 'SCOPE', 'VALUEA', 'SCOPEB', 'VALUEB']
            HopStyles.extend(grid.get_hop_movements(position, moves))
        if type == 'STEP':  # type same
            # ['SAME', 'SCOPE', LIMIT, VALUE]
            StepStyles.extend(grid.get_step_movements(position, moves))
    grid_array = []
    for i in range(col):
        column = []
        for j in range(row):
            column.append("⬜")
        grid_array.append(column)
    grid_array = adjust_grid(grid_array, SameStyles, "🟥")
    grid_array = adjust_grid(grid_array, HopStyles, "🟨")
    grid_array = adjust_grid(grid_array, StepStyles, "🟦")
    grid_array = adjust_grid(grid_array, ["C3"], "🟩")
    returnVal = ""
    for re in range(0, row):
        returnVal = returnVal + \
            (''.join(['{}'.format(item) for item in grid_array[re]])) + "\n"
    make_string = "```" + returnVal + "```"
    return make_string
