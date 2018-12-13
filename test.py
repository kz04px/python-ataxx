import ataxx
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
            {"fen": "x5o/7/7/7/7/7/o5x x",           "nodes": 256},
            {"fen": "x5o/7/2-1-2/7/2-1-2/7/o5x o",   "nodes": 196},
            {"fen": "x5o/7/2-1-2/3-3/2-1-2/7/o5x x", "nodes": 196},
            {"fen": "x5o/7/3-3/2-1-2/3-3/7/o5x o",   "nodes": 256},
        ]

        for position in positions:
            fen = position["fen"]
            nodes = position["nodes"]
            board = ataxx.Board(fen)
            self.assertTrue(board.perft(2) == nodes)

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

if __name__ == '__main__':
    unittest.main()
