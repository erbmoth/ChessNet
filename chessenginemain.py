#!/nfshome/thombre/master_keras/bin/python3
import chess_utilities
import time
from chess_engine_utils.uciinterface import *
from chess_engine_utils.settings import *


def wait_for_command():
    cmd = input()
    return cmd


def main():
    r = Settings(file='/nfshome/lindenau/PycharmProjects/test/settings.csv')
    models = ChessModels()
    models.load_models(settings=r)
    board = fen_to_768('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    move_number = 0
    run = True
    while run:
        cmd_full = wait_for_command()
        cmd_full = cmd_full.split()
        cmd = cmd_full[0]
        if cmd == 'uci':
            EngineOutput.uciok()
        elif cmd == 'debug':
            pass
        elif cmd == 'isready':
            EngineOutput.readyok()
        elif cmd == 'setoption':
            pass
        elif cmd == 'register':
            pass
        elif cmd == 'ucinewgame':
            ChessEngineInput.ucinewgame()
        elif cmd == 'position':
            moves = []
            if cmd_full[1] == 'startpos':
                fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
                board = fen_to_768(fen)
            if cmd_full[1] == 'fen':
                fenstr = cmd_full[2]
                sideplay = cmd_full[3]
                castling = cmd_full[4]
                enpassant = cmd_full[5]
                half_move = cmd_full[6]
                full_move = cmd_full[7]
                if sideplay == 'w':
                    move_number = 0
                elif sideplay == 'b':
                    move_number = 1
                board = fen_to_768(fenstr)
            if len(cmd_full) > 2:
                if cmd_full[1] == 'moves':
                    moves = cmd_full[2:]
                    if len(moves) % 2 == 0:
                        move_number = 0
                    else:
                        move_number = 1
            if len(cmd_full) > 3:
                if cmd_full[2] == 'moves':
                    moves = cmd_full[3:]
                    if len(moves) % 2 == 0:
                        move_number = 0
                    else:
                        move_number = 1
            if len(cmd_full) > 8:
                if cmd_full[8] == 'moves':
                    moves = cmd_full[9:]
                    if len(moves) % 2 == 0:
                        move_number = 0
                    else:
                        move_number = 1
            for m in moves:
                board = move_to_768(old_pos=board, move=m)
        elif cmd == 'go':
            t = time.clock()
            chess_utilities.print_board(board, chess_utilities.figures_short)
            move_number, chess_board = ChessEngineInput.go(board=board, move_number=move_number, models=models)
            print(time.clock() - t)
        elif cmd == 'stop':
            ChessEngineInput.stop()
        elif cmd == 'ponderhit':
            pass
        elif cmd == 'quit':
            run = False
        else:
            print(cmd, 'not recognized')


if __name__ == '__main__':
    main()