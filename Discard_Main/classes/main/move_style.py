

class move_style:
    """Move Style is stored as a multi-lined string."""
    def __init__(self):
        def count=1#number of times you can move.
        """
        SAME ROW
        SAME COLUMN
        SAME DIAGONAL
        SAME ROW LIMIT 4
        SAME COLUMN LIMIT 4
        SAME DIAGONAL LIMIT 4
        HOP X -1 Y -2
        WALK X 1 Y 1
        WALK X 1 Y -1
        WALK X -1 Y 1
        WALK X -1 Y -1
        """
