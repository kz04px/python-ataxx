import ataxx
import ataxx.players

def main():
    """
    A game between the random player and the greedy player
    """
    board = ataxx.Board()

    while not board.gameover():
        if board.turn == ataxx.BLACK:
            move = ataxx.players.random_move(board)
        else:
            move = ataxx.players.greedy(board)

        board.makemove(move)

    moves = " ".join([str(move) for move in board.main_line()])
    print(F"Result: {board.result()}")
    print(F"Moves:  {moves}")

if __name__ == '__main__':
    main()
