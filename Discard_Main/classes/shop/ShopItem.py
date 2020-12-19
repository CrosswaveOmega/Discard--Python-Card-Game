

class ShopItem():
    """Objects that can be shopped for."""
    def __init__(self):
        self.name=""
        self.stock=0
        self.coin=0
        self.star=0
        self.ticket=0
        self.itemcontent=[]
        self.forsale=False

    def to_dictionary(self):
        newdictionary=vars(self).copy()
        return newdictionary

    def add_to_content(self, itemtype:str, value:str):
        entry={}
        entry["type"]=itemtype
        entry["value"]=itemvalue
        self.itemcontent.append(entry)
