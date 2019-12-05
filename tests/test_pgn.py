import ataxx
import ataxx.pgn
import ataxx.players
import unittest
import random
import string
import os

def random_phrase(n):
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.punctuation + string.digits + " ", k=n))

class TestMethods(unittest.TestCase):
    def test_pgn_known(self):
        count = 0
        path = os.path.dirname(__file__) + "/games.pgn"
        for pgn in ataxx.pgn.GameIterator(path):
            self.assertTrue(pgn.headers.get("Valid") == "true")
            self.assertTrue(pgn.headers.get("Event"))
            self.assertTrue(pgn.headers.get("Result"))
            count += 1
        self.assertTrue(count == 7)

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
