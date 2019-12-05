import ataxx
import ataxx.pgn
import ataxx.players
import unittest
import random
import string

pgns = [
"""[Event "Example 1"]
[Site "?"]
[Round "-"]
[White "Player 1"]
[Black "Player 2"]
[Result "*"]
[FEN "x5o/7/7/7/7/7/o5x x"]

1. a7c5 a2 2. g2 *""",
"""[Event "Example 2"]
[Site "?"]
[Round "-"]
[White "Player 1"]
[Black "Player 2"]
[Result "*"]
[FEN "x5o/7/7/7/7/7/o5x x"]

1. a7c5 { Test 123 } 1... a2 { Test } 2. g2 *""",

"""[Event "Example 3"]
[Site "?"]
[Round "-"]
[White "Player 1"]
[Black "Player 2"]
[Result "*"]
[FEN "x5o/7/7/7/7/7/o5x x"]

1. a7c7 (1. a7c5 { Test }) 1... g7f5 (1... a2 { Test } 2. g2 (2. f2 { Test })) 2. g1f3 a1b3 { Test 123 } *""",

"""[Event "Example 4"]
[Site "?"]
[Round "-"]
[White "Player 1"]
[Black "Player 2"]
[Result "*"]
[FEN "x5o/7/7/7/7/7/o5x x"]

1. a7c7 { Test } (1. a7c5 { Test }) 1... g7f5 (1... a2 { Test } 2. g2 (2. f2 { Test } 2... a1c2)) 2. g1f3 a1b3 { Test 123 } *"""
]

def random_phrase(n):
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.punctuation + string.digits + " ", k=n))

class TestMethods(unittest.TestCase):
    def test_pgn_known(self):
        # Test some known pgn strings
        for pgn in pgns:
            parsed = ataxx.pgn.parse(pgn)
            del parsed.headers["Date"]
            self.assertTrue(str(parsed) == pgn)

    def test_pgn_create(self):
        # Create a pgn ourselves
        game = ataxx.pgn.Game()
        game.headers["Event"] = "Example"
        game.headers["Site"] = "?"
        game.headers["Round"] = "-"
        game.headers["White"] = "?"
        game.headers["Black"] = "?"
        game.headers["Result"] = "*"
        game.headers["FEN"] = ataxx.FEN_STARTPOS
        del game.headers["Date"]
        node = game.add_variation(ataxx.Move.from_san("g2"), comment="First move")
        node = node.add_variation(ataxx.Move.from_san("a1a3"), comment="Second move")
        self.assertTrue(str(game) == "[Event \"Example\"]\n[Site \"?\"]\n[Round \"-\"]\n[White \"?\"]\n[Black \"?\"]\n[Result \"*\"]\n[FEN \"x5o/7/7/7/7/7/o5x x 0 1\"]\n\n1. g2 { First move } a1a3 { Second move } *")

    def test_pgn_random(self):
        # Try parse some random games
        # These won't have variations or comments in them
        for _ in range(10):
            board = ataxx.Board()
            while not board.gameover() and board.halfmove_clock < 500:
                move = ataxx.players.random_move(board)
                board.makemove(move)

            pgn = ataxx.pgn.Game()
            pgn.headers["Event"]  = random_phrase(12)
            pgn.headers["Black"]  = random_phrase(12)
            pgn.headers["White"]  = random_phrase(12)
            pgn.headers["FEN"]    = ataxx.FEN_STARTPOS
            pgn.headers["Result"] = board.result()
            pgn.from_board(board)

            # Human readable pgn string
            pgn_string = str(pgn)

            # Test: pgn string ---> pgn ---> pgn string
            self.assertTrue(str(ataxx.pgn.parse(pgn_string)) == pgn_string)

            # Check the pgn main line matches the board
            moves = [n.move for n in pgn.main_line()]
            self.assertTrue(moves == board.main_line())
