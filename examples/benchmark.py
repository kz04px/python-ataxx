import ataxx
import ataxx.players
import time

def main():
    """
    Time various parts of the library
    """

    fens = [
        "startpos",
        "x4oo/x3ooo/4xxx/3o1x1/1ooo3/1oo3x/6x x"
    ]

    total = 0

    # Perft
    t1 = time.time()
    for fen in fens:
        board = ataxx.Board(fen)
        for i in range(4):
            board.perft(i)
        t2 = time.time()
    total += t2-t1
    print(F"Perft:   {t2-t1:.4f} seconds")

    # Movegen
    t1 = time.time()
    for fen in fens:
        board = ataxx.Board(fen)
        for i in range(10000):
            for move in board.legal_moves():
                assert move
    t2 = time.time()
    total += t2-t1
    print(F"Movegen: {t2-t1:.4f} seconds")

    # FEN parsing
    t1 = time.time()
    for fen in fens:
        for i in range(10000):
            board = ataxx.Board(fen)
    t2 = time.time()
    total += t2-t1
    print(F"Parsing: {t2-t1:.4f} seconds")

    # Negamax
    t1 = time.time()
    for fen in fens:
        board = ataxx.Board(fen)
        move = ataxx.players.negamax(board, 3)
    t2 = time.time()
    total += t2-t1
    print(F"Negamax: {t2-t1:.4f} seconds")

    print(F"Total:   {total:.4f} seconds")

if __name__ == "__main__":
    main()
