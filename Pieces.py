class Piece:
    def __init__(self, color, grid_x, grid_y):

        # x, y grid coordinates of Piece
        self.x = grid_x
        self.y = grid_y

        # Tkinter image id
        self.id = None

        # The piece has never moved
        self.first = True

        # Color of piece: black or white
        self.color = color

    @staticmethod
    def in_range(x, y):
        if 0 <= x < 8 and 0 <= y < 8:
            return True

        return False

    # Move the piece in the matrix, then return previous
    # grid positions and the target_piece
    def tentative_move(self, x, y, chess):
        # Store previous grid locations
        prev_x = self.x
        prev_y = self.y

        # Remove this piece from its previous location
        chess.matrix[prev_x][prev_y] = None

        # Change this piece's grid x,y to new grid x,y
        self.x = x
        self.y = y

        target_piece = chess.matrix[x][y]
        chess.matrix[x][y] = self

        if target_piece is not None:
            if target_piece.color == 'WHITE':
                chess.white_pieces.remove(target_piece)
            elif target_piece.color == 'BLACK':
                chess.black_pieces.remove(target_piece)

        return [prev_x, prev_y, target_piece]

    def revert(self, prev_x, prev_y, target_piece, chess):
        # Revert board back to previous state
        chess.matrix[self.x][self.y] = target_piece
        if target_piece is not None:
            if target_piece.color == 'WHITE':
                chess.white_pieces.append(target_piece)
            elif target_piece.color == 'BLACK':
                chess.black_pieces.append(target_piece)

        chess.matrix[prev_x][prev_y] = self

        self.x = prev_x
        self.y = prev_y

    def move(self, x, y, chess):
        # If piece is king and is attempting castle
        # execute this if block
        # Else, carry on
        if isinstance(self, King) and self.attempting_castle(x, y, chess):
            return self.has_castled(x, y, chess)

        # Move tentatively
        prev_x, prev_y, target_piece = self.tentative_move(x, y, chess)

        # If move is illegal, revert back to original state
        if chess.is_illegal_state(self.color):
            self.revert(prev_x, prev_y, target_piece, chess)
            return False

        # This piece has made its first move, so set
        # self.first to false
        self.first = False

        return True

    def move_AI(self, x, y, chess):
        # Move tentatively
        prev_x, prev_y, target_piece = self.tentative_move(x, y, chess)

        # If move is illegal, revert back to original state
        if chess.is_illegal_state(self.color):
            self.revert(prev_x, prev_y, target_piece, chess)
            return [False, self.x, self.y, x, y]

        self.revert(prev_x, prev_y, target_piece, chess)

        return [True, self.x, self.y, x, y]

    # Converts to pixel and adds 10 for the width of an image. Change later
    def convert_grid_to_pixel(self, x, y):
        pos_list = [((x + 1) * 80) + 10, ((y + 1) * 80) + 10]

        return pos_list


class Pawn(Piece):
    def __init__(self, color, grid_x, grid_y):
        self.file = 'images/' + color + '_PAWN.png'
        self.val = 100
        super().__init__(color, grid_x, grid_y)

    def possible_moves(self, board):
        possible_moves = []

        x = self.x
        y = self.y

        move_one = 0
        move_two = 0

        if self.color == 'WHITE':
            move_one = -1
            move_two = -2

        if self.color == 'BLACK':
            move_one = 1
            move_two = 2

        can_move_one = False
        # Check if we can move one space forward
        if Piece.in_range(x, y + move_one):
            piece = board[x][y + move_one]
            if piece is None:
                possible_moves.append([x, y + move_one])
                can_move_one = True

        # Check if we can move one space diagonally right
        if Piece.in_range(x + 1, y + move_one):
            piece = board[x + 1][y + move_one]
            if piece is not None and piece.color != self.color:
                possible_moves.append([x + 1, y + move_one])

        # Check if we can move one space diagonally left
        if Piece.in_range(x - 1, y + move_one):
            piece = board[x - 1][y + move_one]
            if piece is not None and piece.color != self.color:
                possible_moves.append([x - 1, y + move_one])

        # Check if this is pawn's first move
        # and if it can move two spaces forward
        if self.first and Piece.in_range(x, y + move_two):
            piece = board[x][y + move_two]
            if piece is None and can_move_one:
                possible_moves.append([x, y + move_two])

        return possible_moves


class Rook(Piece):
    def __init__(self, color, grid_x, grid_y):
        self.file = 'images/' + color + '_ROOK.png'
        self.val = 500
        super().__init__(color, grid_x, grid_y)

    def possible_moves(self, board):
        possible_moves = []

        x = self.x
        y = self.y

        up_spaces = True
        down_spaces = True
        left_spaces = True
        right_spaces = True

        for i in range(1, 8):
            if up_spaces and Piece.in_range(x, y + i):
                piece = board[x][y + i]
                if piece is None:
                    possible_moves.append([x, y + i])
                elif self.color != piece.color:
                    possible_moves.append([x, y + i])
                    up_spaces = False
                else:
                    up_spaces = False

            if down_spaces and Piece.in_range(x, y - i):
                piece = board[x][y - i]
                if piece is None:
                    possible_moves.append([x, y - i])
                elif self.color != piece.color:
                    possible_moves.append([x, y - i])
                    down_spaces = False
                else:
                    down_spaces = False

            if left_spaces and Piece.in_range(x - i, y):
                piece = board[x - i][y]
                if piece is None:
                    possible_moves.append([x - i, y])
                elif self.color != piece.color:
                    possible_moves.append([x - i, y])
                    left_spaces = False
                else:
                    left_spaces = False

            if right_spaces and Piece.in_range(x + i, y):
                piece = board[x + i][y]
                if piece is None:
                    possible_moves.append([x + i, y])
                elif self.color != piece.color:
                    possible_moves.append([x + i, y])
                    right_spaces = False
                else:
                    right_spaces = False

        return possible_moves


class Knight(Piece):
    def __init__(self, color, grid_x, grid_y):
        self.file = 'images/' + color + '_KNIGHT.png'
        self.val = 320
        super().__init__(color, grid_x, grid_y)

    def possible_moves(self, board):

        possible_moves = []

        x = self.x
        y = self.y

        two_moves_x = 2
        two_moves_y = 2

        one_move_x = 1
        one_move_y = 1

        for i in range(2):
            if Piece.in_range(x + two_moves_x, y + one_move_y):
                piece = board[x + two_moves_x][y + one_move_y]
                if piece is None or self.color != piece.color:
                    possible_moves.append([x + two_moves_x, y + one_move_y])

            if Piece.in_range(x + two_moves_x, y - one_move_y):
                piece = board[x + two_moves_x][y - one_move_y]
                if piece is None or self.color != piece.color:
                    possible_moves.append([x + two_moves_x, y - one_move_y])

            if Piece.in_range(x + one_move_x, y + two_moves_y):
                piece = board[x + one_move_x][y + two_moves_y]
                if piece is None or self.color != piece.color:
                    possible_moves.append([x + one_move_x, y + two_moves_y])

            if Piece.in_range(x + one_move_x, y - two_moves_y):
                piece = board[x + one_move_x][y - two_moves_y]
                if piece is None or self.color != piece.color:
                    possible_moves.append([x + one_move_x, y - two_moves_y])

            two_moves_x *= -1
            two_moves_y *= -1

            one_move_x *= -1
            one_move_y *= -1

        return possible_moves


class Bishop(Piece):
    def __init__(self, color, grid_x, grid_y):
        self.file = 'images/' + color + '_BISHOP.png'
        self.val = 330
        super().__init__(color, grid_x, grid_y)

    def possible_moves(self, board):
        possible_moves = []

        x = self.x
        y = self.y

        up_right_spaces = True
        down_right_spaces = True
        up_left_spaces = True
        down_left_spaces = True

        for i in range(1, 8):
            new_right_x = x + i
            new_left_x = x - i
            new_up_y = y + i
            new_down_y = y - i

            if up_right_spaces and Piece.in_range(new_right_x, new_up_y):
                piece = board[new_right_x][new_up_y]
                if piece is None:
                    possible_moves.append([new_right_x, new_up_y])
                elif self.color != piece.color:
                    possible_moves.append([new_right_x, new_up_y])
                    up_right_spaces = False
                else:
                    up_right_spaces = False
            if down_right_spaces and Piece.in_range(new_right_x, new_down_y):
                piece = board[new_right_x][new_down_y]
                if piece is None:
                    possible_moves.append([new_right_x, new_down_y])
                elif self.color != piece.color:
                    possible_moves.append([new_right_x, new_down_y])
                    down_right_spaces = False
                else:
                    down_right_spaces = False
            if up_left_spaces and Piece.in_range(new_left_x, new_up_y):
                piece = board[new_left_x][new_up_y]
                if piece is None:
                    possible_moves.append([new_left_x, new_up_y])
                elif self.color != piece.color:
                    possible_moves.append([new_left_x, new_up_y])
                    up_left_spaces = False
                else:
                    up_left_spaces = False
            if down_left_spaces and Piece.in_range(new_left_x, new_down_y):
                piece = board[new_left_x][new_down_y]
                if piece is None:
                    possible_moves.append([new_left_x, new_down_y])
                elif self.color != piece.color:
                    possible_moves.append([new_left_x, new_down_y])
                    down_left_spaces = False
                else:
                    down_left_spaces = False

        return possible_moves


class Queen(Piece):
    def __init__(self, color, grid_x, grid_y):
        self.file = 'images/' + color + '_QUEEN.png'
        self.val = 900
        super().__init__(color, grid_x, grid_y)

    def possible_moves(self, board):
        possible_moves = []

        up_right_spaces = True
        down_right_spaces = True
        up_left_spaces = True
        down_left_spaces = True

        up_spaces = True
        down_spaces = True
        left_spaces = True
        right_spaces = True

        x = self.x
        y = self.y

        for i in range(1, 8):
            new_right_x = x + i
            new_left_x = x - i
            new_up_y = y + i
            new_down_y = y - i

            if up_spaces and Piece.in_range(x, new_up_y):
                piece = board[x][new_up_y]
                if piece is None:
                    possible_moves.append([x, new_up_y])
                elif self.color != piece.color:
                    possible_moves.append([x, new_up_y])
                    up_spaces = False
                else:
                    up_spaces = False
            if down_spaces and Piece.in_range(x, new_down_y):
                piece = board[x][new_down_y]
                if piece is None:
                    possible_moves.append([x, new_down_y])
                elif self.color != piece.color:
                    possible_moves.append([x, new_down_y])
                    down_spaces = False
                else:
                    down_spaces = False
            if left_spaces and Piece.in_range(new_left_x, y):
                piece = board[new_left_x][y]
                if piece is None:
                    possible_moves.append([new_left_x, y])
                elif self.color != piece.color:
                    possible_moves.append([new_left_x, y])
                    left_spaces = False
                else:
                    left_spaces = False
            if right_spaces and Piece.in_range(new_right_x, y):
                piece = board[new_right_x][y]
                if piece is None:
                    possible_moves.append([new_right_x, y])
                elif self.color != piece.color:
                    possible_moves.append([new_right_x, y])
                    right_spaces = False
                else:
                    right_spaces = False

            if up_right_spaces and Piece.in_range(new_right_x, new_up_y):
                piece = board[new_right_x][new_up_y]
                if piece is None:
                    possible_moves.append([new_right_x, new_up_y])
                elif self.color != piece.color:
                    possible_moves.append([new_right_x, new_up_y])
                    up_right_spaces = False
                else:
                    up_right_spaces = False
            if down_right_spaces and Piece.in_range(new_right_x, new_down_y):
                piece = board[new_right_x][new_down_y]
                if piece is None:
                    possible_moves.append([new_right_x, new_down_y])
                elif self.color != piece.color:
                    possible_moves.append([new_right_x, new_down_y])
                    down_right_spaces = False
                else:
                    down_right_spaces = False
            if up_left_spaces and Piece.in_range(new_left_x, new_up_y):
                piece = board[new_left_x][new_up_y]
                if piece is None:
                    possible_moves.append([new_left_x, new_up_y])
                elif self.color != piece.color:
                    possible_moves.append([new_left_x, new_up_y])
                    up_left_spaces = False
                else:
                    up_left_spaces = False
            if down_left_spaces and Piece.in_range(new_left_x, new_down_y):
                piece = board[new_left_x][new_down_y]
                if piece is None:
                    possible_moves.append([new_left_x, new_down_y])
                elif self.color != piece.color:
                    possible_moves.append([new_left_x, new_down_y])
                    down_left_spaces = False
                else:
                    down_left_spaces = False

        return possible_moves


class King(Piece):
    def __init__(self, color, grid_x, grid_y):
        self.file = 'images/' + color + '_KING.png'
        self.val = 20000
        super().__init__(color, grid_x, grid_y)

    def possible_moves(self, board):

        possible_moves = []
        vertical = 1
        horizontal = 1

        x = self.x
        y = self.y

        for i in range(2):
            new_x = x + horizontal
            new_y = y + vertical

            if (0 <= new_x < 8) and (0 <= new_y < 8):
                piece = board[new_x][new_y]
                if piece is None:
                    possible_moves.append([new_x, new_y])
                elif self.color != piece.color:
                    possible_moves.append([new_x, new_y])

            if 0 <= new_x < 8:
                piece = board[new_x][y]
                if piece is None:
                    possible_moves.append([new_x, y])
                elif self.color != piece.color:
                    possible_moves.append([new_x, y])

            if 0 <= new_y < 8:
                piece = board[x][new_y]
                if piece is None:
                    possible_moves.append([x, new_y])
                elif self.color != piece.color:
                    possible_moves.append([x, new_y])

            new_x = x + (1 * horizontal)
            new_y = y + (-1 * vertical)

            if (0 <= new_x < 8) and (0 <= new_y < 8):
                piece = board[new_x][new_y]
                if piece is None:
                    possible_moves.append([new_x, new_y])
                elif self.color != piece.color:
                    possible_moves.append([new_x, new_y])

            vertical *= -1
            horizontal *= -1

        # Following is for castling
        if self.first:
            rook_right = board[7][y]
            rook_left = board[0][y]

            if rook_right is not None and isinstance(rook_right, Rook) \
                    and rook_right.first:
                possible_moves.append([6, y])

                for i in range(2):
                    if board[self.x + i + 1][self.y] is not None:
                        del possible_moves[-1]
                        break

            if rook_left is not None and isinstance(rook_left, Rook) \
                    and rook_left.first:
                possible_moves.append([2, y])

                for i in range(3):
                    if board[self.x - i - 1][self.y] is not None:
                        del possible_moves[-1]
                        break

        return possible_moves

    def attempting_castle(self, x, y, chess):
        return self.first and (x == 6 or x == 2) and (y == 0 or y == 7)

    def has_castled(self, x, y, chess):
        # List of all positions of the castling side
        castle_side = []
        shift_x = 0
        castle_range = 0
        rook = None
        king = chess.matrix[self.x][self.y]
        rook_new_x = 0

        if x == 6:
            shift_x = 1
            castle_range = 4
            rook = chess.matrix[7][king.y]
            rook_new_x = 5
        if x == 2:
            shift_x = -1
            castle_range = 5
            rook = chess.matrix[0][king.y]
            rook_new_x = 3

        for i in range(castle_range):
            castle_side.append([king.x + (i * shift_x), king.y])

        if chess.cannot_castle(castle_side, self.color):
            return [0, 0, None, False]

        # Store king's previous grid locations
        king_prev_x = king.x
        king_prev_y = king.y

        # Store rook's previous grid locations
        rook_prev_x = rook.x
        rook_prev_y = rook.y

        # Remove these pieces from its previous location
        chess.matrix[king_prev_x][king_prev_y] = None
        chess.matrix[rook_prev_x][rook_prev_y] = None

        # Change these pieces' grid x to new grid x
        king.x = x
        rook.x = rook_new_x

        chess.matrix[x][y] = king
        chess.matrix[rook_new_x][y] = rook

        king.first = False
        rook.first = False

        return [rook_prev_x, rook_prev_y, rook, True]
