from keras.models import load_model
import numpy as np
import chess_engine_utils

"""
Functions to choose the move from the prediction
"""
find_white_move = chess_engine_utils.legal_move_max_sum
find_black_move = chess_engine_utils.legal_move_max_sum


def fen_to_768(fen):
    piece = {'P': 0,
             'R': 1,
             'N': 2,
             'B': 3,
             'K': 4,
             'Q': 5,
             'p': 6,
             'r': 7,
             'n': 8,
             'b': 9,
             'k': 10,
             'q': 11}
    chess = np.zeros(768, dtype=np.int8)
    fen_rows = fen.split('/')[0:8]
    fen_rows[7] = fen_rows[7].split()[0]
    index_x = 7
    index_y = 0
    for i in range(8):
        row = fen_rows[i]
        for c in row:
            if c.isnumeric():
                index_y = index_y + int(c)
            else:
                c_index = index_y * 8 + index_x + 64 * piece[c]
                chess[c_index] = 1
                index_y = index_y + 1
        index_x = index_x - 1
        index_y = 0
    return chess


def move_to_768(old_pos, move):
    # missing : en passant
    board = {'a': 0,
             'b': 1,
             'c': 2,
             'd': 3,
             'e': 4,
             'f': 5,
             'g': 6,
             'h': 7}
    le = len(move)
    piece_index = int(board[move[0]]) * 8 + int(move[1]) - 1
    move_index = int(board[move[2]]) * 8 + int(move[3]) - 1
    if piece_index == 32 and (move_index == 16 or move_index == 48) and old_pos[piece_index + 64 * 4] == 1:
        old_pos[piece_index + 64 * 4] = 0
        old_pos[move_index + 64 * 4] = 1
        if move_index == 16:
            old_pos[0 + 64 * 1] = 0
            old_pos[24 + 64 * 1] = 1
        else:
            old_pos[56 + 64 * 1] = 0
            old_pos[40 + 64 * 1] = 1
    elif piece_index == 39 and (move_index == 23 or move_index == 55) and old_pos[piece_index + 64 * 10] == 1:
        old_pos[piece_index + 64 * 10] = 0
        old_pos[move_index + 64 * 10] = 1
        if move_index == 23:
            old_pos[7 + 64 * 7] = 0
            old_pos[31 + 64 * 7] = 1
        else:
            old_pos[63 + 64 * 7] = 0
            old_pos[47 + 64 * 7] = 1
    elif le > 4:  # piece promotion
        for i in range(12):
            if old_pos[piece_index + 64 * i] == 1:
                old_pos[piece_index + 64 * i] = 0
            if old_pos[move_index + 64 * i] == 1:
                old_pos[move_index + 64 * i] = 0
        if move_index == 7 or move_index == 15 or move_index == 23 or move_index == 31 or move_index == 39 or move_index == 47 or move_index == 55 or move_index == 63:
            if move[4] == 'q':
                old_pos[move_index + 64 * 5]=1
            elif move[4] == 'r':
                old_pos[move_index + 64 * 1] = 1
            elif move[4] == 'n':
                old_pos[move_index + 64 * 2] = 1
            elif move[4] == 'b':
                old_pos[move_index + 64 * 3] = 1
        if move_index == 0 or move_index == 8 or move_index == 16 or move_index == 24 or move_index == 32 or move_index == 40 or move_index == 48 or move_index == 56:
            if move[4] == 'q':
                old_pos[move_index+64*11]=1
            elif move[4] == 'r':
                old_pos[move_index + 64 * 7] = 1
            elif move[4] == 'n':
                old_pos[move_index + 64 * 8] = 1
            elif move[4] == 'b':
                old_pos[move_index + 64 * 9] = 1

    else:
        for i in range(12):
            if old_pos[piece_index + 64 * i] == 1:
                old_pos[piece_index + 64 * i] = 0
                old_pos[move_index + 64 * i] = 1
            elif old_pos[move_index + 64 * i] == 1:
                old_pos[move_index + 64 * i] = 0


    return old_pos


class ChessEngineInput:
    @staticmethod
    def uci():
        print("id name ChessNet")
        print("uciok")

    @staticmethod
    def isready():
        print("readyok")

    @staticmethod
    def register():
        print("register name ChessNet code 12345")

    @staticmethod
    def ucinewgame():
        print("isready")

    @staticmethod
    def position(chess_board, fen=None, moves=None):
        #method for converting fen to our representation
        if fen:
            chess_board = fen_to_768(fen)
        if moves:
            chess_board = move_to_768(chess_board, moves)
        return chess_board

    @staticmethod
    def go(board, move_number, models):
        move_number, chess_board, move = models.chess_move_uci(chess_board=board, mv=move_number)
        EngineOutput.bestmove(move)
        return move_number, chess_board

    @staticmethod
    def quit():
        exit(0)

    @staticmethod
    def stop():
        pass


class EngineOutput:
    @staticmethod
    def id():
        print('id name ChessNet')
        print('id author Malte Lindenau')

    @staticmethod
    def uciok():
        print('uciok')

    @staticmethod
    def readyok():
        print('readyok')

    @staticmethod
    def bestmove(move):
        print('bestmove ' + move)

    @staticmethod
    def copyprotection():
        print('copyprotection')

    @staticmethod
    def registration():
        print('registration')

    @staticmethod
    def info():
        pass

    @staticmethod
    def option():
        pass


def find_piece(val, board):
    brd = np.reshape(board, [12, 64])
    for i in range(12):
        if brd[i, val] == 1:
            return i
    return -1


def conv_move(piece_index, move_index, initial_piece, final_piece):
    # chess_figs = ['', 'R', 'N', 'B', 'K', 'Q']
    chess_board_index = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    final_x = move_index // 8 + 1
    final_y = move_index % 8
    initial_x = piece_index // 8 + 1
    initial_y = piece_index % 8
    move = chess_board_index[initial_y] + str(initial_x) + chess_board_index[final_y] + str(final_x)
    return move
    # if (initial_piece == 0 or initial_piece == 6) and final_piece < 0:
    #     move = chess_board_index[initial_y]+str(initial_x)+"-"+chess_board_index[final_y]+str(final_x)
    #     return move
    # elif final_piece < 0:
    #     if initial_piece > 5:
    #         initial_piece = initial_piece-6
    #     move = chess_figs[initial_piece]+chess_board_index[initial_y] + str(initial_x) + "-" + chess_board_index[
    #         final_y] + str(final_x)
    #     return move
    # elif (initial_piece == 0 or initial_piece == 6) and final_piece > 0:
    #     move = chess_board_index[initial_y] + str(initial_x) + "x" + chess_board_index[
    #         final_y] + str(final_x)
    #     return move
    # elif final_piece >= 0:
    #     if initial_piece > 5:
    #         initial_piece = initial_piece-6
    #     move = chess_figs[initial_piece] + chess_board_index[initial_y] + str(initial_x) + "x" + \
    #            chess_board_index[final_y] + str(final_x)
    #     return move
    # else:
    #     move = "could not conv"
    #     return move


def make_move(chess_board, piece_index, move_index):
    chess_board_c = np.copy(chess_board)
    for i in range(12):
        pt = np.reshape(chess_board_c[i * 64:(i + 1) * 64], [8, 8])
        pr = np.transpose(pt)
        chess_board_c[i * 64:(i + 1) * 64] = np.reshape(pr, [64, ])
    ini = find_piece(piece_index, chess_board_c)
    chess_board_c[ini * 64 + piece_index] = 0
    fin = find_piece(move_index, chess_board_c)
    if fin >= 0:
        chess_board_c[fin * 64 + move_index] = 0
        chess_board_c[ini * 64 + move_index] = 1
    else:
        chess_board_c[ini * 64 + move_index] = 1
    for i in range(12):
        pt = np.reshape(chess_board_c[i * 64:(i + 1) * 64], [8, 8])
        pr = np.transpose(pt)
        chess_board_c[i * 64:(i + 1) * 64] = np.reshape(pr, [64, ])
    return chess_board_c, ini, fin


class ChessModels:
    def __init__(self):
        self.whiteModel128 = False
        self.whiteModel128_old = False
        self.blackModel128 = False
        self.blackModel128_old = False
        self.model_white = None
        self.model_black = None
        self.model_piece_white = None
        self.model_move_white = None
        self.model_piece_black = None
        self.model_move_black = None
        self.brd_store = []

    def load_models(self, settings):
        print(settings.s)
        if settings.s['whiteModel128'] == 'True':
            self.whiteModel128 = True
            self.model_white = load_model(settings.s['whiteModel'])
        elif settings.s['whiteModel128'] == 'old':
            self.whiteModel128_old = True
            self.model_white = load_model(settings.s['whiteModel'])
        else:
            self.model_piece_white = load_model(settings.s['blackPieceModel'])
            self.model_move_white = load_model(settings.s['blackMoveModel'])
        if settings.s['blackModel128'] == 'True':
            self.blackModel128 = True
            self.model_black = load_model(settings.s['blackModel'])
        elif settings.s['blackModel128'] == 'old':
            self.blackModel128_old = True
            self.model_black = load_model(settings.s['blackModel'])
        else:
            self.model_piece_black = load_model(settings.s['blackPieceModel'])
            self.model_move_black = load_model(settings.s['blackMoveModel'])

    def chess_move_uci(self, chess_board, mv):
        if mv % 2 == 0:  # white move
            chess_board = np.reshape(chess_board, (1, 768))
            if self.whiteModel128:
                [prediction_piece, prediction_move] = self.model_white.predict(chess_board, batch_size=1, verbose=0)
            elif self.whiteModel128_old:
                p = self.model_white.predict(chess_board, batch_size=1, verbose=0)
                prediction_piece = p[:, 0:64]
                prediction_move = p[:, 64:128]
            else:
                prediction_piece = self.model_piece_white.predict(chess_board, batch_size=1, verbose=0)
                prediction_move = self.model_move_white.predict(chess_board, batch_size=1, verbose=0)
            prediction_move = np.squeeze(prediction_move)
            prediction_piece = np.squeeze(prediction_piece)
            chess_board = np.squeeze(chess_board)
            piece_index, move_index = find_white_move(chess_board, prediction_piece, prediction_move,color='white')
            if piece_index == -100 and move_index == -100:
                print("No White move")
                return -123
            chess_board, ini, fin = make_move(chess_board, piece_index, move_index)
            move = conv_move(piece_index,move_index, ini, fin)
            return mv, chess_board, move
        elif mv % 2 != 0:  # black move
            chess_board = np.reshape(chess_board, (1, 768))
            if self.blackModel128:
                [prediction_piece, prediction_move] = self.model_black.predict(chess_board, batch_size=1, verbose=0)
            elif self.blackModel128_old:
                p = self.model_black.predict(chess_board, batch_size=1, verbose=0)
                prediction_piece = p[:, 0:64]
                prediction_move = p[:, 64:128]
            else:
                prediction_piece = self.model_piece_black.predict(chess_board, batch_size=1, verbose=0)
                prediction_move = self.model_move_black.predict(chess_board, batch_size=1, verbose=0)
            prediction_move = np.squeeze(prediction_move)
            prediction_piece = np.squeeze(prediction_piece)
            chess_board = np.squeeze(chess_board)
            piece_index, move_index = find_black_move(chess_board, prediction_piece, prediction_move,color='black')
            if piece_index == -100 and move_index == -100:
                print("No Black move")
                return -123
            chess_board, ini, fin = make_move(chess_board, piece_index, move_index)
            move = conv_move(piece_index, move_index, ini, fin)
            return mv, chess_board, move