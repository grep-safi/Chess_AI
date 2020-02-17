class Chess:
    def __init__(self, color, grid_x, grid_y, filename):

        # Records if piece has ever moved
        self.has_moved = True
        self.file = filename

        # x, y grid coordinates of Piece
        self.x = grid_x
        self.y = grid_y

        # Records the Tkinter image id when piece is initialized
        self.id = None

        # Color of piece: black or white
        self.color = color


class Pawn(Chess):
    def __init__(self):
        pass


class Rook(Chess):
    def __init__(self):
        pass


class Knight(Chess):
    def __init__(self):
        pass


class Bishop(Chess):
    def __init__(self):
        pass


class Queen(Chess):
    def __init__(self):
        pass


class King(Chess):
    def __init__(self):
        pass
