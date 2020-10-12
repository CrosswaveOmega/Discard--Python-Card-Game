from .notationhelp import space_notation_to_value, to_notation
        #['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
class Position():
    def __init__(self, x=None, y=None, notation=None):
        if(notation!=None):
            x_note, y_note= space_notation_to_value(notation)
            self.row=y_note
            self.column=x_note
        else:
            self.row=y
            self.column=x
    def getR(self):
        return self.row
    def getC(self):
        return self.column
    def get_row(self):
        return self.getR()
    def get_col(self):
        return self.getC()
    def x(self):
        return self.getC()
    def y(self):
        return self.getR()
    def x_y(self):
        return (self.x(), self.y())
    def get_notation(self):
        return to_notation(self.column, self.row);
    def same_row(self, other):
        """Check if other is in same row."""
        if(self.y()==other.y()):
            return True
        return False
    def same_column(self, other):
        """Check if other is in same column."""
        if(self.x()==other.x()):
            return True
        return False
    def north_of(self, other, rangeVal=1):
        """Check if other is in the row to the north of self.
        """
        mod=rangeVal
        row_mod=self.y() + mod
        if(row_mod == other.y()):
            return True
        return False
    def south_of(self, other, rangeVal=1):
        """Check if other is in the row to the south of self."""
        mod=rangeVal
        row_mod=self.y() - mod
        if(row_mod == other.y()):
            return True
        return False

    def east_of(self, other, rangeVal=1):
        """Check if other is in the column to the east of self."""
        mod=rangeVal
        column_mod=self.x() + mod
        if(column_mod == other.x()):
            return True
        return False
    def west_of(self, other, rangeVal=1):
        """Check if other is in the column to the west of self."""
        mod=rangeVal
        column_mod=self.x() - mod
        if(column_mod == other.x()):
            return True
        return False
    def northeast_of(self, other, rangeVal=1):
        if (self.north_of(other, rangeVal) and self.east_of(other, range_val)):
            return True
        return False
    def northwest_of(self, other, rangeVal=1):
        if (self.north_of(other, rangeVal) and self.west_of(other, range_val)):
            return True
        return False
    def southeast_of(self, other, rangeVal=1):
        if (self.south_of(other, rangeVal) and self.south_of(other, range_val)):
            return True
        return False
    def southwest_of(self, other, rangeVal=1):
        if (self.south_of(other, rangeVal) and self.west_of(other, range_val)):
            return True
        return False
    def diagonal_to(self, other, rangeVal=1):
        if not(self.same_row(other) or self.same_column(other)): #test 1. only diagonals.
            if(self.north_of(other) or self.south_of(other) or self.east_of(other) or self.west_of(other)):
                return True
        return False
    def adjacent_to(self, other):
        if(self.same_row(other) or self.same_column(other)): #test 1. no diagonals.
            if((self.north_of(other)) or (self.south_of(other)) or (self.east_of(other)) or (self.west_of(other))):
                return True
        return False
     # adding two objects
    def __add__(self, other):
        currX=self.getC()
        currY=self.getR()
        return Position(currX+other.getC(), currY+other.getR())
    # subtracting two objects
    def __sub__(self, other):
        currX=self.getC()
        currY=self.getR()
        return Position(currX+other.getC(), currY+other.getR())

#Testing.

#Driver Code
#Driver Code.
if __name__ == "__main__":
    posA=Position(1,1)
    posB=Position(2,1)
    posC=Position(2,2)

    posD=Position(2,3)

    print(posA.north_of(posC), posB.north_of(posD), posB.north_of(posD, 2), posC.south_of(posA), posA.east_of(posC), posC.west_of(posA), posB.adjacent_to(posA), posB.adjacent_to(posC),posA.adjacent_to(posB), posA.adjacent_to(posC), posA.diagonal_to(posC), posC.diagonal_to(posA))

    print(posD.get_notation())
