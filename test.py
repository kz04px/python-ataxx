import ataxx
import ataxx.players
import random
import unittest

class TestStringMethods(unittest.TestCase):
    def test_fen(self):
        fens = [
            "x5o/7/7/7/7/7/o5x x",
            "x5o/7/2-1-2/7/2-1-2/7/o5x o",
            "x5o/7/2-1-2/3-3/2-1-2/7/o5x x",
            "x5o/7/3-3/2-1-2/3-3/7/o5x o"
        ]

        for fen in fens:
            board = ataxx.Board(fen)
            self.assertTrue(board.get_fen() == fen)

    def test_perft(self):
        positions = [
            {"fen": ataxx.FEN_EMPTY,                 "nodes": [1, 0, 0, 0, 0]},
            {"fen": "x5o/7/7/7/7/7/o5x x",           "nodes": [1, 16, 256, 6460, 155888]},
            {"fen": "x5o/7/2-1-2/7/2-1-2/7/o5x o",   "nodes": [1, 14, 196, 4184, 86528]},
            {"fen": "x5o/7/2-1-2/3-3/2-1-2/7/o5x x", "nodes": [1, 14, 196, 4100, 83104]},
            {"fen": "x5o/7/3-3/2-1-2/3-3/7/o5x o",   "nodes": [1, 16, 256, 5948, 133264]},
        ]

        depth = 4
        for position in positions:
            fen = position["fen"]
            board = ataxx.Board(fen)
            for idx, nodes in enumerate(position["nodes"]):
                if idx > depth:
                    break
                self.assertTrue(board.perft(idx) == nodes)

    def test_single_double(self):
        fens = [
            "x5o/7/7/7/7/7/o5x x",
            "x5o/7/2-1-2/7/2-1-2/7/o5x o",
            "x5o/7/2-1-2/3-3/2-1-2/7/o5x x",
            "x5o/7/3-3/2-1-2/3-3/7/o5x o"
        ]

        for fen in fens:
            board = ataxx.Board(fen)
            for move in board.legal_moves():
                self.assertTrue(move.is_single() != move.is_double())

    def test_parse_san(self):
        fens = [
            "x5o/7/7/7/7/7/o5x x",
            "x5o/7/2-1-2/7/2-1-2/7/o5x o",
            "x5o/7/2-1-2/3-3/2-1-2/7/o5x x",
            "x5o/7/3-3/2-1-2/3-3/7/o5x o"
        ]

        for fen in fens:
            board = ataxx.Board(fen)
            for move in board.legal_moves():
                self.assertTrue(board.parse_san(str(move)) == move)

    def test_single_equality(self):
        nums = [0,1,2,3,4,5,6]
        squares = [[f,r] for f in nums for r in nums]

        for sq_to in squares:
            a, b, c, d = sq_to + sq_to
            move1 = ataxx.Move(a, b, c, d)

            for sq_from in squares:
                a, b, c, d = sq_from + sq_to
                move2 = ataxx.Move(a, b, c, d)

                if move2.is_single():
                    self.assertTrue(move1 == move2)
                elif move2.is_double():
                    self.assertTrue(move1 != move2)

    def test_set_get(self):
        nums = [0,1,2,3,4,5,6]
        squares = [[f,r] for f in nums for r in nums]
        board = ataxx.Board("empty")

        for x, y in squares:
            for piece in [ataxx.BLACK, ataxx.WHITE, ataxx.GAP, ataxx.EMPTY]:
                board.set(x, y, piece)
                self.assertTrue(piece == board.get(x, y))

    def test_main_line(self):
        for _ in range(10):
            history = []

            # Play random moves on the board
            board1 = ataxx.Board("startpos")
            while not board1.gameover() and len(history) < 50:
                moves = board1.legal_moves()
                move = random.choice(moves)
                board1.makemove(move)
                history.append(move)

            # Replay the moves on a new board
            board2 = ataxx.Board("startpos")
            for move in board1.main_line():
                board2.makemove(move)

            self.assertTrue(board1.main_line() == history)
            self.assertTrue(board1.get_fen() == board2.get_fen())

    def test_players(self):
        positions = [
            {"fen": "x5o/7/7/7/7/7/o5x x",           "moves": ["f1", "f2", "g2", "a6", "b6", "b7"]},
            {"fen": "x5o/7/2-1-2/7/2-1-2/7/o5x o",   "moves": ["a2", "b1", "b2", "g6", "f6", "f7"]},
            {"fen": "x5o/7/2-1-2/3-3/2-1-2/7/o5x x", "moves": ["f1", "f2", "g2", "a6", "b6", "b7"]},
            {"fen": "x5o/7/3-3/2-1-2/3-3/7/o5x o",   "moves": ["a2", "b1", "b2", "g6", "f6", "f7"]},
            {"fen": "7/3o3/7/3x3/7/7/7 x",           "moves": ["c5", "d5", "e5"]},
            {"fen": "3o3/7/7/3x3/7/7/7 x",           "moves": ["d4c6", "d4d6", "d4e6"]},
            {"fen": "3o3/7/3x3/3x3/7/7/7 x",         "moves": ["c6", "d6", "e6"]},
            {"fen": "o4oo/7/x5x/7/7/7/7 x",          "moves": ["f6", "g6"]},
            {"fen": "7/3o3/7/3x3/7/7/3oo2 x",        "moves": ["d4d2", "d4e2"]},
            {"fen": "7/7/7/7/7/7/7 x",               "moves": ["None"]}
        ]

        for position in positions:
            fen = position["fen"]
            moves = position["moves"]

            # Greedy player
            board = ataxx.Board(fen)
            for _ in range(100):
                move = ataxx.players.greedy(board)
                self.assertTrue(str(move) in position["moves"])

    def test_make_undo(self):
        fens = [
            "x5o/7/7/7/7/7/o5x x",
            "x5o/7/2-1-2/7/2-1-2/7/o5x o",
            "x5o/7/2-1-2/3-3/2-1-2/7/o5x x",
            "x5o/7/3-3/2-1-2/3-3/7/o5x o",
            "7/3o3/7/3x3/7/7/3oo2 x"
        ]

        for fen in fens:
            board = ataxx.Board(fen)
            for move in board.legal_moves():
                board.makemove(move)
                board.undo()
                self.assertTrue(board.get_fen() == fen)

if __name__ == '__main__':
    unittest.main()
