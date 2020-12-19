from .generic.notationhelp import space_notation_to_value, to_notation, get_letter
from .generic.position import Position

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
    "limit": ["noself"]
}
amount_dictionary = {
    "Single": 1,
    "x1": 1,
    "x2": 2,
    "x3": 3,
    "x4": 4,
    "x5": 5,
    "x6": 6,
    "x7": 7,
    "x8": 8,
    "x9": 9,
    "All": 20
}


def match_shape_and_dist(posA, posB, shape, dist):
    if shape == "Cardinal":
        return posA.cardinal_to(posB, int(dist))
    if shape == "Diagonal":
        return posA.diagonal_to(posB, int(dist))
    if shape == "Omni":
        return posA.cardinal_or_diagonal_to(posB, int(dist))
    if shape == "Adjacent":
        return posA.adjacent_to(posB)
    if shape == "Rectilinear":
        return posA.rectilinear_to(posB, int(dist))
    if shape == "Row":
        return posA.same_row(posB)
    if shape == "Column":
        return posA.same_column(posB)
    if shape == "Any":
        return True
    if shape == "Other":
        return True
    return False


def match_amount(amount_str):
    return amount_dictionary[amount_str]


def match_with_target_data(targetdata, user, game_ref):
    # scope_pass
    scope = targetdata["scope"]
    number = 0
    grouped= False
    inital_targets = []
    if (scope == "Self"):
        return [user], 1, False
    for entity in game_ref.get_entity_list():
        team_equal = (user.get_team() == entity.get_team())
        if scope == "Enemy" and not (team_equal):
            inital_targets.append(entity)
        if scope == "Ally" and (team_equal):
            inital_targets.append(entity)
        if scope == "Both":
            inital_targets.append(entity)

    # shape, dist
    shape_pass = []
    posA = user.get_position()
    for other in inital_targets:
        posB = other.get_position()
        #if posA.is_equal(posB) == False: #Don't match if the coordinates are the same
        if match_shape_and_dist(posA, posB, targetdata["shape"], targetdata["dist"]):
            shape_pass.append(other)
    # get_number_of_entities
    number = match_amount(targetdata["amount"])

    # get_limits...
    limit_dict={}
    for lim in targetdata["limit"]:
         if lim == "noself":
             limit_dict["noself"]=True

    elimination_pass = []

    for piece in shape_pass:
        if "noself" in limit_dict:
            if piece.get_game_id() != user.get_game_id():
                elimination_pass.append(piece)
        else:
            elimination_pass.append(piece)

    final_pass = elimination_pass
    return final_pass, number, grouped
