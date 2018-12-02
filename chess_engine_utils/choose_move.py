import numpy as np
import chess_utilities
import chess_engine_utils
import random

brd_mv=[]
rook_move_white_1=False
rook_move_white_2=False
rook_move_black_1=False
rook_move_black_2=False

king_move_white=False
king_move_black=False





"""def possible_piece(chess, move, piece_index, color):
    move_index = move
    pos_x = move // 8
    pos_y = move - pos_x * 8
    move = [pos_x, pos_y]
    x = piece_index // 8
    y = piece_index - x * 8
    p = [x, y]
    possible = []
    if color == 'white':
        pieces = range(0, 6)
    elif color == 'black':
        pieces = range(6, 12)
    else:
        print('colors : white, black')
    for i in pieces:
        if chess[(i*64) + (8*y)+x] == 1:
            if chess_utilities.legal_move(chess_utilities.figures[i], old_pos=p, new_pos=move, situation=chess):
                possible.append(np.array(p, dtype=np.int8))
    print("Possible= ",possible)
    chess_board_new, ini, fin = chess_engine_utils.make_move(chess_board=chess,
                                                             piece_index=piece_index,
                                                             move_index=move_index)
    if chess_engine_utils.check(chess_board_new, color):
        chess_utilities.print_board(figures=chess_utilities.figures_short, vector=chess_board_new)
        possible = []
    return possible
"""

def possible_piece(chess, move, piece_index, color):
    chs=np.asarray(chess)
    if (chs==chess_engine_utils.chess_board_config_array).all():
        global brd_mv
        brd_mv = []
        print("NEW GAME RESET")
        global rook_move_white_1
        rook_move_white_1 = False
        global rook_move_white_2
        rook_move_white_2 = False
        global king_move_white
        king_move_white = False
        global rook_move_black_1
        rook_move_black_1 = False
        global rook_move_black_2
        rook_move_black_2 = False
        global king_move_black
        king_move_black = False
    move_index = move
    pos_x = move // 8
    pos_y = move - pos_x * 8
    move = [pos_x, pos_y]
    x = piece_index // 8
    y = piece_index - x * 8
    p = [x, y]
    possible = []
    if color == 'white':
        pieces = range(0, 6)
    elif color == 'black':
        pieces = range(6, 12)
    else:
        print('colors : white, black')
    for i in pieces:
        if chess[(i*64) + (8*y)+x] == 1:
            if chess_utilities.legal_move(chess_utilities.figures[i], old_pos=p, new_pos=move, situation=chess,white_rook_1=rook_move_white_1,white_rook_2=rook_move_white_2,black_rook_1=rook_move_black_1,black_rook_2=rook_move_black_2,white_king=king_move_white,black_king=king_move_black):
                possible.append(np.array(p, dtype=np.int8))
    if possible:
        chess_board_new, ini, fin = chess_engine_utils.make_move(chess_board=chess, piece_index=piece_index, move_index=move_index)
        #print(chess_board_new)
        if chess_engine_utils.check(chess_board_new, color, white_rook_1=rook_move_white_1, white_rook_2=rook_move_white_2, black_rook_1=rook_move_black_1, black_rook_2=rook_move_black_2, white_king=king_move_white, black_king=king_move_black):
            possible = []
        le=len(brd_mv)
        occ_cnt=0
        for i in range(le):
            q=np.asarray(brd_mv[i])
            #print("q=", q)
            if (chess_board_new==q).all():
                occ_cnt=occ_cnt+1
        print('count:', occ_cnt)
        if occ_cnt==2:
            possible=[]
        else:
            brd_mv.append(chess_board_new)
            #cnt=cnt+1
        #To check castling
        if ini==1 and p==[0,0]:
            global rook_move_white_1
            rook_move_white_1=True
        if ini==1 and p==[0,7]:
            global rook_move_white_2
            rook_move_white_2 = True
        if ini==4 and p==[0,4]:
            global king_move_white
            king_move_white=True
        if ini==7 and p==[7,0]:
            global rook_move_black_1
            rook_move_black_1=True
        if ini==7 and p==[7,7]:
            global rook_move_black_2
            rook_move_black_2 = True
        if ini==10 and p==[7,4]:
            global king_move_black
            king_move_black=True

    return possible





def legal_move(initial_config, prediction_piece, prediction_move,color):
    prediction_piece_original = np.copy(prediction_piece)
    for p in range(64):
        move_index = np.argmax(prediction_move)
        prediction_move[move_index] = 0
        prediction_piece = np.copy(prediction_piece_original)
        for j in range(64):
            piece_index = np.argmax(prediction_piece)
            prediction_piece[piece_index] = 0
            if possible_piece(chess=initial_config, piece_index=piece_index, move=move_index, color=color):
                return piece_index, move_index
    return -100, -100


def legal_move_max_sum(initial_config, prediction_piece, prediction_move,color):
    prediction_piece = np.tile(prediction_piece, (64, 1))
    prediction_move = np.tile(prediction_move, (64, 1)).T
    s = prediction_move + prediction_piece
    for i in range(4096):
        move = np.argmax(s)
        move = np.unravel_index(move, [64, 64])
        s[move] = 0
        if possible_piece(chess=initial_config, piece_index=move[1], move=move[0], color=color):
            pos_x = move[0] // 8
            pos_y = move[0] % 8
            m = [pos_x, pos_y]
            x = move[1] // 8
            y = move[1] % 8
            p = [x, y]
            print(move[1], p, move[0], m)
            return move[1], move[0]
    return -100, -100


def legal_move_max_sum_random(initial_config, prediction_piece, prediction_move, color):
    random_moves = 3
    prediction_piece = np.tile(prediction_piece, (64, 1))
    prediction_move = np.tile(prediction_move, (64, 1)).T
    s = prediction_move + prediction_piece
    move_v = np.zeros([random_moves, 2])
    v = 0
    count = 0
    for i in range(4096):
        if v > random_moves - 1:
            break
        move = np.argmax(s)
        move = np.unravel_index(move, [64, 64])
        s[move] = 0
        if possible_piece(chess=initial_config, piece_index=move[1], move=move[0], color=color):
            count = count + 1
            pos_x = move[0] // 8
            pos_y = move[0] % 8
            m = [pos_x, pos_y]
            x = move[1] // 8
            y = move[1] % 8
            p = [x, y]
            print(move[1], p, move[0], m)
            move_v[v, 0] = move[1]
            move_v[v, 1] = move[0]
            v = v + 1
    v = random.randrange(count)
    print('choose:', v)
    return int(move_v[v, 0]), int(move_v[v, 1])


def random_player(initial_config, prediction_piece, prediction_move, color):
    s = np.random.rand(64, 64)
    for i in range(4096):
        move = np.argmax(s)
        move = np.unravel_index(move, [64, 64])
        s[move] = 0
        if possible_piece(chess=initial_config, piece_index=move[1], move=move[0], color=color):
            pos_x = move[0] // 8
            pos_y = move[0] % 8
            m = [pos_x, pos_y]
            x = move[1] // 8
            y = move[1] % 8
            p = [x, y]
            print(move[1], p, move[0], m)
            return move[1], move[0]
    return -100, -100