import ataxx
import unittest

class TestMethods(unittest.TestCase):
    def test_complete(self):
        fens = [
            "x5o/7/7/7/7/7/o5x x 0 1",
            "x5o/7/2-1-2/7/2-1-2/7/o5x o 0 1",
            "x5o/7/2-1-2/3-3/2-1-2/7/o5x x 0 1",
            "x5o/7/3-3/2-1-2/3-3/7/o5x o 0 1"
        ]

        for fen in fens:
            board = ataxx.Board()
            self.assertTrue(board.set_fen(fen) == True)
            self.assertTrue(board.get_fen() == fen)
            self.assertTrue(board.start_fen() == fen)

    def test_malformed(self):
        tests = [
            ["x5o/7/7/7/7/7/o5x x 0 1 " ,"x5o/7/7/7/7/7/o5x x 0 1"],
            ["x5o/7/7/7/7/7/o5x x 0 1   " ,"x5o/7/7/7/7/7/o5x x 0 1"],
            ["x5o/7/7/7/7/7/o5x x 0  1" ,"x5o/7/7/7/7/7/o5x x 0 1"],
            ["x5o/7/7/7/7/7/o5x x  0 1" ,"x5o/7/7/7/7/7/o5x x 0 1"],
            ["x5o/7/7/7/7/7/o5x  x 0 1" ,"x5o/7/7/7/7/7/o5x x 0 1"],
            [" x5o/7/7/7/7/7/o5x x 0 1" ,"x5o/7/7/7/7/7/o5x x 0 1"],
        ]

        for fen, corrected in tests:
            board = ataxx.Board()
            self.assertTrue(board.set_fen(fen) == True)
            self.assertTrue(board.get_fen() == corrected)

    def test_partial(self):
        tests = [
            ["x5o/7/7/7/7/7/o5x", "x5o/7/7/7/7/7/o5x x 0 1"],
            ["x5o/7/2-1-2/7/2-1-2/7/o5x o", "x5o/7/2-1-2/7/2-1-2/7/o5x o 0 1"],
            ["x5o/7/2-1-2/3-3/2-1-2/7/o5x x 0", "x5o/7/2-1-2/3-3/2-1-2/7/o5x x 0 1"],
            ["x5o/7/3-3/2-1-2/3-3/7/o5x o 0 1" ,"x5o/7/3-3/2-1-2/3-3/7/o5x o 0 1"]
        ]

        for fen, corrected in tests:
            board = ataxx.Board()
            self.assertTrue(board.set_fen(fen) == True)
            self.assertTrue(board.get_fen() == corrected)

    def test_invalid(self):
        fens = [
            "",
            "a",
            "a x 0 1",
            "x5o/7/7/7/7/7/o5g x 0 1",
            "x5o/7/7/7/7/7/o5 x 0 1",
            "x5o/7/7/7/7/7/o5xg x 0 1",
            "x5o/7/7/7/7/7/o5x a 0 1",
            "x5o/7/7/7/7/7/o5x x a 1",
            "x5o/7/7/7/7/7/o5x x 0 a",
            "x5o/7/7/7/7/7/o5x x 0 1 a",
            "x5o/7/7/7/7/7/o5x x -5 1",
            "x5o/7/7/7/7/7/o5x x 0 -5",
            "x5o/7/7/7/7/7/o5x x 0 1 a",
            "7/7/7/7/7/7/7/7 x 0 1",
        ]

        for fen in fens:
            board = ataxx.Board()
            self.assertTrue(board.set_fen(fen) == False)
