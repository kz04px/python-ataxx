import ataxx
import ataxx.players
import unittest

class TestMethods(unittest.TestCase):
    def test_greedy(self):
        tests = [
            ["x5o/7/7/7/7/7/o5x x 0 1", ["f1", "f2", "g2", "a6", "b6", "b7"]],
            ["x5o/7/2-1-2/7/2-1-2/7/o5x o 0 1", ["a2", "b1", "b2", "g6", "f6", "f7"]],
            ["x5o/7/2-1-2/3-3/2-1-2/7/o5x x 0 1", ["f1", "f2", "g2", "a6", "b6", "b7"]],
            ["x5o/7/3-3/2-1-2/3-3/7/o5x o 0 1", ["a2", "b1", "b2", "g6", "f6", "f7"]],
            ["7/3o3/7/3x3/7/7/7 x 0 1", ["c5", "d5", "e5"]],
            ["3o3/7/7/3x3/7/7/7 x 0 1", ["d4c6", "d4d6", "d4e6"]],
            ["3o3/7/3x3/3x3/7/7/7 x 0 1", ["c6", "d6", "e6"]],
            ["o4oo/7/x5x/7/7/7/7 x 0 1", ["f6", "g6"]],
            ["7/3o3/7/3x3/7/7/3oo2 x 0 1", ["d4d2", "d4e2"]],
            ["7/7/7/7/7/7/7 x 0 1", ["0000"]]
        ]

        for fen, moves in tests:
            board = ataxx.Board(fen)

            # Greedy player
            for _ in range(100):
                move = ataxx.players.greedy(board)
                if board.gameover():
                    self.assertTrue(move == ataxx.Move.null())
                else:
                    self.assertTrue(move in board.legal_moves())
                    self.assertTrue(str(move) in moves)

    def test_random(self):
        fens = [
            "x5o/7/7/7/7/7/o5x x 0 1",
            "x5o/7/2-1-2/7/2-1-2/7/o5x o 0 1",
            "x5o/7/2-1-2/3-3/2-1-2/7/o5x x 0 1",
            "x5o/7/3-3/2-1-2/3-3/7/o5x o 0 1",
            "7/3o3/7/3x3/7/7/7 x 0 1",
            "3o3/7/7/3x3/7/7/7 x 0 1",
            "3o3/7/3x3/3x3/7/7/7 x 0 1",
            "o4oo/7/x5x/7/7/7/7 x 0 1",
            "7/3o3/7/3x3/7/7/3oo2 x 0 1",
            "7/7/7/7/7/7/7 x 0 1"
        ]

        for fen in fens:
            board = ataxx.Board(fen)

            # Random player
            for _ in range(100):
                move = ataxx.players.random_move(board)
                if board.gameover():
                    self.assertTrue(move == ataxx.Move.null())
                else:
                    self.assertTrue(move in board.legal_moves())
