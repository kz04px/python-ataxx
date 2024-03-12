import ataxx
import unittest

class TestMethods(unittest.TestCase):
    def test_result(self):
        tests = [
            # No result
            ["x5o/7/7/7/7/7/o5x x 0 1", "*"],
            ["x5o/7/7/7/7/7/o5x o 0 1", "*"],
            ["x5o/7/2-1-2/7/2-1-2/7/o5x x 0 1", "*"],
            ["x5o/7/2-1-2/7/2-1-2/7/o5x o 0 1", "*"],
            ["7/7/7/7/7/-------/x-----o x 0 1", "*"],
            ["7/7/7/7/7/-------/x-----o o 0 1", "*"],
            # Win due to no opponent pieces
            ["x6/7/7/7/7/7/7 x 0 1", "1-0"],
            ["x6/7/7/7/7/7/7 o 0 1", "1-0"],
            ["o6/7/7/7/7/7/7 x 0 1", "0-1"],
            ["o6/7/7/7/7/7/7 o 0 1", "0-1"],
            # No result with board almost full
            ["1xxxxxx/xxxxxxx/xxxxxxx/xxxxooo/ooooooo/ooooooo/ooooooo x 0 1", "*"],
            ["1xxxxxx/xxxxxxx/xxxxxxx/xxxxooo/ooooooo/ooooooo/ooooooo o 0 1", "*"],
            ["1oooooo/ooooooo/ooooooo/ooooxxx/xxxxxxx/xxxxxxx/xxxxxxx x 0 1", "*"],
            ["1oooooo/ooooooo/ooooooo/ooooxxx/xxxxxxx/xxxxxxx/xxxxxxx o 0 1", "*"],
            # Board totally filled
            ["xxxxxxx/xxxxxxx/xxxxxxx/xxxxooo/ooooooo/ooooooo/ooooooo x 0 1", "1-0"],
            ["xxxxxxx/xxxxxxx/xxxxxxx/xxxxooo/ooooooo/ooooooo/ooooooo o 0 1", "1-0"],
            ["ooooooo/ooooooo/ooooooo/ooooxxx/xxxxxxx/xxxxxxx/xxxxxxx x 0 1", "0-1"],
            ["ooooooo/ooooooo/ooooooo/ooooxxx/xxxxxxx/xxxxxxx/xxxxxxx o 0 1", "0-1"],
            ["xxxxxxx/xxxxxxx/xxxxxxx/xxx-ooo/ooooooo/ooooooo/ooooooo x 0 1", "1/2-1/2"],
            ["xxxxxxx/xxxxxxx/xxxxxxx/xxx-ooo/ooooooo/ooooooo/ooooooo o 0 1", "1/2-1/2"],
            ["ooooooo/ooooooo/ooooooo/ooo-xxx/xxxxxxx/xxxxxxx/xxxxxxx x 0 1", "1/2-1/2"],
            ["ooooooo/ooooooo/ooooooo/ooo-xxx/xxxxxxx/xxxxxxx/xxxxxxx o 0 1", "1/2-1/2"],
            # No moves left without full board
            ["7/7/7/7/-------/-------/x-----o x 0 1", "1/2-1/2"],
            ["7/7/7/7/-------/-------/x-----o o 0 1", "1/2-1/2"],
            ["7/7/7/7/-------/-------/xx----o x 0 1", "1-0"],
            ["7/7/7/7/-------/-------/xx----o o 0 1", "1-0"],
            ["7/7/7/7/-------/-------/x----oo x 0 1", "0-1"],
            ["7/7/7/7/-------/-------/x----oo o 0 1", "0-1"],
            # Empty board
            ["7/7/7/7/7/7/7 o 0 1", "1/2-1/2"],
            # 50 move rule draw
            ["x5o/7/7/7/7/7/o5x x 99 0", "*"],
            ["x5o/7/7/7/7/7/o5x x 100 0", "1/2-1/2"],
            ["x5o/7/7/7/7/7/o5x x 400 0", "1/2-1/2"],
            ["xxxxxxo/7/7/7/7/7/o5x x 100 0", "1/2-1/2"],
            ["xxxxxxo/7/7/7/7/7/o5x o 100 0", "1/2-1/2"],
            ["xoooooo/7/7/7/7/7/o5x x 100 0", "1/2-1/2"],
            ["xoooooo/7/7/7/7/7/o5x o 100 0", "1/2-1/2"],
            # Win due to no opponent pieces has priority over the 50 move rule
            ["x6/7/7/7/7/7/7 x 100 0", "1-0"],
            ["x6/7/7/7/7/7/7 o 100 0", "1-0"],
            ["o6/7/7/7/7/7/7 x 100 0", "0-1"],
            ["o6/7/7/7/7/7/7 o 100 0", "0-1"],
            # Win with full board has priority over the 50 move rule
            ["xxxxxxx/xxxxxxx/xxxxxxx/xxxxooo/ooooooo/ooooooo/ooooooo x 100 1", "1-0"],
            ["xxxxxxx/xxxxxxx/xxxxxxx/xxxxooo/ooooooo/ooooooo/ooooooo o 100 1", "1-0"],
            ["ooooooo/ooooooo/ooooooo/ooooxxx/xxxxxxx/xxxxxxx/xxxxxxx x 100 1", "0-1"],
            ["ooooooo/ooooooo/ooooooo/ooooxxx/xxxxxxx/xxxxxxx/xxxxxxx o 100 1", "0-1"],
            # Win with no more moves has priority over the 50 move rule
            ["7/7/7/7/-------/-------/x-----o x 100 1", "1/2-1/2"],
            ["7/7/7/7/-------/-------/x-----o o 100 1", "1/2-1/2"],
            ["7/7/7/7/-------/-------/xx----o x 100 1", "1-0"],
            ["7/7/7/7/-------/-------/xx----o o 100 1", "1-0"],
            ["7/7/7/7/-------/-------/x----oo x 100 1", "0-1"],
            ["7/7/7/7/-------/-------/x----oo o 100 1", "0-1"],
            # Fullmove counter is irrelevant
            ["x5o/7/7/7/7/7/o5x x 0 400", "*"],
            ["x6/7/7/7/7/7/7 x 0 400", "1-0"],
            ["x6/7/7/7/7/7/7 o 0 400", "1-0"],
            ["o6/7/7/7/7/7/7 x 0 400", "0-1"],
            ["o6/7/7/7/7/7/7 o 0 400", "0-1"],
        ]

        for fen, result in tests:
            board = ataxx.Board(fen)
            self.assertTrue(board.result() == result)
