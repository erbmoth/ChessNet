import numpy as np


def print_board(vector, figures):
    board = np.ones(64) * -1
    for i in range(64):
        for k in range(12):
            if vector[i + 64 * k] == 1:
                board[i] = k
    board = np.reshape(board, [8, 8])
    print('     x=0  x=1  x=2  x=3  x=4  x=5  x=6  x=7')
    print('    -----------------------------------------')
    for y in [7, 6, 5, 4, 3, 2, 1, 0]:
        line = 'y=' + str(y) + ' |'
        for x in range(8):
            if board[x, y] == -1:
                line = line + '    |'
            else:
                line = line + figures[board[x, y]] + '   |'
        print(line)
        print('    -----------------------------------------')