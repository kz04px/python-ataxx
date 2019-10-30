import ataxx
import ataxx.pgn
import unittest
import random
import string

pgns = [
"""[Event "Example 1"]
[Black "Player 1"]
[White "Player 2"]
[UTCDate "1970.01.01"]
[UTCTime "00:00:00"]
[FEN "x5o/7/7/7/7/7/o5x x"]
[Result "*"]

1. a7c5 a2 2. g2 *""",
"""[Event "Example 2"]
[Black "Player 1"]
[White "Player 2"]
[UTCDate "1970.01.01"]
[UTCTime "00:00:00"]
[FEN "x5o/7/7/7/7/7/o5x x"]
[Result "*"]

1. a7c5 { Test 123 } 1... a2 { Test } 2. g2 *""",

"""[Event "Example 3"]
[Black "Player 1"]
[White "Player 2"]
[UTCDate "1970.01.01"]
[UTCTime "00:00:00"]
[FEN "x5o/7/7/7/7/7/o5x x"]
[Result "*"]

1. a7c7 (1. a7c5 { Test }) 1... g7f5 (1... a2 { Test } 2. g2 (2. f2 { Test })) 2. g1f3 a1b3 { Test 123 } *""",

"""[Event "Example 4"]
[Black "Player 1"]
[White "Player 2"]
[UTCDate "1970.01.01"]
[UTCTime "00:00:00"]
[FEN "x5o/7/7/7/7/7/o5x x"]
[Result "*"]

1. a7c7 { Test } (1. a7c5 { Test }) 1... g7f5 (1... a2 { Test } 2. g2 (2. f2 { Test } 2... a1c2)) 2. g1f3 a1b3 { Test 123 } *"""
]

def random_phrase(n):
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.punctuation + string.digits + " ", k=n))

class TestMethods(unittest.TestCase):
    def test_pgn_known(self):
        # Test some known pgn strings
        for pgn in pgns:
            self.assertTrue(str(ataxx.pgn.parse(pgn)) == pgn)

    def test_pgn_create(self):
        # Create a pgn ourselves
        game = ataxx.pgn.Game()
        game.headers["FEN"] = ataxx.FEN_STARTPOS
        game.headers["Result"] = "*"
        node = game.add_variation(ataxx.Move.from_san("g2"), comment="First move")
        node = node.add_variation(ataxx.Move.from_san("a1a3"), comment="Second move")
        self.assertTrue(str(game) == "[Event \"Example\"]\n[FEN \"x5o/7/7/7/7/7/o5x x 0 1\"]\n[Result \"*\"]\n\n1. g2 { First move } a1a3 { Second move } *")

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
