import ataxx
import unittest

class TestMethods(unittest.TestCase):
    def test_counters(self):
        tests = [
            ["g2", 0, 1],
            ["a2", 0, 2],
            ["g3", 0, 2],
            ["a2a4", 1, 3],
            ["a7a5", 2, 3],
            ["a1b3", 3, 4],
            ["b4", 0, 4],
            ["f6", 0, 5],
        ]

        board = ataxx.Board("x5o/7/7/7/7/7/o5x x 0 1")

        for movestr, half, full in tests:
            move = ataxx.Move.from_san(movestr)
            board.makemove(move)
            self.assertTrue(board.halfmove_clock == half)
            self.assertTrue(board.fullmove_clock == full)

        board = ataxx.Board("x5o/7/7/7/7/7/o5x x 0 1")
        board.makemove(ataxx.Move.null())
        self.assertTrue(board.halfmove_clock == 1)
