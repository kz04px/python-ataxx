import ataxx
import unittest
import random

class TestMethods(unittest.TestCase):
    def test_make_undo(self):
        fens = [
            "x5o/7/7/7/7/7/o5x x 0 1",
            "x5o/7/2-1-2/7/2-1-2/7/o5x o 0 1",
            "x5o/7/2-1-2/3-3/2-1-2/7/o5x x 0 1",
            "x5o/7/3-3/2-1-2/3-3/7/o5x o 0 1",
            "7/3o3/7/3x3/7/7/3oo2 x 0 1"
        ]

        for fen in fens:
            board = ataxx.Board(fen)

            while not board.gameover() and board.fullmove_clock < 200:
                current_fen = board.get_fen()

                # Test all legal moves
                for move in board.legal_moves():
                    board.makemove(move)
                    self.assertTrue(board.get_fen() != current_fen)
                    board.undo()
                    self.assertTrue(board.get_fen() == current_fen)

                # Test null move
                board.makemove(ataxx.Move.null())
                board.undo()
                self.assertTrue(board.get_fen() == current_fen)

                # Pick a random move and keep going
                move = random.choice(board.legal_moves())
                board.makemove(move)

            # Undo every move in the game
            while board.main_line():
                board.undo()

            # Make sure we're back where we started
            self.assertTrue(board.get_fen() == fen)
