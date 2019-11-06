import ataxx
import unittest
from ataxx.zobrist import calculate_hash

class TestMethods(unittest.TestCase):
    def test_known(self):
        tests = [
            ["x5o/7/7/7/7/7/o5x x 0 1", 0x94aea6ca1a7b7761],
            ["x5o/7/2-1-2/7/2-1-2/7/o5x x 0 1", 0x94aea6ca1a7b7761],
            ["1oo1o2/7/7/3xo2/1x5/7/7 x 0 1", 0xb97cab11e44bc9ef],
            ["7/7/7/7/-------/-------/x5o x 0 1", 0x4cb62ab58e84a8d7],
        ]

        for fen, hash in tests:
            board = ataxx.Board(fen)
            self.assertTrue(board.get_hash() == hash)

    def test_incremental(self):
        def hash_test(board, depth):
            self.assertTrue(board.get_hash() == calculate_hash(board))

            if depth == 0 or board.gameover():
                return

            for move in board.legal_moves():
                board.makemove(move)
                hash_test(board, depth-1)
                board.undo()

        fens = [
            "x5o/7/7/7/7/7/o5x x 0 1",
            "x5o/7/2-1-2/7/2-1-2/7/o5x x 0 1",
            "1oo1o2/7/7/3xo2/1x5/7/7 x 0 1",
            "7/7/7/7/-------/-------/x5o x 0 1",
        ]

        for fen in fens:
            board = ataxx.Board(fen)
            hash_test(board, 3)
