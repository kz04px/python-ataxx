import ataxx
import unittest

movestrings = [
    "0000",
    "a1", "b1", "c1", "d1", "e1", "f1", "g1",
    "a2", "b2", "c2", "d2", "e2", "f2", "g2",
    "a3", "b3", "c3", "d3", "e3", "f3", "g3",
    "a4", "b4", "c4", "d4", "e4", "f4", "g4",
    "a5", "b5", "c5", "d5", "e5", "f5", "g5",
    "a6", "b6", "c6", "d6", "e6", "f6", "g6",
    "a7", "b7", "c7", "d7", "e7", "f7", "g7",
    "a1c1", "a1c2", "a1a3", "a1b3", "a1c3",
    "b1d1", "b1d2", "b1a3", "b1b3", "b1c3", "b1d3",
    "c1a1", "c1e1", "c1a2", "c1e2", "c1a3", "c1b3", "c1c3", "c1d3", "c1e3",
    "d1b1", "d1f1", "d1b2", "d1f2", "d1b3", "d1c3", "d1d3", "d1e3", "d1f3",
    "e1c1", "e1g1", "e1c2", "e1g2", "e1c3", "e1d3", "e1e3", "e1f3", "e1g3",
    "f1d1", "f1d2", "f1d3", "f1e3", "f1f3", "f1g3",
    "g1e1", "g1e2", "g1e3", "g1f3", "g1g3",
    "a2c1", "a2c2", "a2c3", "a2a4", "a2b4", "a2c4",
    "b2d1", "b2d2", "b2d3", "b2a4", "b2b4", "b2c4", "b2d4",
    "c2a1", "c2e1", "c2a2", "c2e2", "c2a3", "c2e3", "c2a4", "c2b4", "c2c4", "c2d4", "c2e4",
    "d2b1", "d2f1", "d2b2", "d2f2", "d2b3", "d2f3", "d2b4", "d2c4", "d2d4", "d2e4", "d2f4",
    "e2c1", "e2g1", "e2c2", "e2g2", "e2c3", "e2g3", "e2c4", "e2d4", "e2e4", "e2f4", "e2g4",
    "f2d1", "f2d2", "f2d3", "f2d4", "f2e4", "f2f4", "f2g4",
    "g2e1", "g2e2", "g2e3", "g2e4", "g2f4", "g2g4",
    "a3a1", "a3b1", "a3c1", "a3c2", "a3c3", "a3c4", "a3a5", "a3b5", "a3c5",
    "b3a1", "b3b1", "b3c1", "b3d1", "b3d2", "b3d3", "b3d4", "b3a5", "b3b5", "b3c5", "b3d5",
    "c3a1", "c3b1", "c3c1", "c3d1", "c3e1", "c3a2", "c3e2", "c3a3", "c3e3", "c3a4", "c3e4", "c3a5", "c3b5", "c3c5", "c3d5", "c3e5",
    "d3b1", "d3c1", "d3d1", "d3e1", "d3f1", "d3b2", "d3f2", "d3b3", "d3f3", "d3b4", "d3f4", "d3b5", "d3c5", "d3d5", "d3e5", "d3f5",
    "e3c1", "e3d1", "e3e1", "e3f1", "e3g1", "e3c2", "e3g2", "e3c3", "e3g3", "e3c4", "e3g4", "e3c5", "e3d5", "e3e5", "e3f5", "e3g5",
    "f3d1", "f3e1", "f3f1", "f3g1", "f3d2", "f3d3", "f3d4", "f3d5", "f3e5", "f3f5", "f3g5",
    "g3e1", "g3f1", "g3g1", "g3e2", "g3e3", "g3e4", "g3e5", "g3f5", "g3g5",
    "a4a2", "a4b2", "a4c2", "a4c3", "a4c4", "a4c5", "a4a6", "a4b6", "a4c6",
    "b4a2", "b4b2", "b4c2", "b4d2", "b4d3", "b4d4", "b4d5", "b4a6", "b4b6", "b4c6", "b4d6",
    "c4a2", "c4b2", "c4c2", "c4d2", "c4e2", "c4a3", "c4e3", "c4a4", "c4e4", "c4a5", "c4e5", "c4a6", "c4b6", "c4c6", "c4d6", "c4e6",
    "d4b2", "d4c2", "d4d2", "d4e2", "d4f2", "d4b3", "d4f3", "d4b4", "d4f4", "d4b5", "d4f5", "d4b6", "d4c6", "d4d6", "d4e6", "d4f6",
    "e4c2", "e4d2", "e4e2", "e4f2", "e4g2", "e4c3", "e4g3", "e4c4", "e4g4", "e4c5", "e4g5", "e4c6", "e4d6", "e4e6", "e4f6", "e4g6",
    "f4d2", "f4e2", "f4f2", "f4g2", "f4d3", "f4d4", "f4d5", "f4d6", "f4e6", "f4f6", "f4g6",
    "g4e2", "g4f2", "g4g2", "g4e3", "g4e4", "g4e5", "g4e6", "g4f6", "g4g6",
    "a5a3", "a5b3", "a5c3", "a5c4", "a5c5", "a5c6", "a5a7", "a5b7", "a5c7",
    "b5a3", "b5b3", "b5c3", "b5d3", "b5d4", "b5d5", "b5d6", "b5a7", "b5b7", "b5c7", "b5d7",
    "c5a3", "c5b3", "c5c3", "c5d3", "c5e3", "c5a4", "c5e4", "c5a5", "c5e5", "c5a6", "c5e6", "c5a7", "c5b7", "c5c7", "c5d7", "c5e7",
    "d5b3", "d5c3", "d5d3", "d5e3", "d5f3", "d5b4", "d5f4", "d5b5", "d5f5", "d5b6", "d5f6", "d5b7", "d5c7", "d5d7", "d5e7", "d5f7",
    "e5c3", "e5d3", "e5e3", "e5f3", "e5g3", "e5c4", "e5g4", "e5c5", "e5g5", "e5c6", "e5g6", "e5c7", "e5d7", "e5e7", "e5f7", "e5g7",
    "f5d3", "f5e3", "f5f3", "f5g3", "f5d4", "f5d5", "f5d6", "f5d7", "f5e7", "f5f7", "f5g7",
    "g5e3", "g5f3", "g5g3", "g5e4", "g5e5", "g5e6", "g5e7", "g5f7", "g5g7",
    "a6a4", "a6b4", "a6c4", "a6c5", "a6c6", "a6c7",
    "b6a4", "b6b4", "b6c4", "b6d4", "b6d5", "b6d6", "b6d7",
    "c6a4", "c6b4", "c6c4", "c6d4", "c6e4", "c6a5", "c6e5", "c6a6", "c6e6", "c6a7", "c6e7",
    "d6b4", "d6c4", "d6d4", "d6e4", "d6f4", "d6b5", "d6f5", "d6b6", "d6f6", "d6b7", "d6f7",
    "e6c4", "e6d4", "e6e4", "e6f4", "e6g4", "e6c5", "e6g5", "e6c6", "e6g6", "e6c7", "e6g7",
    "f6d4", "f6e4", "f6f4", "f6g4", "f6d5", "f6d6", "f6d7",
    "g6e4", "g6f4", "g6g4", "g6e5", "g6e6", "g6e7",
    "a7a5", "a7b5", "a7c5", "a7c6", "a7c7",
    "b7a5", "b7b5", "b7c5", "b7d5", "b7d6", "b7d7",
    "c7a5", "c7b5", "c7c5", "c7d5", "c7e5", "c7a6", "c7e6", "c7a7", "c7e7",
    "d7b5", "d7c5", "d7d5", "d7e5", "d7f5", "d7b6", "d7f6", "d7b7", "d7f7",
    "e7c5", "e7d5", "e7e5", "e7f5", "e7g5", "e7c6", "e7g6", "e7c7", "e7g7",
    "f7d5", "f7e5", "f7f5", "f7g5", "f7d6", "f7d7",
    "g7e5", "g7f5", "g7g5", "g7e6", "g7e7",
]

class TestMethods(unittest.TestCase):
    def test_is_legal(self):
        fens = [
            "x5o/7/7/7/7/7/o5x x 0 1",
            "x5o/7/2-1-2/7/2-1-2/7/o5x o 0 1",
            "x5o/7/2-1-2/3-3/2-1-2/7/o5x x 0 1",
            "x5o/7/3-3/2-1-2/3-3/7/o5x o 0 1",
            "7/3o3/7/3x3/7/7/3oo2 x 0 1",
            "7/7/7/7/4ooo/4ooo/4oox x 0 1",
            "7/7/7/7/4ooo/4ooo/4oox o 0 1",
            "7/7/7/7/4xxx/4xxx/4xxo x 0 1",
            "7/7/7/7/4xxx/4xxx/4xxo o 0 1",
            "7/7/7/7/7/7/7 x 0 1",
            "7/7/7/7/7/7/7 o 0 1",
            "7/7/7/7/-------/-------/xxx1ooo x 0 1",
            "7/7/7/7/-------/-------/xxx1ooo o 0 1",
            "7/7/7/7/-------/-------/xxxxooo x 0 1",
            "7/7/7/7/-------/-------/xxxxooo o 0 1",
            "7/7/7/7/---1---/-------/xxxxooo x 0 1",
            "7/7/7/7/---1---/-------/xxxxooo o 0 1",
            "xxxxxxx/ooooooo/xxxxxxx/ooooooo/xxxxxxx/ooooooo/xxxxxxx x 0 1",
            "7/7/7/7/7/7/6x x 0 1",
            "7/7/7/7/7/7/6x o 0 1",
            "7/7/7/7/7/7/6o x 0 1",
            "7/7/7/7/7/7/6o o 0 1"
        ]

        all_moves = [ataxx.Move.from_san(n) for n in movestrings]

        for fen in fens:
            board = ataxx.Board(fen)
            generated_moves = [n for n in board.legal_moves()]
            found = 0

            for move in all_moves:
                if move in generated_moves:
                    self.assertTrue(board.is_legal(move))
                    found += 1
                else:
                    self.assertFalse(board.is_legal(move))

            self.assertTrue(found == len(generated_moves))
