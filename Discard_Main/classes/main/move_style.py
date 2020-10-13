

class move_style:
    """Move Style is stored as a multi-lined string."""
    def __init__(self):
        self.count=1#number of times you can move.
        self.instruction"""
        SAME ROW
        SAME COLUMN
        SAME DIAGONAL
        SAME ROW LIMIT 4
        SAME COLUMN LIMIT 4
        SAME DIAGONAL LIMIT 4
        HOP X -1 Y -2
        STEP 1
        STEP 2
        STEP X 1 Y 1
        STEP X -1 Y -1
        """ #- how you can move.
