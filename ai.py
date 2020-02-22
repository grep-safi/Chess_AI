def minimax(mama_board, depth, alpha, beta, AI_move, first_layer):
    if depth == 0:
        board_val = mama_board[1]
        mama_board[0].print_grid()
        return [mama_board, board_val]
    if AI_move:
        max_eval = [None, -1000000]  # some very small number
        baby_boards = get_children(mama_board, enemy=False)
        for baby_board in baby_boards:
            eval = minimax(baby_board, depth - 1, alpha, beta, False, False)
            if (max_eval[1] < eval[1]):
                max_eval = eval
                if first_layer:
                    max_eval = [baby_board, eval[1]]

            if (alpha[1] < eval[1]):
                alpha = eval
                if first_layer:
                    alpha = [baby_board, eval[1]]

            if beta[1] <= alpha[1]:
                break

        return max_eval
    else:
        min_eval = [None, 1000000]  # some very large number
        baby_boards = get_children(mama_board, enemy=True)
        for baby_board in baby_boards:
            eval = minimax(baby_board, depth - 1, alpha, beta, True, False)
            if (min_eval[1] > eval[1]):
                min_eval = eval
                if first_layer:
                    min_eval = [baby_board, eval[1]]

            if (beta[1] > eval[1]):
                beta = eval
                if first_layer:
                    beta = [baby_board, eval[1]]

            if beta[1] <= alpha[1]:
                break

        return min_eval


def get_children(m_board, enemy=True):
    board = m_board[0]
    pieces = board.black_pieces
    if enemy:
        pieces = board.white_pieces

#    print('Start ----------------------------------------------------->')
#    board.print_grid()

    children = []
    for piece in pieces:
        possible_moves = piece.possible_moves(board.matrix)
        for move in possible_moves:
            piece_move = piece.tentative_move(move[0], move[1], board)
            prev_x, prev_y = piece_move[0], piece_move[1]
            viable_move = False
            tried_castling = False
            print('i am the piece move', piece_move)
            if len(piece_move) == 6 and piece_move[5]:
                viable_move = True
                tried_castling = True
            elif len(piece_move) == 3:
                viable_move = not (board.is_illegal_state(piece.color))

            if viable_move:
                piece.first = False
                new_child = [board.clone(), board.evaluate_board(), prev_x, prev_y, piece.x, piece.y]
                children.append(new_child)

            if tried_castling:
                prev_king_x, prev_king_y, prev_rook_x, prev_rook_y, rook, success = piece_move
                piece.revert(prev_king_x, prev_king_y, None, board)
                rook.revert(prev_rook_x, prev_rook_y, None, board)
                rook.first = True
            else:
                prev_x, prev_y, target_piece = piece_move
                piece.revert(prev_x, prev_y, target_piece, board)

            piece.first = True

#    board.print_grid()
#    print('End ----------------------------------------------------->')
    return children
