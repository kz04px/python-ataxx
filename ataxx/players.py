import ataxx
import random
import copy

def random_move(board):
    moves = board.legal_moves()
    if moves == []:
        return None
    return random.choice(moves)

def greedy(board):
    most = -1
    moves = []

    for move in board.legal_moves():
        nboard = copy.deepcopy(board)
        nboard.makemove(move)
        num_black, num_white, num_gaps, num_empty = nboard.count()

        # Maximise our advantage
        if board.turn == ataxx.BLACK:
            score = num_black - num_white
        else:
            score = num_white - num_black

        # Track most captures
        if score > most:
            most = score
            moves = []

        if score == most:
            moves.append(move)

    # No legal moves
    if most < 0:
        return None

    return random.choice(moves)
