import ataxx

def main():
    """
    Play a game solo
    """
    fen = input("FEN: ")
    if fen == "":
        fen = "startpos"
    board = ataxx.Board(fen)

    while not board.gameover():
        print("\n\n\n")
        print(F"FEN: {board.get_fen()}")
        print(board)
        try:
            move_string = input("Move: ")
            move = ataxx.Move.from_san(move_string)
            if board.is_legal(move):
                board.makemove(move)
            else:
                print(F"Illegal move: {move}")
        except KeyboardInterrupt:
            print("")
            break

    print(F"Result: {board.result()}")

if __name__ == '__main__':
    main()
