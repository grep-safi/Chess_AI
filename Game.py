import tkinter as tk
from ai import minimax
import random
from Chess import Chess


class Game:
    def __init__(self, master, canvas):
        self.master = master
        self.cv = canvas

        self.bg_image = tk.PhotoImage(file="images/chess_bg.png")

        self.chess = Chess()

        # Event listeners response
        self.moves = []
        self.circles = []
        self.piece_clicked = False
        self.current_piece = None

        # Binding to get click events
        self.master.bind("<Button-1>", self.getClickXY)

        self.white_turn = True
        self.piece_clicked = False
        self.piece_images = []

        # Prints board and loads pieces
        self.print_board()
        self.drawPieces()

    def drawPieces(self):
        for piece_num in range(16):
            b_piece = self.chess.black_pieces[piece_num]
            w_piece = self.chess.white_pieces[piece_num]

            b_x, b_y = self.convert_grid_to_pixel(b_piece.x, b_piece.y)
            w_x, w_y = self.convert_grid_to_pixel(w_piece.x, w_piece.y)

            b_img = tk.PhotoImage(file=b_piece.file)
            w_img = tk.PhotoImage(file=w_piece.file)

            self.piece_images.append(b_img)
            self.piece_images.append(w_img)

            b_id = self.cv.create_image(b_x, b_y, image=b_img, anchor='nw')
            w_id = self.cv.create_image(w_x, w_y, image=w_img, anchor='nw')

            b_piece.id = b_id
            w_piece.id = w_id

    def getClickXY(self, click_event):
        x = click_event.x
        y = click_event.y
        self.removeCircles()

        grid_x, grid_y = self.convert_pixel_to_grid(x, y)
        target_piece = self.chess.matrix[grid_x][grid_y]

        if self.piece_clicked:
            self.move_piece(grid_x, grid_y)
        elif target_piece.color == 'WHITE' and self.white_turn:
            self.click_piece(grid_x, grid_y)
        elif target_piece.color == 'BLACK' and not self.white_turn:
            self.click_piece(grid_x, grid_y)

    def minimax_AI(self):
        AI_board = self.chess.clone()
        depth = 3
        alpha = [None, -1000000]  # some very large number
        beta = [None, 1000000]  # some very large number
        best_move = minimax([AI_board, 10000], depth, alpha, beta, True, True)
        print(best_move)
#        best_move = minimax([AI_board, 10000], depth, True, True)
        board_obj, board_val, piece_x, piece_y, move_x, move_y = best_move[0]

#        print('this was the best move I could think of: ', piece_x, piece_y, move_x, move_y)
#        board_obj.print_grid()

        piece = self.chess.matrix[piece_x][piece_y]
        target_piece = self.chess.matrix[move_x][move_y]

        piece_move = piece.move(move_x, move_y, self.chess)
        print('this is the piece movee youve looking for', piece_move)
        if len(piece_move) == 6 and piece_move[3]:
            self.move_visually(piece_x, piece_y, None, piece)
            self.move_visually(piece_move[0], piece_move[1], None, piece_move[2])
        # piece_move if promotion
        elif len(piece_move) == 2 and piece_move[0] and piece_move[1]:
            promoted_piece = self.chess.matrix[piece.x][piece.y]
            promoted_x, promoted_y = self.convert_grid_to_pixel(piece.x, piece.y)
            promoted_image = tk.PhotoImage(file=promoted_piece.file)
            self.piece_images.append(promoted_image)
            promoted_id = self.cv.create_image(promoted_x, promoted_y, image=promoted_image, anchor='nw')
            promoted_piece.id = promoted_id
            self.cv.delete(piece.id)

            self.move_visually(piece_x, piece_y, target_piece, promoted_piece)
        # move piece in all other cases:
        elif len(piece_move) == 2 and piece_move[0]:
            self.move_visually(piece_x, piece_y, target_piece, piece)

        self.chess.print_grid()
        self.white_turn = not self.white_turn

    def random_AI(self):
        pieces = self.chess.black_pieces
        rand_piece = pieces[random.randint(0, len(pieces) - 1)]
        moves = rand_piece.possible_grid_moves(self.chess.matrix)
        while len(moves) == 0:
            rand_piece = pieces[random.randint(0, len(pieces) - 1)]
            moves = rand_piece.possible_grid_moves(self.chess.matrix)
        rand_move = moves[random.randint(0, len(moves) - 1)]
        piece_move = rand_piece.move(rand_move[0], rand_move[1], self.chess)
        # needs to be adjusted for the case of castling
        if piece_move:
            self.white_turn = not self.white_turn
        else:
            self.random_AI()

    def move_piece(self, grid_x, grid_y):
        for move in self.moves:
            if grid_x == move[0] and grid_y == move[1]:
                target_piece = self.chess.matrix[grid_x][grid_y]
                prev_x = self.current_piece.x
                prev_y = self.current_piece.y
                piece_move = self.current_piece.move(grid_x, grid_y, self.chess)
                piece = self.current_piece
                # Checks for list because only castling will return list
                # piece_move = [previous rook x, previous rook y, rook object, boolean
                #               that returns true if castling is legal]
                print('who am i, where am i', self.current_piece, prev_x, prev_y)
                print(piece_move)
                if len(piece_move) == 6 and piece_move[3]:
                    print('I TRIED TO DO CASTLE')
                    self.white_turn = not self.white_turn
                    self.move_visually(prev_x, prev_y, None, self.current_piece)
                    self.move_visually(piece_move[0], piece_move[1], None, piece_move[2])
        #            self.minimax_AI()
                # piece_move in all other cases
                elif len(piece_move) == 2 and piece_move[0] and piece_move[1]:
                    print('PORMOTION')
                    self.white_turn = not self.white_turn
                    promoted_piece = self.chess.matrix[piece.x][piece.y]
                    promoted_x, promoted_y = self.convert_grid_to_pixel(piece.x, piece.y)
                    promoted_image = tk.PhotoImage(file=promoted_piece.file)
                    self.piece_images.append(promoted_image)
                    promoted_id = self.cv.create_image(promoted_x, promoted_y, image=promoted_image, anchor='nw')
                    promoted_piece.id = promoted_id
                    self.cv.delete(piece.id)
                    self.move_visually(prev_x, prev_y, target_piece, promoted_piece)
                    # self.minimax_AI()
                elif len(piece_move) == 2 and piece_move[0]:
                    print('every other goddamn easy move')
                    self.white_turn = not self.white_turn
                    self.move_visually(prev_x, prev_y, target_piece, self.current_piece)
         #           self.minimax_AI()
        self.piece_clicked = False
        self.chess.print_grid()

    def move_visually(self, x, y, target_piece, this_piece):
        # If we killed a piece, remove it
        if target_piece is not None:
            self.cv.delete(target_piece.id)

        # Calculate pixel coordinates
        prev_pixel_x, prev_pixel_y = self.convert_grid_to_pixel(x, y)
        new_pixel_x, new_pixel_y = self.convert_grid_to_pixel(
            this_piece.x,
            this_piece.y
        )

        difference_x = new_pixel_x - prev_pixel_x
        difference_y = new_pixel_y - prev_pixel_y

        self.cv.move(this_piece.id, difference_x, difference_y)

    def removeCircles(self):
#        print('someone is calling me')
        for circle in self.circles:
            self.cv.delete(circle)

    def click_piece(self, grid_x, grid_y):
        self.current_piece = self.chess.matrix[grid_x][grid_y]
        if (self.current_piece is None):
            return False

        self.moves = self.current_piece.possible_moves(self.chess.matrix)
        self.piece_clicked = True

        for i in range(len(self.moves)):
            grid_x, grid_y = self.moves[i]
            px, py = self.convert_grid_to_pixel(grid_x, grid_y)
            pixel_x, pixel_y = self.convert_grid_to_pixel(self.current_piece.x, self.current_piece.y)

            x = [grid_x, grid_y, px, py]

            r = 10

            x0 = x[2] - r + 30
            x1 = x[2] + r + 30
            y0 = x[3] - r + 30
            y1 = x[3] + r + 30
            id_num = self.cv.create_oval(x0, y0, x1, y1, fill="#ed7979")
            self.circles.append(id_num)
            # printa("coords of oval", x0,y0,x1,y1)

        return True

    def convert_grid_to_pixel(self, x, y):
        pos_list = [((x + 1) * 80) + 10, ((y + 1) * 80) + 10]

        return pos_list

    def convert_pixel_to_grid(self, x, y):
        pos_lis = [int(x / 80) - 1, int(y / 80) - 1]
        return pos_lis

    def print_board(self):

        # get the width and height of the image
        board_width = self.bg_image.width()
        board_height = self.bg_image.height()

        # size the window so the image will fill it
        self.master.geometry('%dx%d+%d+%d' %
                             (board_width, board_height, 600, 100))

        self.cv.pack(side='top', fill='both', expand='yes')
        self.cv.create_image(0, 0, image=self.bg_image, anchor='nw')


root = tk.Tk()
root.title('Chess AI')

cv = tk.Canvas(root, width=800, height=800)

game = Game(root, cv)

root.mainloop()
