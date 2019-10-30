import ataxx
import unittest
import random

class TestMethods(unittest.TestCase):
    def test_history(self):
        for _ in range(10):
            history = []

            # Play random moves on the board
            board1 = ataxx.Board("startpos")
            while not board1.gameover() and len(history) < 50:
                moves = board1.legal_moves()
                move = random.choice(moves)
                board1.makemove(move)
                history.append(move)

            self.assertTrue(board1.main_line() == history)

            # Replay the moves on a new board
            board2 = ataxx.Board("startpos")
            for move in board1.main_line():
                self.assertTrue(move in board2.legal_moves())
                board2.makemove(move)

            self.assertTrue(board1.main_line() == board2.main_line())
            self.assertTrue(board1.get_fen() == board2.get_fen())
