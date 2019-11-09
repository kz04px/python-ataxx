import ataxx
import unittest

class TestMethods(unittest.TestCase):
    def test_predict(self):
        def hash_test(board, depth):
            if depth == 0 or board.gameover():
                return

            for move in board.legal_moves():
                predicted = board.predict_hash(move)
                board.makemove(move)
                self.assertTrue(board.get_hash() == predicted)
                hash_test(board, depth-1)
                board.undo()

        fens = [
            "x5o/7/7/7/7/7/o5x x 0 1",
            "x5o/7/2-1-2/7/2-1-2/7/o5x x 0 1",
            "1oo1o2/7/7/3xo2/1x5/7/7 x 0 1",
            "7/7/7/7/-------/-------/x5o x 0 1",
            "7/7/7/7/4ooo/4ooo/4oox x 0 1",
        ]

        for fen in fens:
            board = ataxx.Board(fen)
            hash_test(board, 3)
