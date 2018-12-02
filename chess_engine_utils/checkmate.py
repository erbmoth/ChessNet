import chess_utilities


def check(chessboard, color,white_rook_1,white_rook_2,black_rook_1,black_rook_2,white_king,black_king):
    if color == 'white':
        king = 4
        for i in range(64):
            if chessboard[king * 64 + i] == 1:
                king_pos = [i %8, i//8]
        enemy_pieces = range(6, 12)
    elif color == 'black':
        king = 10
        for i in range(64):
            if chessboard[king * 64 + i] == 1:
                king_pos = [i % 8, i // 8]

        enemy_pieces = range(0, 6)
    else:
        print('colors : white, black')
    for i in enemy_pieces:
        # print('enemy_piece', i)
        for k in range(64):
            if chessboard[i * 64 + k] == 1:
                enemy = [k % 8, k // 8]
                # print('enemy at:', enemy, '(', chess_utilities.figures[i], ')')
                if chess_utilities.legal_move(figure=chess_utilities.figures[i],
                                              situation=chessboard,
                                              new_pos=king_pos,
                                              old_pos=enemy,
                                              white_rook_1=white_rook_1,
                                              white_rook_2=white_rook_2,
                                              black_rook_1=black_rook_1,
                                              black_rook_2=black_rook_2,
                                              white_king=white_king,
                                              black_king=black_king):
                    print(color + ' check ', chess_utilities.figures[i], enemy, 'king', king_pos)
                    chess_utilities.print_board(figures=chess_utilities.figures_short, vector=chessboard)
                    return True
    return False