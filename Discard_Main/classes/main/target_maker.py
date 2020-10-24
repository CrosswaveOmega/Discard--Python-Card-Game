from .generic.notationhelp import space_notation_to_value, to_notation, get_letter
from .generic.position import Position



{
"shape": "Type of Range",
"dist":"The Number of Spaces covered.",
"scope": "The Scope of the target.",
"amount":"The amount of entities within target.",
"limit": ["Additional Conditions"]
}
optionsDictionary={
"shape": ["Cardinal", "Diagonal", "Omni", "Adjacent", "Rectilinear", "Row", "Column", "Any", "Other"],
"dist": "", #jUST A NUMBER
"scope": ["Enemy", "Ally","Both","Self","Else"],
"amount":["Single","x1","x2","x3","x4","x5","x6","x7","x8","x9","All"],
"limit": ["None"]
}

def Args_To_Target(*args):
    new_dictionary={
    "shape":"", #required
    "dist": 1 ,
    "scope":"", #required
    "amount":"", #required
    "limit": [], #optional
    }
    number_of_args=len(args) #min is 3,
    #match based on universal list.
    shapematch=False
    distmatch=False
    scopematch=False
    amountmatch=False
    for element in args:
        if not shapematch:
            if(element in optionsDictionary["shape"]):
                new_dictionary["shape"]=element
                shapematch=True
        if not scopematch:
            if(element in optionsDictionary["scope"]):
                new_dictionary["scope"]=element
                scopematch=True
        if not amountmatch:
            if(element in optionsDictionary["amount"]):
                new_dictionary["amount"]=element
                amountmatch=True
        if not distmatch:
            stringvertotest=string(element)
            if(stringvertotest.isnumeric()):
                new_dictionary["dist"]=int(stringvertotest)
                distmatch=True
        if(element in optionsDictionary["limit"]):
            new_dictionary["limit"].append(element)
    return new_dictionary
