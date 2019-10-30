import ataxx
import unittest

class TestMethods(unittest.TestCase):
    def test_nullmove(self):
        self.assertTrue(ataxx.Move.null() == ataxx.Move(-1, -1, -1, -1))
        self.assertTrue(ataxx.Move.null() != ataxx.Move(0, 0, 0, 0))
        self.assertTrue(str(ataxx.Move.null()) == "0000")

        board1 = ataxx.Board()
        board2 = ataxx.Board()

        # Make the null move
        board2.makemove(ataxx.Move.null())

        pieces1, turn1, halfmoves1, _ = board1.get_fen().split(" ")
        pieces2, turn2, halfmoves2, _ = board2.get_fen().split(" ")

        # Check changes made
        self.assertTrue(pieces1 == pieces2)
        self.assertTrue(turn1 != turn2)
        self.assertTrue(int(halfmoves1)+1 == int(halfmoves2))
