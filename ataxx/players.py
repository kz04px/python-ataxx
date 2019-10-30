import ataxx
import random

def random_move(board):
    if board.gameover():
        return ataxx.Move.null()

    moves = board.legal_moves()
    return random.choice(moves)

def greedy(board):
    if board.gameover():
        return ataxx.Move.null()

    most = -99999
    moves = []

    for move in board.legal_moves():
        board.makemove(move)
        num_black, num_white, num_gaps, num_empty = board.count()
        board.undo()

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

    return random.choice(moves)

def negamax(board, depth, root=True):
    if depth == 0:
        black, white, _, _ = board.count()
        if board.turn == ataxx.BLACK:
            return black - white
        else:
            return white - black

    best_score = -99999
    best_move = None

    for move in board.legal_moves():
        board.makemove(move)
        score = -negamax(board, depth-1, root=False)

        if score > best_score:
            best_score = score
            best_move = move

        board.undo()

    if root:
        return best_move
    else:
        return best_score

def alphabeta(board, alpha, beta, depth, root=True):
    if depth == 0:
        black, white, _, _ = board.count()
        if board.turn == ataxx.BLACK:
            return black - white
        else:
            return white - black

    best_move = None

    for move in board.legal_moves():
        board.makemove(move)
        score = -alphabeta(board, -beta, -alpha, depth-1, root=False)

        if score > alpha:
            alpha = score
            best_move = move
        if score >= beta:
            score = beta
            board.undo()
            break

        board.undo()

    if root:
        return best_move
    else:
        return alpha
