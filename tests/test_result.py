import ataxx
import unittest

class TestMethods(unittest.TestCase):
    def test_result(self):
        tests = [
            ["x5o/7/7/7/7/7/o5x x", "*"],
            ["x5o/7/7/7/7/7/o5x o", "*"],
            ["x5o/7/2-1-2/7/2-1-2/7/o5x x", "*"],
            ["x5o/7/2-1-2/7/2-1-2/7/o5x o", "*"],
            ["x6/7/7/7/7/7/7 x", "1-0"],
            ["x6/7/7/7/7/7/7 o", "1-0"],
            ["o6/7/7/7/7/7/7 x", "0-1"],
            ["o6/7/7/7/7/7/7 o", "0-1"],
            ["1xxxxxx/xxxxxxx/xxxxxxx/xxxxooo/ooooooo/ooooooo/ooooooo x", "*"],
            ["1xxxxxx/xxxxxxx/xxxxxxx/xxxxooo/ooooooo/ooooooo/ooooooo o", "*"],
            ["1oooooo/ooooooo/ooooooo/ooooxxx/xxxxxxx/xxxxxxx/xxxxxxx x", "*"],
            ["1oooooo/ooooooo/ooooooo/ooooxxx/xxxxxxx/xxxxxxx/xxxxxxx o", "*"],
            ["xxxxxxx/xxxxxxx/xxxxxxx/xxxxooo/ooooooo/ooooooo/ooooooo x", "1-0"],
            ["xxxxxxx/xxxxxxx/xxxxxxx/xxxxooo/ooooooo/ooooooo/ooooooo o", "1-0"],
            ["ooooooo/ooooooo/ooooooo/ooooxxx/xxxxxxx/xxxxxxx/xxxxxxx x", "0-1"],
            ["ooooooo/ooooooo/ooooooo/ooooxxx/xxxxxxx/xxxxxxx/xxxxxxx o", "0-1"],
            ["7/7/7/7/7/7/7 o", "1/2-1/2"],
            ["x5o/7/7/7/7/7/o5x x 99 0", "*"],
            ["x5o/7/7/7/7/7/o5x x 100 0", "1/2-1/2"],
            ["x5o/7/7/7/7/7/o5x x 0 400", "*"],
            ["x5o/7/7/7/7/7/o5x x 0 401", "1/2-1/2"],
        ]

        for fen, result in tests:
            board = ataxx.Board(fen)

            # Check the result is right
            self.assertTrue(board.result() == result)

            # Check that if we double pass (null move) we get a decisive result
            if result == "*":
                board.makemove(ataxx.Move.null())
                board.makemove(ataxx.Move.null())
                self.assertTrue(board.result() != "*")
