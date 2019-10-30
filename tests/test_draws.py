import ataxx
import unittest

class TestMethods(unittest.TestCase):
    def test_draws(self):
        # Check nullmove draw conditions
        board = ataxx.Board()
        board.makemove(ataxx.Move.null())
        board.makemove(ataxx.Move.null())
        self.assertTrue(board.gameover())
        self.assertFalse(board.fifty_move_draw())
        self.assertFalse(board.max_length_draw())

        # Check double move draw conditions
        board = ataxx.Board()
        for i in range(500):
            if i < 50:
                self.assertFalse(board.gameover())
                self.assertFalse(board.fifty_move_draw())
                self.assertFalse(board.max_length_draw())
            elif i < 400:
                self.assertTrue(board.gameover())
                self.assertTrue(board.fifty_move_draw())
                self.assertFalse(board.max_length_draw())
            else:
                self.assertTrue(board.gameover())
                self.assertTrue(board.fifty_move_draw())
                self.assertTrue(board.max_length_draw())

            if i % 2 == 0:
                board.makemove(ataxx.Move.from_san("g1g3"))
                board.makemove(ataxx.Move.from_san("a1a3"))
            else:
                board.makemove(ataxx.Move.from_san("g3g1"))
                board.makemove(ataxx.Move.from_san("a3a1"))
