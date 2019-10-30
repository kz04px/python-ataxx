import ataxx
import unittest

class TestMethods(unittest.TestCase):
    def test_set_get(self):
        nums = [0,1,2,3,4,5,6]
        squares = [[f,r] for f in nums for r in nums]
        board = ataxx.Board("empty")

        for x, y in squares:
            for piece in [ataxx.BLACK, ataxx.WHITE, ataxx.GAP, ataxx.EMPTY]:
                board.set(x, y, piece)
                self.assertTrue(piece == board.get(x, y))
