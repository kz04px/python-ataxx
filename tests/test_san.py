import ataxx
import unittest

class TestMethods(unittest.TestCase):
    def test_positions(self):
        fens = [
            "x5o/7/7/7/7/7/o5x x",
            "x5o/7/2-1-2/7/2-1-2/7/o5x o",
            "x5o/7/2-1-2/3-3/2-1-2/7/o5x x",
            "x5o/7/3-3/2-1-2/3-3/7/o5x o"
        ]

        for fen in fens:
            board = ataxx.Board(fen)
            for move in board.legal_moves():
                self.assertTrue(ataxx.Move.from_san(str(move)) == move)

    def test_valid(self):
        move_strings = [
            "a1c3",
            "c3a1",
            "c1a3",
            "a3c1",
            "d4f5",
            "d4f3",
            "d4b5",
            "d4b3",
            "a1",
            "a7",
            "g1",
            "g7",
            "0000",
        ]

        for movestr in move_strings:
            try:
                move = ataxx.Move.from_san(movestr)
            except:
                self.fail(F"Move.from_san() raised an exception parsing {movestr}")

    def test_invalid(self):
        move_strings = [
            "",
            "a8",
            "a0",
            "g1",
            "g7",
            "asd",
            "a2a4a",
            "a1a4",
            "A2",
            "A2C4",
            "a1a1",
            "a1a2",
            "a1b1",
            "a1b2",
            "11",
            "1133",
        ]

        for movestr in move_strings:
            self.assertRaises(Exception, lambda:ataxx.Move.from_san(), movestr)
