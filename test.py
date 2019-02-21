import ataxx
import ataxx.players
import ataxx.pgn
import random
import string
import copy
import unittest

class TestMethods(unittest.TestCase):
    def test_fen(self):
        fens = [
            "x5o/7/7/7/7/7/o5x x 0 1",
            "x5o/7/2-1-2/7/2-1-2/7/o5x o 0 1",
            "x5o/7/2-1-2/3-3/2-1-2/7/o5x x 0 1",
            "x5o/7/3-3/2-1-2/3-3/7/o5x o 0 1"
        ]

        for fen in fens:
            board = ataxx.Board(fen)
            self.assertTrue(board.get_fen() == fen)

        fens = [
            "",
            "a x 0 1",
            "x5o/7/7/7/7/7/o5x a 0 1",
            "x5o/7/7/7/7/7/o5x x a 1",
            "x5o/7/7/7/7/7/o5x x 0 a",
            "x5o/7/7/7/7/7/o5x x 0 1 a",
            "x5o/7/7/7/7/7/o5x x -5 1",
            "x5o/7/7/7/7/7/o5x x 0 -5"
        ]

        for fen in fens:
            board = ataxx.Board()
            self.assertTrue(board.set_fen(fen) != True)

    def test_perft(self):
        positions = [
            {"fen": "7/7/7/7/7/7/7 x",                "nodes": [1, 0, 0, 0, 0]},
            {"fen": "x5o/7/7/7/7/7/o5x x",            "nodes": [1, 16, 256, 6460, 155888]},
            {"fen": "x5o/7/2-1-2/7/2-1-2/7/o5x o",    "nodes": [1, 14, 196, 4184, 86528]},
            {"fen": "x5o/7/2-1-2/3-3/2-1-2/7/o5x x",  "nodes": [1, 14, 196, 4100, 83104]},
            {"fen": "x5o/7/3-3/2-1-2/3-3/7/o5x o",    "nodes": [1, 16, 256, 5948, 133264]},
            {"fen": "7/7/7/7/2-----/2-----/2--x1o x", "nodes": [1, 1, 0, 0, 0]},
            {"fen": "7/7/7/7/2-----/2-----/2--x1o o", "nodes": [1, 1, 0, 0, 0]},
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

    def test_from_san(self):
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

    def test_null_move(self):
        nullmove = ataxx.Move.null()

        self.assertTrue(nullmove == ataxx.Move(-1, -1, -1, -1))
        self.assertTrue(nullmove == ataxx.Move.null())
        self.assertTrue(nullmove != ataxx.Move(0, 0, 0, 0))
        self.assertTrue(str(nullmove) == "0000")

        board1 = ataxx.Board()
        board2 = ataxx.Board()

        # Make the null move
        board2.makemove(nullmove)

        pieces1, turn1, halfmoves1, _ = board1.get_fen().split(" ")
        pieces2, turn2, halfmoves2, _ = board2.get_fen().split(" ")

        # Check changes made
        self.assertTrue(pieces1 == pieces2)
        self.assertTrue(turn1 != turn2)
        self.assertTrue(int(halfmoves1)+1 == int(halfmoves2))

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
            {"fen": "7/7/7/7/7/7/7 x",               "moves": ["0000"]}
        ]

        for position in positions:
            fen = position["fen"]
            moves = position["moves"]

            # Greedy player
            board = ataxx.Board(fen)
            for _ in range(100):
                move = ataxx.players.greedy(board)
                self.assertTrue(str(move) in moves)

    def test_make_undo(self):
        fens = [
            "x5o/7/7/7/7/7/o5x x 0 1",
            "x5o/7/2-1-2/7/2-1-2/7/o5x o 0 1",
            "x5o/7/2-1-2/3-3/2-1-2/7/o5x x 0 1",
            "x5o/7/3-3/2-1-2/3-3/7/o5x o 0 1",
            "7/3o3/7/3x3/7/7/3oo2 x 0 1"
        ]

        for fen in fens:
            board = ataxx.Board(fen)

            while not board.gameover() and board.halfmove_clock < 500:
                current_fen = board.get_fen()

                # Test all legal moves
                for move in board.legal_moves():
                    board.makemove(move)
                    board.undo()
                    self.assertTrue(board.get_fen() == current_fen)

                # Test null move
                board.makemove(ataxx.Move.null())
                board.undo()
                self.assertTrue(board.get_fen() == current_fen)

                # Pick a random move and keep going
                move = random.choice(board.legal_moves())
                board.makemove(move)

            # Undo every move in the game
            while board.main_line():
                board.undo()

            # Make sure we're back where we started
            self.assertTrue(board.get_fen() == fen)

    def test_pgn(self):
        def random_phrase(n):
            return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.punctuation + string.digits + " ", k=n))

        pgns = [
            "[Event \"Example 1\"]\n[Black \"Player 1\"]\n[White \"Player 2\"]\n[UTCDate \"1970.01.01\"]\n[UTCTime \"00:00:00\"]\n[FEN \"x5o/7/7/7/7/7/o5x x\"]\n[Result \"*\"]\n\n1. a7c5 a2 2. g2 *",
            "[Event \"Example 2\"]\n[Black \"Player 1\"]\n[White \"Player 2\"]\n[UTCDate \"1970.01.01\"]\n[UTCTime \"00:00:00\"]\n[FEN \"x5o/7/7/7/7/7/o5x x\"]\n[Result \"*\"]\n\n1. a7c5 { Test 123 } 1... a2 { Test } 2. g2 *",
            "[Event \"Example 3\"]\n[Black \"Player 1\"]\n[White \"Player 2\"]\n[UTCDate \"1970.01.01\"]\n[UTCTime \"00:00:00\"]\n[FEN \"x5o/7/7/7/7/7/o5x x\"]\n[Result \"*\"]\n\n1. a7c7 (1. a7c5 { Test }) 1... g7f5 (1... a2 { Test } 2. g2 (2. f2 { Test })) 2. g1f3 a1b3 { Test 123 } *",
            "[Event \"Example 4\"]\n[Black \"Player 1\"]\n[White \"Player 2\"]\n[UTCDate \"1970.01.01\"]\n[UTCTime \"00:00:00\"]\n[FEN \"x5o/7/7/7/7/7/o5x x\"]\n[Result \"*\"]\n\n1. a7c7 { Test } (1. a7c5 { Test }) 1... g7f5 (1... a2 { Test } 2. g2 (2. f2 { Test } 2... a1c2)) 2. g1f3 a1b3 { Test 123 } *"
        ]

        # Test some known pgn strings
        for pgn in pgns:
            self.assertTrue(str(ataxx.pgn.parse(pgn)) == pgn)

        # Try parse some random games
        # These won't have variations or comments in them
        for _ in range(10):
            board = ataxx.Board()
            while not board.gameover() and board.halfmove_clock < 500:
                move = ataxx.players.random_move(board)
                board.makemove(move)

            pgn = ataxx.pgn.Game()
            pgn.headers["Event"]  = random_phrase(12)
            pgn.headers["Black"]  = random_phrase(12)
            pgn.headers["White"]  = random_phrase(12)
            pgn.headers["FEN"]    = ataxx.FEN_STARTPOS
            pgn.headers["Result"] = board.result()
            pgn.from_board(board)

            # Human readable pgn string
            pgn_string = str(pgn)

            # Test: pgn string ---> pgn ---> pgn string
            self.assertTrue(str(ataxx.pgn.parse(pgn_string)) == pgn_string)

            # Check the pgn main line matches the board
            moves = [n.move for n in pgn.main_line()]
            self.assertTrue(moves == board.main_line())

        # Create a pgn ourselves
        game = ataxx.pgn.Game()
        game.headers["FEN"] = ataxx.FEN_STARTPOS
        game.headers["Result"] = "*"
        node = game.add_variation(ataxx.Move.from_san("g2"), comment="First move")
        node = node.add_variation(ataxx.Move.from_san("a1a3"), comment="Second move")
        self.assertTrue(str(game) == "[Event \"Example\"]\n[FEN \"x5o/7/7/7/7/7/o5x x 0 1\"]\n[Result \"*\"]\n\n1. g2 { First move } a1a3 { Second move } *")

    def test_result(self):
        positions = [
            {"fen": "x5o/7/7/7/7/7/o5x x", "result": "*"},
            {"fen": "x5o/7/7/7/7/7/o5x o", "result": "*"},
            {"fen": "x5o/7/2-1-2/7/2-1-2/7/o5x x", "result": "*"},
            {"fen": "x5o/7/2-1-2/7/2-1-2/7/o5x o", "result": "*"},
            {"fen": "x6/7/7/7/7/7/7 x", "result": "1-0"},
            {"fen": "x6/7/7/7/7/7/7 o", "result": "1-0"},
            {"fen": "o6/7/7/7/7/7/7 x", "result": "0-1"},
            {"fen": "o6/7/7/7/7/7/7 o", "result": "0-1"},
            {"fen": "1xxxxxx/xxxxxxx/xxxxxxx/xxxxooo/ooooooo/ooooooo/ooooooo x", "result": "*"},
            {"fen": "1xxxxxx/xxxxxxx/xxxxxxx/xxxxooo/ooooooo/ooooooo/ooooooo o", "result": "*"},
            {"fen": "1oooooo/ooooooo/ooooooo/ooooxxx/xxxxxxx/xxxxxxx/xxxxxxx x", "result": "*"},
            {"fen": "1oooooo/ooooooo/ooooooo/ooooxxx/xxxxxxx/xxxxxxx/xxxxxxx o", "result": "*"},
            {"fen": "xxxxxxx/xxxxxxx/xxxxxxx/xxxxooo/ooooooo/ooooooo/ooooooo x", "result": "1-0"},
            {"fen": "xxxxxxx/xxxxxxx/xxxxxxx/xxxxooo/ooooooo/ooooooo/ooooooo o", "result": "1-0"},
            {"fen": "ooooooo/ooooooo/ooooooo/ooooxxx/xxxxxxx/xxxxxxx/xxxxxxx x", "result": "0-1"},
            {"fen": "ooooooo/ooooooo/ooooooo/ooooxxx/xxxxxxx/xxxxxxx/xxxxxxx o", "result": "0-1"},
        ]

        for position in positions:
            fen = position["fen"]
            result = position["result"]
            board = ataxx.Board(fen)

            # Check the result is right
            self.assertTrue(board.result() == result)

            # Check that if we double pass (null move) we get a decisive result
            if result == "*":
                board.makemove(ataxx.Move.null())
                board.makemove(ataxx.Move.null())
                self.assertTrue(board.result() != "*")

    def test_result(self):
        positions = [
            {"move": "g1f3", "fen": "x5o/7/7/7/5x1/7/o6 o 1 1"},
            {"move": "a1c1", "fen": "x5o/7/7/7/5x1/7/2o4 x 2 2"},
            {"move": "b6",   "fen": "x5o/1x5/7/7/5x1/7/2o4 o 0 2"},
            {"move": "c1e3", "fen": "x5o/1x5/7/7/4oo1/7/7 x 0 3"},
            {"move": "0000", "fen": "x5o/1x5/7/7/4oo1/7/7 o 1 3"},
        ]

        board = ataxx.Board();

        for position in positions:
            move = position["move"]
            fen = position["fen"]

            board.makemove(ataxx.Move.from_san(move))

            self.assertTrue(board.get_fen() == fen)

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

if __name__ == '__main__':
    unittest.main()
