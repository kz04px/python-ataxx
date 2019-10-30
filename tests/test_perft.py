import ataxx
import unittest

class TestMethods(unittest.TestCase):
    def test_perft(self):
        positions = [
            ["7/7/7/7/7/7/7 x 0 1", [1, 0, 0, 0, 0]],
            ["x5o/7/7/7/7/7/o5x x", [1, 16, 256, 6460]],
            ["x5o/7/2-1-2/7/2-1-2/7/o5x o", [1, 14, 196, 4184]],
            ["x5o/7/2-1-2/3-3/2-1-2/7/o5x x", [1, 14, 196, 4100]],
            ["x5o/7/3-3/2-1-2/3-3/7/o5x o", [1, 16, 256, 5948]],
            ["7/7/7/7/2-----/2-----/2--x1o x", [1, 1, 0, 0, 0]],
            ["7/7/7/7/2-----/2-----/2--x1o o", [1, 1, 0, 0, 0]],
        ]

        for fen, nodes in positions:
            board = ataxx.Board(fen)
            for idx, count in enumerate(nodes):
                self.assertTrue(board.perft(idx) == count)
