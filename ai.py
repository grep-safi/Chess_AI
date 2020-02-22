def minimax(mama_board, depth, AI_move, first_layer):
    if depth == 0:
        board_val = mama_board[1]
        print('New board variation')
        mama_board[0].print_grid()
        print('Finished new board variation')
        return [mama_board, board_val]
    if AI_move:
        max_eval = [None, -1000000]  # some very small number
        baby_boards = get_children(mama_board, enemy=False)
        for baby_board in baby_boards:
            eval = minimax(baby_board, depth - 1, False, False)
            if (max_eval[1] < eval[1]):
                max_eval = eval
            if (first_layer):
                max_eval = [baby_board, 0]
        return max_eval
    else:
        min_eval = [None, 1000000]  # some very large number
        baby_boards = get_children(mama_board, enemy=True)
        for baby_board in baby_boards:
            eval = minimax(baby_board, depth - 1, True, False)
            if (min_eval[1] > eval[1]):
                min_eval = eval
            if (first_layer):
                max_eval = [baby_board, 0]
        return min_eval


def get_children(m_board, enemy=True):
    board = m_board[0]
    pieces = board.black_pieces
    if enemy:
        pieces = board.white_pieces


    print('Start ----------------------------------------------------->')
    board.print_grid()

    children = []
    for piece in pieces:
        possible_moves = piece.possible_moves(board.matrix)
        for move in possible_moves:
            prev_x, prev_y, target_piece = piece.tentative_move(move[0], move[1], board)
            viable_move = not (board.is_illegal_state(piece.color))
            if viable_move:
                piece.first = False
                new_child = [board.clone(), board.evaluate_board(), prev_x, prev_y, piece.x, piece.y]
                children.append(new_child)

            piece.first = True
            piece.revert(prev_x, prev_y, target_piece, board)

    board.print_grid()
    print('End ----------------------------------------------------->')
    return children