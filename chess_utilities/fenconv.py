import numpy as np
import changedatt
import att1
import time
import psutil


def fen_conv(vector, figures,ini,fina):
    board = np.ones(64) * -1
    for i in range(64):
        for k in range(12):
            if vector[i + 64 * k] == 1:
                board[i] = k
    board = np.reshape(board, [8, 8])
    fin=""
    for y in [7, 6, 5, 4, 3, 2, 1, 0]:
        s=""
        cnt = 0
        for x in range(8):

            if board[x, y] == -1:
                cnt=cnt+1
            else:
                if cnt!=0:
                    s=s+str(cnt)+figures[board[x, y]]
                    cnt = 0
                else:
                    s=s+figures[board[x, y]]
            if x==7 and cnt!=0:
                s=s+str(cnt)
        if fin=="":
            fin=fin+s
        else:
            fin=fin+"/"+s
    print(fin)
    #renderer = att1.DrawChessPosition()
    renderer = changedatt.DrawChessPosition(ini,fina)
    board = renderer.draw(fin)
    board.show()
    time.sleep(6)

    for proc in psutil.process_iter():
        if proc.name() == "display":
            proc.kill()