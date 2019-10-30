import ataxx
import unittest

class TestMethods(unittest.TestCase):
    def test_result(self):
        tests = [
            ["x5o/7/7/7/7/7/o5x x 0 1", "*"],
            ["x5o/7/7/7/7/7/o5x o 0 1", "*"],
            ["x5o/7/2-1-2/7/2-1-2/7/o5x x 0 1", "*"],
            ["x5o/7/2-1-2/7/2-1-2/7/o5x o 0 1", "*"],
            ["x6/7/7/7/7/7/7 x 0 1", "1-0"],
            ["x6/7/7/7/7/7/7 o 0 1", "1-0"],
            ["o6/7/7/7/7/7/7 x 0 1", "0-1"],
            ["o6/7/7/7/7/7/7 o 0 1", "0-1"],
            ["1xxxxxx/xxxxxxx/xxxxxxx/xxxxooo/ooooooo/ooooooo/ooooooo x 0 1", "*"],
            ["1xxxxxx/xxxxxxx/xxxxxxx/xxxxooo/ooooooo/ooooooo/ooooooo o 0 1", "*"],
            ["1oooooo/ooooooo/ooooooo/ooooxxx/xxxxxxx/xxxxxxx/xxxxxxx x 0 1", "*"],
            ["1oooooo/ooooooo/ooooooo/ooooxxx/xxxxxxx/xxxxxxx/xxxxxxx o 0 1", "*"],
            ["xxxxxxx/xxxxxxx/xxxxxxx/xxxxooo/ooooooo/ooooooo/ooooooo x 0 1", "1-0"],
            ["xxxxxxx/xxxxxxx/xxxxxxx/xxxxooo/ooooooo/ooooooo/ooooooo o 0 1", "1-0"],
            ["ooooooo/ooooooo/ooooooo/ooooxxx/xxxxxxx/xxxxxxx/xxxxxxx x 0 1", "0-1"],
            ["ooooooo/ooooooo/ooooooo/ooooxxx/xxxxxxx/xxxxxxx/xxxxxxx o 0 1", "0-1"],
            ["7/7/7/7/7/7/7 o 0 1", "1/2-1/2"],
            ["x5o/7/7/7/7/7/o5x x 99 0", "*"],
            ["x5o/7/7/7/7/7/o5x x 100 0", "1/2-1/2"],
            ["x5o/7/7/7/7/7/o5x x 0 400", "*"],
        ]

        for fen, result in tests:
            board = ataxx.Board(fen)
            self.assertTrue(board.result() == result)
