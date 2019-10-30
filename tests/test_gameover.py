import ataxx
import unittest

class TestMethods(unittest.TestCase):
    def test_gameover(self):
        tests = [
            ["x5o/7/7/7/7/7/o5x x 0 1", False],
            ["x5o/7/2-1-2/7/2-1-2/7/o5x x 0 1", False],
            ["x5o/7/3-3/2-1-2/3-3/7/o5x x 0 1", False],
            ["7/7/7/7/7/7/7 x 0 1", True],
            ["7/7/7/7/7/7/7 o 0 1", True],
            ["x5o/7/7/7/7/7/o5x x 0 1", False],
            ["x5o/7/7/7/7/7/o5x x 99 1", False],
            ["x5o/7/7/7/7/7/o5x x 100 1", True],
            ["x5o/7/7/7/7/7/o5x x 101 1", True],
            ["x6/7/7/7/7/7/7 x 0 1", True],
            ["x6/7/7/7/7/7/7 o 0 1", True],
            ["o6/7/7/7/7/7/7 x 0 1", True],
            ["o6/7/7/7/7/7/7 o 0 1", True],
            ["7/7/7/7/4ooo/4ooo/4oox x 0 1", False],
            ["7/7/7/7/4ooo/4ooo/4oox o 0 1", False],
            ["7/7/7/7/-------/-------/x5o x 0 1", False],
            ["7/7/7/7/-------/-------/x5o o 0 1", False],
            ["7/7/7/7/-------/-------/xxxoooo x 0 1", True],
            ["7/7/7/7/-------/-------/xxxoooo o 0 1", True],
            ["7/7/7/7/---1---/-------/xxxoooo x 0 1", False],
            ["7/7/7/7/---1---/-------/xxxoooo o 0 1", False],
        ]

        for fen, gameover in tests:
            board = ataxx.Board(fen)
            self.assertTrue(board.gameover() == gameover)

            num_moves = len(board.legal_moves())

            if gameover:
                self.assertTrue(num_moves == 0)
            else:
                self.assertTrue(num_moves > 0)
