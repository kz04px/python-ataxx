import ataxx
import unittest

class TestMethods(unittest.TestCase):
    def test_pass(self):
        tests = [
            ["x5o/7/7/7/7/7/o5x x 0 1", False],
            ["x5o/7/2-1-2/7/2-1-2/7/o5x x 0 1", False],
            ["x5o/7/3-3/2-1-2/3-3/7/o5x x 0 1", False],
            ["7/7/7/7/4ooo/4ooo/4oox x 0 1", True],
            ["7/7/7/7/4ooo/4ooo/4oox o 0 1", False],
            ["7/7/7/7/4xxx/4xxx/4xxo x 0 1", False],
            ["7/7/7/7/4xxx/4xxx/4xxo o 0 1", True],
            ["xxxxxxx/-------/-------/7/7/-------/ooooooo x 0 1", True],
            ["xxxxxxx/-------/-------/7/7/-------/ooooooo o 0 1", False],
            ["ooooooo/-------/-------/7/7/-------/xxxxxxx x 0 1", False],
            ["ooooooo/-------/-------/7/7/-------/xxxxxxx o 0 1", True],
            ["x5o/7/7/7/7/7/o5x x 0 100", False],
            ["7/7/7/7/4ooo/4ooo/4oox x 0 100", True],
        ]

        for fen, passing in tests:
            board = ataxx.Board(fen)
            moves = board.legal_moves()
            num_moves = len(moves)

            self.assertTrue(board.must_pass() == passing)

            if board.gameover():
                self.assertTrue(num_moves == 0)
            else:
                if passing:
                    self.assertTrue(num_moves == 1)
                    self.assertTrue(moves[0] == ataxx.Move.null())
                else:
                    self.assertTrue(num_moves > 0)
                    self.assertTrue(ataxx.Move.null() not in moves)
