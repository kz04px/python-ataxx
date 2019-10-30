import ataxx
import unittest

class TestMethods(unittest.TestCase):
    def test_is_legal(self):
        fens = [
            "x5o/7/7/7/7/7/o5x x 0 1",
            "x5o/7/2-1-2/7/2-1-2/7/o5x o 0 1",
            "x5o/7/2-1-2/3-3/2-1-2/7/o5x x 0 1",
            "x5o/7/3-3/2-1-2/3-3/7/o5x o 0 1",
            "7/3o3/7/3x3/7/7/3oo2 x 0 1",
            "7/7/7/7/4ooo/4ooo/4oox x 0 1",
            "7/7/7/7/4ooo/4ooo/4oox o 0 1",
            "7/7/7/7/4xxx/4xxx/4xxo x 0 1",
            "7/7/7/7/4xxx/4xxx/4xxo o 0 1",
            "7/7/7/7/7/7/7 x 0 1",
            "7/7/7/7/7/7/7 o 0 1",
            "7/7/7/7/-------/-------/xxx1ooo x 0 1",
            "7/7/7/7/-------/-------/xxx1ooo o 0 1",
            "7/7/7/7/-------/-------/xxxxooo x 0 1",
            "7/7/7/7/-------/-------/xxxxooo o 0 1",
            "7/7/7/7/---1---/-------/xxxxooo x 0 1",
            "7/7/7/7/---1---/-------/xxxxooo o 0 1"
        ]

        for fen in fens:
            board = ataxx.Board(fen)
            for move in board.legal_moves():
                self.assertTrue(board.is_legal(move))
