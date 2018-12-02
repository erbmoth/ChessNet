import numpy as np
import chess_utilities


def fields_between_positions(old_pos, new_pos, board):
    distance = max([abs(old_pos[0] - new_pos[0]), abs(old_pos[1] - new_pos[1])]) - 1
    step_x = 0
    step_y = 0
    if old_pos[0] - new_pos[0] != 0:
        step_x = (new_pos[0] - old_pos[0]) / abs(old_pos[0] - new_pos[0])
    if old_pos[1] - new_pos[1] != 0:
        step_y = (new_pos[1] - old_pos[1]) / abs(old_pos[1] - new_pos[1])
    for i in range(distance):
        x = int(old_pos[0] + (i + 1) * step_x)
        y = int(old_pos[1] + (i + 1) * step_y)
        if board[x, y] != 0:
            return False
    return True


def legal_move(figure,
               old_pos,
               new_pos,
               situation,
               white_rook_1=False,
               white_rook_2=False,
               black_rook_1=False,
               black_rook_2=False,
               white_king=False,
               black_king=False,
               check_en_passant=False):
    chess = np.zeros([8, 8])
    for i in range(6):
        chess = chess + np.reshape(situation[i*64:(i+1)*64], [8, 8])
    for i in range(6, 12):
        chess = chess - np.reshape(situation[i*64:(i+1)*64], [8, 8])
    chess = np.transpose(chess)
    if chess[old_pos[0], old_pos[1]] == chess[new_pos[0], new_pos[1]]:
        return False
    # pos[0] = numbers, pos[1] = letters, [0,0] = bottom left field (a1)
    if chess[old_pos[0], old_pos[1]] == 0:
        return False
    if old_pos[0] == new_pos[0] and old_pos[1] == new_pos[1]:
        return False
    if old_pos[0] < 0 or old_pos[1] < 0 or new_pos[0] < 0 or new_pos[1] < 0:
        return False
    if figure == 'white pawn':
        if new_pos == [old_pos[0] + 1, old_pos[1]] and chess[new_pos[0], new_pos[1]] == 0:
            return True
        elif new_pos == [3, old_pos[1]] and chess[2, old_pos[1]] == 0 and chess[new_pos[0], new_pos[1]] == 0 and new_pos[0]>old_pos[0]:
            return True
        # en passant
        elif new_pos[0] == 5 and chess[4, new_pos[1]] == -1 and check_en_passant:
            return True
        elif new_pos == [old_pos[0] + 1, old_pos[1] + 1] and chess[new_pos[0], new_pos[1]] == -1:
            return True
        elif new_pos == [old_pos[0] + 1, old_pos[1] - 1] and chess[new_pos[0], new_pos[1]] == -1:
            return True
        # print('Pawn error', old_pos, new_pos)
        return False
    elif figure == 'white rook':
        if new_pos[0] == old_pos[0] and fields_between_positions(old_pos, new_pos, chess):
            return True
        elif new_pos[1] == old_pos[1] and fields_between_positions(old_pos, new_pos, chess):
            return True
        else:
            # print('Rook error', old_pos, new_pos)
            return False
    elif figure == 'white knight':
        if new_pos == [old_pos[0] + 2, old_pos[1] + 1]:
            return True
        elif new_pos == [old_pos[0] + 2, old_pos[1] - 1]:
            return True
        elif new_pos == [old_pos[0] - 2, old_pos[1] + 1]:
            return True
        elif new_pos == [old_pos[0] - 2, old_pos[1] - 1]:
            return True
        elif new_pos == [old_pos[0] + 1, old_pos[1] + 2]:
            return True
        elif new_pos == [old_pos[0] + 1, old_pos[1] - 2]:
            return True
        elif new_pos == [old_pos[0] - 1, old_pos[1] + 2]:
            return True
        elif new_pos == [old_pos[0] - 1, old_pos[1] - 2]:
            return True
        # print('Knight error', old_pos, new_pos)
        return False
    elif figure == 'white bishop':
        diff_x = abs(old_pos[0] - new_pos[0])
        diff_y = abs(old_pos[1] - new_pos[1])
        if diff_x == diff_y and fields_between_positions(old_pos, new_pos, chess):
            return True
        # print('Bishop error', old_pos, new_pos)
        return False
    elif figure == 'white king':
        diff_x = abs(old_pos[0] - new_pos[0])
        diff_y = abs(old_pos[1] - new_pos[1])
        if diff_y == 1 and diff_x == 0:
            return True
        elif diff_x == 1 and diff_y == 0:
            return True
        elif diff_x == 1 and diff_y == 1:
            return True
        elif old_pos == [0, 4]:
            if (new_pos == [0, 2] and
                        chess[0, 0] == 1 and
                        chess[0, 1] == 0 and
                        chess[0, 2] == 0 and
                        chess[0, 3] == 0 and
                        white_rook_1 == False and
                        white_king == False ) or \
                    (new_pos == [0, 6] and
                             chess[0, 7] == 1 and
                             chess[0, 5] == 0 and
                             chess[0, 6] == 0 and
                             white_rook_2 == False and
                             white_king == False):
                return True
        # print('King error', old_pos, new_pos)
        return False
    elif figure == 'white queen':
        diff_x = abs(old_pos[0] - new_pos[0])
        diff_y = abs(old_pos[1] - new_pos[1])
        if (diff_x == diff_y or new_pos[0] == old_pos[0] or new_pos[1] == old_pos[1]) \
                and fields_between_positions(old_pos, new_pos, chess):
            return True
        # print('Queen error', old_pos, new_pos)
        return False
    elif figure == 'black pawn':
        if new_pos == [old_pos[0] - 1, old_pos[1]] and chess[new_pos[0], new_pos[1]] == 0:
            return True
        elif new_pos == [4, old_pos[1]] and chess[5, old_pos[1]] == 0 and chess[new_pos[0], new_pos[1]] == 0 and new_pos[0]<old_pos[0]:
            return True
        # en passant
        elif new_pos[0] == 2 and chess[3, new_pos[1]] == 1 and check_en_passant:
            return True
        elif new_pos == [old_pos[0] - 1, old_pos[1] + 1] and chess[new_pos[0], new_pos[1]] == 1:
            return True
        elif new_pos == [old_pos[0] - 1, old_pos[1] - 1] and chess[new_pos[0], new_pos[1]] == 1:
            return True
        # print('Pawn error', old_pos, new_pos)
        return False
    elif figure == 'black rook':
        if new_pos[0] == old_pos[0] and fields_between_positions(old_pos, new_pos, chess):
            return True
        elif new_pos[1] == old_pos[1] and fields_between_positions(old_pos, new_pos, chess):
            return True
        else:
            # print('Rook error', old_pos, new_pos)
            return False
    elif figure == 'black knight':
        if new_pos == [old_pos[0] + 2, old_pos[1] + 1]:
            return True
        elif new_pos == [old_pos[0] + 2, old_pos[1] - 1]:
            return True
        elif new_pos == [old_pos[0] - 2, old_pos[1] + 1]:
            return True
        elif new_pos == [old_pos[0] - 2, old_pos[1] - 1]:
            return True
        elif new_pos == [old_pos[0] + 1, old_pos[1] + 2]:
            return True
        elif new_pos == [old_pos[0] + 1, old_pos[1] - 2]:
            return True
        elif new_pos == [old_pos[0] - 1, old_pos[1] + 2]:
            return True
        elif new_pos == [old_pos[0] - 1, old_pos[1] - 2]:
            return True
        # print('Knight error', old_pos, new_pos)
        return False
    elif figure == 'black bishop':
        diff_x = abs(old_pos[0] - new_pos[0])
        diff_y = abs(old_pos[1] - new_pos[1])
        if diff_x == diff_y and fields_between_positions(old_pos, new_pos, chess):
            return True
        # print('Bishop error', old_pos, new_pos)
        return False
    elif figure == 'black king':
        diff_x = abs(old_pos[0] - new_pos[0])
        diff_y = abs(old_pos[1] - new_pos[1])
        if diff_y == 1 and diff_x == 0:
            return True
        elif diff_x == 1 and diff_y == 0:
            return True
        elif diff_x == 1 and diff_y == 1:
            return True
        elif old_pos == [7, 4]:
            #if new_pos == [7, 2] and  or new_pos == [7, 6]:
            if (new_pos == [7, 2] and
                        chess[7, 0] == -1 and
                        chess[7, 1] == 0 and
                        chess[7, 2] == 0 and
                        chess[7, 3] == 0 and
                        black_rook_1 == False and
                        black_king == False) or \
                    (new_pos == [7, 6] and
                             chess[7, 7] == -1 and
                             chess[7, 5] == 0 and
                             chess[7, 6] == 0 and
                             black_rook_2 == False and
                             black_king == False):
                return True
        # print('King error', old_pos, new_pos)
        return False
    elif figure == 'black queen':
        diff_x = abs(old_pos[0] - new_pos[0])
        diff_y = abs(old_pos[1] - new_pos[1])
        if (diff_x == diff_y or new_pos[0] == old_pos[0] or new_pos[1] == old_pos[1]) \
                and fields_between_positions(old_pos, new_pos, chess):
            return True
        # print('Queen error', old_pos, new_pos)
        return False
    return True


def figure_count(x, y, print_errors=False):
    figure_index = -1
    figure_pos = [-1, -1]
    move = [-1, -1]
    for i in range(64):
        if y[i] == 1:
            figure_index = i
            pos_x = figure_index // 8
            pos_y = figure_index - pos_x * 8
            figure_index = pos_y * 8 + pos_x
            figure_pos = [pos_x, pos_y]
            # print(i, ' ', pos_x, ' ', pos_y, ' ', figure_pos)
            break
    for i in range(64):
        if y[i+64] == 1:
            move = i
            pos_x = move // 8
            pos_y = move - pos_x * 8
            move = [pos_x, pos_y]
            # print(i, ' ', pos_x, ' ', pos_y, ' ', figure_pos)
            break
    if figure_index == -1:
        return -13
    for i in range(12):
        if x[figure_index + 64 * i] == 1:
            if legal_move(chess_utilities.figures[i], figure_pos, move, x, check_en_passant=True):
                return i
            else:
                if print_errors:
                    print(figure_pos, move, chess_utilities.figures[i])
                    print(np.reshape(x[0:64], [8, 8]))
                    chess_utilities.print_board(x, chess_utilities.figures_short)
                return -i - 1
    return -13