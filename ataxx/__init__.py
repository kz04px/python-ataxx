__author__ = "kz04px"
__url__ = "https://github.com/kz04px/python-ataxx"
__version__ = "1.1.0"

BLACK, WHITE, GAP, EMPTY = 0, 1, 2, 3
SINGLES = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
DOUBLES = [(-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2), (-1, -2), (-1, 2), (0, -2), (0, 2), (1, -2), (1, 2), (2, -2), (2, -1), (2, 0), (2, 1), (2, 2)]

# Some standard positions
FEN_STARTPOS = "x5o/7/7/7/7/7/o5x x 0 1"
FEN_4CORNERS = "x5o/7/2-1-2/7/2-1-2/7/o5x x 0 1"
FEN_4SIDES   = "x5o/7/3-3/2-1-2/3-3/7/o5x x 0 1"
FEN_EMPTY    = "7/7/7/7/7/7/7 x 0 1"

class Move:
    def __init__(self, fr_x, fr_y, to_x, to_y):
        self.fr_x = fr_x
        self.fr_y = fr_y
        self.to_x = to_x
        self.to_y = to_y
        self.flipped = [False]*8

    @classmethod
    def from_san(cls, san):
        if san == "0000":
            return cls.null()
        elif len(san) == 2:
            if san[0] not in "abcdefgABCDEFG":
                raise Exception(F"ValueError {san}")
            elif san[1] not in "1234567":
                raise Exception(F"ValueError {san}")

            to_x = ord(san[0]) - ord('a') 
            to_y = ord(san[1]) - ord('1')
            return cls(to_x, to_y, to_x, to_y)
        elif len(san) == 4:
            if san[0] not in "abcdefgABCDEFG":
                raise Exception(F"ValueError {san}")
            elif san[1] not in "1234567":
                raise Exception(F"ValueError {san}")
            elif san[2] not in "abcdefgABCDEFG":
                raise Exception(F"ValueError {san}")
            elif san[3] not in "1234567":
                raise Exception(F"ValueError {san}")

            fr_x = ord(san[0]) - ord('a') 
            fr_y = ord(san[1]) - ord('1')
            to_x = ord(san[2]) - ord('a') 
            to_y = ord(san[3]) - ord('1')
            return cls(fr_x, fr_y, to_x, to_y)
        else:
            raise Exception(F"ValueError {san}")

    @classmethod
    def null(cls):
        return cls(-1, -1, -1, -1)

    def is_single(self):
        dX = abs(self.fr_x - self.to_x)
        dY = abs(self.fr_y - self.to_y)
        return dX <= 1 and dY <= 1

    def is_double(self):
        return not self.is_single()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            self_single = self.is_single()
            other_single = other.is_single()
            if self_single != other_single:
                return False
            elif self_single and other_single:
                return self.to_x == other.to_x and self.to_y == other.to_y
            else:
                return self.fr_x == other.fr_x and self.fr_y == other.fr_y and self.to_x == other.to_x and self.to_y == other.to_y
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        # Null move
        if self == Move.null():
            return "0000"

        if self.is_single():
            return F"{chr(ord('a')+self.to_x)}{self.to_y+1}"
        else:
            return F"{chr(ord('a')+self.fr_x)}{self.fr_y+1}{chr(ord('a')+self.to_x)}{self.to_y+1}"

class Board:
    def __init__(self, fen="startpos"):
        self._board = [[GAP for x in range(7+4)] for y in range(7+4)]
        self.set_fen(fen)

    def get(self, x, y):
        return self._board[x+2][y+2]

    def set(self, x, y, n):
        self._board[x+2][y+2] = n

    def fifty_move_draw(self):
        return self.halfmove_clock >= 100

    def score(self):
        num_black, num_white, _, _ = self.count()
        return num_black - num_white

    def count(self):
        num_black = 0
        num_white = 0
        num_gaps = 0
        num_empty = 0
        for y in range(7):
            for x in range(7):
                if self.get(x, y) == BLACK:
                    num_black += 1
                elif self.get(x, y) == WHITE:
                    num_white += 1
                elif self.get(x, y) == GAP:
                    num_gaps += 1
                elif self.get(x, y) == EMPTY:
                    num_empty += 1

        return num_black, num_white, num_gaps, num_empty

    def __str__(self):
        board = "  a b c d e f g\n"
        board += " ╔═╦═╦═╦═╦═╦═╦═╗\n"
        for y in range(6, -1, -1):
            board += chr(y+49) + '║'
            for x in range(0, 7):
                if self.get(x, y) == BLACK:
                    board += 'X'
                elif self.get(x, y) == WHITE:
                    board += 'O'
                elif self.get(x, y) == GAP:
                    board += '#'
                elif self.get(x, y) == EMPTY:
                    board += ' '
                else:
                    board += "?"
                board += '║'
            board += chr(y+49) + '\n'
            if y > 0:
                board += ' ╠═╬═╬═╬═╬═╬═╬═╣\n'
        board += " ╚═╩═╩═╩═╩═╩═╩═╝\n"
        board += "  a b c d e f g\n"
        if self.turn == BLACK:
            board += "Turn: X"
        elif self.turn == WHITE:
            board += "Turn: O"
        else:
            board += "Turn: ?"
        return board

    def get_fen(self):
        fen = ''
        for y in range(6, -1, -1):
            empty = 0
            for x in range(7):
                if self.get(x, y) != EMPTY and empty > 0:
                    fen += str(empty)
                    empty = 0

                if self.get(x, y) == BLACK:
                    fen += 'x'
                elif self.get(x, y) == WHITE:
                    fen += 'o'
                elif self.get(x, y) == GAP:
                    fen += '-'
                elif self.get(x, y) == EMPTY:
                    empty += 1
            if empty > 0:
                fen += str(empty)
            if y > 0:
                fen += '/'

        if self.turn == WHITE:
            fen += ' o'
        else:
            fen += ' x'

        fen += ' ' + str(self.halfmove_clock)

        fen += ' ' + str(self.fullmove_clock)

        return fen

    def set_fen(self, fen):
        if fen == "startpos":
            fen = FEN_STARTPOS
        elif fen == "empty":
            fen = FEN_EMPTY

        parts = fen.split(' ')

        if len(parts) < 1 or len(parts) > 4:
            return False
        if parts[0].count('/') != 6:
            return False
        if len(parts[0]) < len("7/7/7/7/7/7/7"):
            return False
        if len(parts[0]) > len("xxxxxxx/xxxxxxx/xxxxxxx/xxxxxxx/xxxxxxx/xxxxxxx/xxxxxxx"):
            return False

        # Clear board
        for x in range(7):
            for y in range(7):
                self.set(x, y, EMPTY)
        self.turn = BLACK
        self.halfmove_clock = 0
        self.fullmove_clock = 1
        self.history = []
        self.halfmove_stack = []

        # Add side to move
        if len(parts) < 2:
            parts.append("x")

        # Add halfmove counter
        if len(parts) < 3:
            parts.append("0")

        # Add fullmove counter
        if len(parts) < 4:
            parts.append("1")

        # Set board
        sq = 0
        for c in parts[0]:
            x, y = sq%7, 7 - sq//7 - 1

            if c in "1234567":
                sq = sq + int(c)
            elif c in "bBxX":
                self.set(x, y, BLACK)
                sq = sq + 1
            elif c in "wWoO":
                self.set(x, y, WHITE)
                sq = sq + 1
            elif c in ['-']:
                self.set(x, y, GAP)
                sq = sq + 1
            elif c in ['/']:
                pass
            else:
                return False

        # We need to have parsed the right number of squares
        if sq != 7 * 7:
            return False

        # Set turn
        if parts[1] in "bBxX":
            self.turn = BLACK
        elif parts[1] in "wWoO":
            self.turn = WHITE
        else:
            return False

        # Set halfmove clock
        if parts[2].isdigit():
            self.halfmove_clock = int(parts[2])
        else:
            return False

        # Set fullmove clock
        if parts[3].isdigit():
            self.fullmove_clock = int(parts[3])
        else:
            return False

        # Save fen
        self._start_fen = ' '.join(parts)

        return True

    def makemove(self, move):
        if self.turn == BLACK:
            opponent = WHITE
        else:
            opponent = BLACK

        self.halfmove_stack.append(self.halfmove_clock)

        if self.turn == WHITE:
            self.fullmove_clock += 1

        # Null move
        if move == Move.null():
            self.turn = opponent
            self.history.append(move)
            self.halfmove_clock += 1
            return

        self.set(move.to_x, move.to_y, self.turn)
        if move.is_double():
            self.set(move.fr_x, move.fr_y, EMPTY)

        for idx, (dx, dy) in enumerate(SINGLES):
            x, y = move.to_x + dx, move.to_y + dy
            if self.get(x, y) == opponent:
                move.flipped[idx] = True
                self.set(x, y, self.turn)
            else:
                move.flipped[idx] = False

        self.history.append(move)
        self.turn = opponent
        self.halfmove_clock += 1
        if move.is_single():
            self.halfmove_clock = 0

    def undo(self):
        if self.turn == BLACK:
            us = WHITE
        else:
            us = BLACK
        them = self.turn

        if self.turn == BLACK:
            self.fullmove_clock -= 1

        move = self.history.pop()
        self.halfmove_clock = self.halfmove_stack.pop()
        self.turn = us

        if move == Move.null():
            return

        # Remove the piece we placed
        self.set(move.to_x, move.to_y, EMPTY)

        # Restore the piece we removed
        if move.is_double():
            self.set(move.fr_x, move.fr_y, us)

        # Restore the pieces we captured
        for idx, val in enumerate(move.flipped):
            if val:
                dx, dy = SINGLES[idx]
                self.set(move.to_x + dx, move.to_y + dy, them)

    def main_line(self):
        return self.history
    
    def start_fen(self):
        return self._start_fen

    def legal_moves(self):
        if self.gameover():
            return []

        movelist = []
        for x in range(7):
            for y in range(7):
                # Singles
                if self.get(x, y) == EMPTY:
                    for dx, dy in SINGLES:
                        if self.get(x+dx, y+dy) == self.turn:
                            movelist.append(Move(x, y, x, y))
                            break
                # Doubles
                elif self.get(x, y) == self.turn:
                    for dx, dy in DOUBLES:
                        if self.get(x+dx, y+dy) == EMPTY:
                            movelist.append(Move(x, y, x+dx, y+dy))

        if movelist == []:
            return [Move.null()]
        else:
            return movelist

    def is_legal(self, move):
        return move in self.legal_moves()

    def perft(self, depth, full=False):
        movelist = self.legal_moves()

        if depth == 0:
            return 1

        if self.gameover():
            return 0

        if depth == 1:
            return len(movelist)

        nodes = 0

        for move in movelist:
            self.makemove(move)
            nodes += self.perft(depth-1)
            self.undo()

        return nodes

    def gameover(self):
        # 50 move rule
        if self.fifty_move_draw():
            return True

        # No pieces left, no gaps left
        num_black, num_white, num_gaps, num_empty = self.count()
        if num_empty == 0 or num_black == 0 or num_white == 0:
            return True

        # No moves left
        for x in range(7):
            for y in range(7):
                if self.get(x, y) in [BLACK, WHITE]:
                    # Singles
                    for dx, dy in SINGLES:
                        if self.get(x+dx, y+dy) == EMPTY:
                            return False
                    # Doubles
                    for dx, dy in DOUBLES:
                        if self.get(x+dx, y+dy) == EMPTY:
                            return False

        return True

    def result(self):
        if not self.gameover():
            return "*"

        if self.fifty_move_draw():
            return "1/2-1/2"

        num_black, num_white, num_gaps, num_empty = self.count()

        if num_black > num_white:
            return "1-0"
        elif num_black < num_white:
            return "0-1"
        else:
            return "1/2-1/2"
