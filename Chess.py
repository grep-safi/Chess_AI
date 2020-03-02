import copy
from Pieces import Pawn
from Pieces import Rook
from Pieces import Knight
from Pieces import Bishop
from Pieces import Queen
from Pieces import King


class Chess:
    def __init__(self, main=True):
        # 2D Array that will handle Chess logic
        self.matrix = [[None for row in range(8)] for col in range(8)]

        # Keep track of each sides pieces
        self.white_pieces = []
        self.black_pieces = []

        self.white_king = []
        self.black_king = []

        self.king_is_in_check = False

        self.black_check_mate = False
        self.white_check_mate = False

        if main:
            self.loadMinorPieces()
            # self.loadMajorPieces()

        self.piece_in_check = []

    # Check if moving king to any square removes it from check
    # Check if moving any of king's pieces to any square (including enemy
    # squares) removes it from check
    def in_checkmate(self, pieces, king):
        enemy_pieces = pieces
        friendly_pieces = None
        if king.color == 'WHITE':
            friendly_pieces = self.white_pieces
        if king.color == 'BLACK':
            friendly_pieces = self.black_pieces

        # First, check if king can move to legal square out of check
        possible_king_moves = king.possible_moves(self.matrix)
        for move in possible_king_moves:
            prev_x, prev_y, t_piece = king.tentative_move(move[0], move[1], self)

            still_checked = self.in_check(enemy_pieces, king, check_illegal=True)
            king.revert(prev_x, prev_y, t_piece, self)
            if not still_checked:
                return False

        # Next, check if King's pieces can move to squares that
        # will remove the check on the King
        for piece in friendly_pieces:
            if isinstance(piece, King):
                continue
            possible_moves = piece.possible_moves(self.matrix)
            for move in possible_moves:
                prev_x, prev_y, t_piece = piece.tentative_move(move[0], move[1], self)
                is_in_check = self.in_check(enemy_pieces, king, check_illegal=True)
                piece.revert(prev_x, prev_y, t_piece, self)
                if not is_in_check:
                    return False

        # print('CHECKMATE HAS BEEEN REACHED')
        # print(king.color, ' has been MATED!')
        return True

    def in_check(self, pieces, king, check_illegal=False):
        # print('I AAM MUFASA!!', king)
        king_position = [king.x, king.y]

        for piece in pieces:
            possible_piece_moves = piece.possible_moves(self.matrix)

            if king_position in possible_piece_moves:
                if check_illegal:
                    return True
                else:
                    self.in_checkmate(pieces, king)
                    # self.black_check_mate = self.in_checkmate('BLACK')
                    self.piece_in_check = king
                    self.king_is_in_check = True

                break

        return False

    def is_illegal_state(self, color):
        self.king_is_in_check = False

        if color == 'WHITE':
            if self.in_check(self.black_pieces, self.white_king, check_illegal=True):
                return True

            self.in_check(self.white_pieces, self.black_king)
        elif color == 'BLACK':
            if self.in_check(self.white_pieces, self.black_king, check_illegal=True):
                return True

            self.in_check(self.black_pieces, self.white_king)

        if not self.king_is_in_check:
            self.piece_in_check = []

        return False

    def evaluate_board(self):
        total_white = 0
        total_black = 0

        for w_piece in self.white_pieces:
            total_white += w_piece.val

        for b_piece in self.black_pieces:
            total_black += b_piece.val

        value = total_black - total_white

        # print('This is the current evaluation', value)
        return value

    def clone(self):
        board_clone = Chess(main=False)

        board_clone.matrix = copy.deepcopy(self.matrix)

        for row in board_clone.matrix:
            for piece in row:
                if piece is not None:
                    if piece.color == 'WHITE':
                        board_clone.white_pieces.append(piece)
                        if isinstance(piece, King):
                            board_clone.white_king = piece
                    elif piece.color == 'BLACK':
                        board_clone.black_pieces.append(piece)
                        if isinstance(piece, King):
                            board_clone.black_king = piece

        board_clone.king_is_in_check = self.king_is_in_check
        board_clone.black_check_mate = self.black_check_mate = False
        board_clone.white_check_mate = self.white_check_mate = False

        board_clone.piece_in_check = self.piece_in_check = []

        return board_clone

    def cannot_castle(self, castle_squares, color):
        # king_position = [king.grid_x, king.grid_y]
        if color == 'WHITE':
            pieces = self.black_pieces
        elif color == 'BLACK':
            pieces = self.white_pieces

        for piece in pieces:
            possible_piece_moves = piece.possible_moves(self.matrix)

            for square in castle_squares:
                if square in possible_piece_moves:
                    return True

        return False

    # Loads pawns
    def loadMinorPieces(self):
        for i in range(1):
            black_pawn_piece = Pawn('BLACK', i, 2)
            self.matrix[i][2] = black_pawn_piece

            white_pawn_piece = Pawn('WHITE', i, 6)
            self.matrix[i][6] = white_pawn_piece

            self.black_pieces.append(black_pawn_piece)
            self.white_pieces.append(white_pawn_piece)

        self.matrix[4][7] = King('WHITE', 4, 7)
        self.matrix[4][0] = King('BLACK', 4, 0)
        self.black_king = self.matrix[4][0]
        self.white_king = self.matrix[4][7]

        self.matrix[0][0] = Rook('BLACK', 0, 0)
        self.matrix[0][7] = Rook('WHITE', 0, 7)

        self.matrix[2][7] = Bishop('WHITE', 2, 7)
        self.matrix[2][0] = Bishop('BLACK', 2, 0)

        self.black_pieces.append(self.black_king)
        self.white_pieces.append(self.white_king)

        self.black_pieces.append(self.matrix[0][0])
        self.white_pieces.append(self.matrix[0][7])

        self.white_pieces.append(self.matrix[2][7])
        self.black_pieces.append(self.matrix[2][0])

    # Loads Kings, Queens, Bishops, Knights, and Rooks
    def loadMajorPieces(self):
        self.matrix[0][0] = Rook('BLACK', 0, 0)
        self.matrix[7][0] = Rook('BLACK', 7, 0)

        self.matrix[1][0] = Knight('BLACK', 1, 0)
        self.matrix[6][0] = Knight('BLACK', 6, 0)

        self.matrix[2][0] = Bishop('BLACK', 2, 0)
        self.matrix[5][0] = Bishop('BLACK', 5, 0)

        self.matrix[3][0] = Queen('BLACK', 3, 0)


        self.matrix[0][7] = Rook('WHITE', 0, 7)
        self.matrix[7][7] = Rook('WHITE', 7, 7)

        self.matrix[1][7] = Knight('WHITE', 1, 7)
        self.matrix[6][7] = Knight('WHITE', 6, 7)

        self.matrix[2][7] = Bishop('WHITE', 2, 7)
        self.matrix[5][7] = Bishop('WHITE', 5, 7)

        self.matrix[3][7] = Queen('WHITE', 3, 7)


        for i in range(8):
            black_piece = self.matrix[i][0]
            white_piece = self.matrix[i][7]

            self.black_pieces.append(black_piece)
            self.white_pieces.append(white_piece)

    # Prints board to console for debugging purposes
    def print_grid(self):
        board = self.matrix
        st = 0
        sp = 7
        print()
        for i in range(8):
            for j in range(8):
                s = board[st][7 - sp]
                if isinstance(s, Rook):
                    print('R', end=' ')
                if isinstance(s, Queen):
                    print('Q', end=' ')
                if isinstance(s, Pawn):
                    print('P', end=' ')
                if isinstance(s, Bishop):
                    print('B', end=' ')
                if isinstance(s, King):
                    print('K', end=' ')
                if isinstance(s, Knight):
                    print('N', end=' ')
                if s is None:
                    print('-', end=' ')
                st += 1
            st = 0
            sp -= 1
            print('\n')
