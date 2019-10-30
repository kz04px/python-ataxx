import ataxx
import unittest

class TestMethods(unittest.TestCase):
    def test_score(self):
        tests = [
            ["x5o/7/7/7/7/7/o5x x 0 1", 0],
            ["x5o/7/2-1-2/7/2-1-2/7/o5x x 0 1", 0],
            ["x5o/7/3-3/2-1-2/3-3/7/o5x x 0 1", 0],
            ["7/7/7/7/7/7/7 x 0 1", 0],
            ["x6/7/7/7/7/7/7 x 0 1", 1],
            ["o6/7/7/7/7/7/7 x 0 1", -1],
            ["xxo4/7/7/7/7/7/7 x 0 1", 1],
            ["oox4/7/7/7/7/7/7 x 0 1", -1],
            ["xxxxxxx/xxxxxxx/xxxxxxx/xxxxxxx/xxxxxxx/xxxxxxx/xxxxxxx x 0 1", 49],
            ["ooooooo/ooooooo/ooooooo/ooooooo/ooooooo/ooooooo/ooooooo x 0 1", -49],
        ]

        for fen, score in tests:
            board = ataxx.Board(fen)
            self.assertTrue(board.score() == score)
