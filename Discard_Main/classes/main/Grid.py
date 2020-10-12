from .generic.notationhelp import space_notation_to_value, to_notation, get_letter
from .generic.position import Position
LETTERS={"A":1, "B":2, "C":3, "D":4, "E":5, "F":6, "G":7, "H":8, "I":9, "J":10, "K":11, "L":12, "M":13, "N":14, "O":15, "P":16, "Q":17, "R":18, "S":19, "T":20, "U":21, "V":22, "W":23, "X":24, "Y":25, "Z":26}
class Grid:
    """Where the game will be played.

note: should start at lower right corner.

[ ][ ][ ][ ][ ]
[ ][S][S][S][ ]
[ ][S][L][S][ ]
[ ][S][S][S][ ]
[ ][ ][ ][ ][ ]


    """
    def __init__(self, rows=5, columns=5, game=None):
        self.game_ref=game
        self.rows=rows
        self.columns=columns
        self.grid_array=[]
        for i in range(self.columns):
            col = []
            for j in range(self.rows):
                col.append("Non")
            self.grid_array.append(col)
    def check_if_space_is_on_board(self, x, y):
        """Check if x and y are within the Grid's bounds."""
        if((x<=self.columns and x>0) and (y<=self.rows and y>0)):
            return True
        return False
    def check_if_space_is_valid(self, pos):
        """Check if X and y are within range. and there is nothing there."""
        if(self.check_if_space_is_on_board(pos.getC(), pos.getR())):
            for piece in self.game_ref.entity_list:
                if pos.get_notation()==piece.position.get_notation():
                    return False
            return True
        return False
    def check_with_change(self,  orig_column, orig_row, changeX, changeY, limit=99):
        """intended for the SAME ROW, SAME COLUMN, SAME DIAGONAL part.
            stop if anything is in the way.
        """
        list=[]
        modX=0+changeX
        modY=0+changeY
        print
        valid=True
        current_column=orig_column
        current_row=orig_row
        current_count=1
        while valid:
            if(self.check_if_space_is_on_board(current_column+modX, current_row+modY)):#Out of bounds check.
                pos=Position(current_column+modX, current_row+modY)
                print(pos.get_notation())
                valid=self.check_if_space_is_valid(pos) #Is there something there check.
                if valid:
                    list.append(pos.get_notation())
                    modX=modX+changeX
                    modY=modY+changeY
                current_count=current_count+1
                if(current_count>limit): #if the current_count is more than the limit param, set valid to false.
                    valid=False
            else:
                valid=False
        return list
    def get_same_movements(self, current, moves):
        """
        current-current position
        moves- line split by space.
        """
        list=[]
        if(len(moves)<2):
            print("TOO FEW ARGUMENTS.")
            return None
        scope=moves[1]
        limitV=99
        if(len(moves)>=4):
            print("MORE")
            if moves[2]=='LIMIT':
                print("limitmode")
                limitV=int(moves[3])
        if scope== "COLUMN":
            orig_column=current.getC()
            orig_row=current.getR()
            listA=self.check_with_change(orig_column, orig_row, -1, 0, limitV);
            listB=self.check_with_change(orig_column, orig_row,  1, 0, limitV);
            for item in listA:
                list.append(item)
            for item in listB:
                list.append(item)
        if scope== "ROW":
            orig_column=current.getC()
            orig_row=current.getR()
            listA=self.check_with_change(orig_column, orig_row,  0, -1, limitV);
            listB=self.check_with_change(orig_column, orig_row,  0,  1, limitV);
            for item in listA:
                list.append(item)
            for item in listB:
                list.append(item)
        return list
    def get_hop_movements(self, current, moves):
        """
        current-current position
        moves- line split by space.

        """
        # ['HOP', 'SCOPE', 'VALUEA', 'SCOPEB', 'VALUEB']


        list=[]
        if(len(moves)<3):
            print("TOO FEW ARGUMENTS.")
            return None
        scopea=moves[1]
        valuea=moves[2]
        scopeb=None
        valueb=None
        if(len(moves)>=5):
            print("MORE")
            scopeb=moves[3]
            valueb=moves[4]
        if scopea== "X":
            print("TBD")
        if scopea== "Y":
            print("TBD")
        return list
    def get_all_movements_in_range(self, current, line):
        """Params
        current-Position object
        line- A string of the move_pattern info.
        """
        #line is a string
        moves=line.split(' ')
        print(moves)
        type=moves[0]
        list=[]
        if type=='SAME': #type same
            # ['SAME', 'SCOPE', LIMIT, VALUE]
            list=self.get_same_movements(current, moves)
        if type=='HOP': #type same
            # ['HOP', 'SCOPE', 'VALUEA', 'SCOPEB', 'VALUEB']
            list=self.get_hop_movements(current, moves)

        if type=='STEP': #type same
            # ['SAME', 'SCOPE', LIMIT, VALUE]
            if(len(moves)<2):
                print("TOO FEW ARGUMENTS.")
                return None
            scope=moves[1]
            limitV=99
            if(len(moves)>=4):
                print("MORE")
                if moves[2]=='LIMIT':
                    print("limitmode")
                    limitV=int(moves[3])
            if scope== "COLUMN":
                orig_column=current.getC()
                orig_row=current.getR()
                listA=self.check_with_change(orig_column, orig_row, -1, 0, limitV);
                listB=self.check_with_change(orig_column, orig_row,  1, 0, limitV);
                for item in listA:
                    list.append(item)
                for item in listB:
                    list.append(item)
            if scope== "ROW":
                orig_column=current.getC()
                orig_row=current.getR()
                listA=self.check_with_change(orig_column, orig_row,  0, -1, limitV);
                listB=self.check_with_change(orig_column, orig_row,  0,  1, limitV);
                for item in listA:
                    list.append(item)
                for item in listB:
                    list.append(item)

        return list

    def get_space(self, string_name):
        print(space_notation_to_value(string_name))
    def return_grid(self):
        return self.grid_array
    def print_grid(self, orientation="north"):
        print("START!")
        print("Orientation: "+orientation)
        newgrid= list(map(list, self.grid_array))

        numgrid=[]
        for piece in self.game_ref.entity_list:
            x, y= piece.position.x_y()
            newgrid[y-1][x-1]=piece.name
        for j in range(self.columns):
            numgrid.append(get_letter(j+1))
    #    newgrid.insert(0, numgrid)

        returnVal=""
        returnVal=returnVal+(''.join(['{:10}|'.format(item) for item in numgrid ]))+str(numgrid)+"\n"
        #north

        startValue=0 #Start at top of board.
        endValue=self.rows #End at bottom of board
        #south
        if(orientation=="south"):
            startValue=self.rows-1  #Start at bottom of board
            endValue=0-1  #End at top of board.  needs to reach 0.
        row=startValue
        delim=1
        if startValue>endValue:
            delim=-1
        while row!=endValue:

            print(row)
            returnVal=returnVal+(''.join(['{:10}|'.format(item) for item in newgrid[row]]))+str(row+1)+"\n"
            row=row+delim


        #for row in range(startValue, endValue):
        #    returnVal=returnVal+(''.join(['{:10}|'.format(item) for item in newgrid[row]]))+str(row+1)+"\n"
        print(returnVal)
    def set_space_value(self, notation, value):
        col, row= space_notation_to_value(notation)
        self.grid_array[row-1][col-1]=value






#Driver Code.
if __name__ == "__main__":
    testGrid=Grid()
    print(testGrid.return_grid())
    testGrid.print_grid()
    print(testGrid.return_grid())

    testGrid.set_space_value("D5", "LQP")
    testGrid.print_grid()
    print(testGrid.return_grid())
