BLACK, WHITE, GAP, EMPTY = 0, 1, 2, 3
SINGLES = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
DOUBLES = [(-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2), (-1, -2), (-1, 2), (0, -2), (0, 2), (1, -2), (1, 2), (2, -2), (2, -1), (2, 0), (2, 1), (2, 2)]
# Some standard positions
FEN_STARTPOS = "x5o/7/7/7/7/7/o5x x"
FEN_4CORNERS = "x5o/7/2-1-2/7/2-1-2/7/o5x x"
FEN_4SIDES   = "x5o/7/3-3/2-1-2/3-3/7/o5x x"
FEN_EMPTY    = "7/7/7/7/7/7/7 x"

class Move:
    def __init__(self, fr_x, fr_y, to_x, to_y):
        self.fr_x = fr_x
        self.fr_y = fr_y
        self.to_x = to_x
        self.to_y = to_y
        self.flipped = [False]*8

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
        if self.is_single():
            return F"{chr(ord('a')+self.to_x)}{self.to_y+1}"
        else:
            return F"{chr(ord('a')+self.fr_x)}{self.fr_y+1}{chr(ord('a')+self.to_x)}{self.to_y+1}"

class Board:
    def __init__(self, fen="startpos"):
        self.w = 7
        self.h = 7
        self.board = [[GAP for x in range(self.w+4)] for y in range(self.h+4)]
        self.turn = BLACK
        self.halfmove_clock = 0

        for y in range(self.w):
            for x in range(self.h):
                self.set(x, y, EMPTY)

        self.set_fen(fen)

    def get(self, x, y):
        return self.board[x+2][y+2]

    def set(self, x, y, n):
        self.board[x+2][y+2] = n

    def fifty_move_draw(self):
        return False

    def max_length_draw(self):
        return self.halfmove_clock >= 400

    def score(self):
        num_black, num_white, num_gaps, num_empty = self.count()

        black_moves = self.legal_moves(BLACK)
        white_moves = self.legal_moves(WHITE)

        if len(black_moves) == 0 and len(white_moves) == 0:
            pass
        elif len(black_moves) == 0:
            num_white += num_empty;
        elif len(white_moves) == 0:
            num_black += num_empty;

        return num_black - num_white

    def count(self):
        num_black = 0
        num_white = 0
        num_gaps = 0
        num_empty = 0
        for y in range(self.h):
            for x in range(self.w):
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
        for y in range(self.h-1, -1, -1):
            board += chr(y+49) + '║'
            for x in range(0, self.w):
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
        for y in range(self.h - 1, -1, -1):
            empty = 0
            for x in range(self.w):
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

        return fen

    def set_fen(self, fen):
        if fen == "startpos":
            fen = FEN_STARTPOS
        elif fen == "empty":
            fen = FEN_EMPTY

        parts = fen.split(' ')

        if len(parts) != 2:
            return -1
        if parts[0].count('/') != 6:
            return -2
        if len(parts[0]) < 16 or len(parts[0]) > 55:
            return -3
        if len(parts[1]) != 1:
            return -4

        for x in range(self.w):
            for y in range(self.h):
                self.set(x, y, EMPTY)

        sq = 0
        for c in parts[0]:
            x, y = sq%self.w, self.h - sq//self.h - 1

            if c in "1234567":
                sq = sq + int(c)
            elif c in ['x', 'X']:
                self.set(x, y, BLACK)
                sq = sq + 1
            elif c in ['o', 'O']:
                self.set(x, y, WHITE)
                sq = sq + 1
            elif c in ['-']:
                self.set(x, y, GAP)
                sq = sq + 1
            elif c in ['/']:
                pass
            else:
                return -5

        if parts[1] in "bBxX":
            self.turn = BLACK
        elif parts[1] in "wWoO":
            self.turn = WHITE
        else:
            return -6

        self.history = []
        self.halfmove_clock = 0

        return True

    def makemove(self, move):
        if self.turn == BLACK:
            opponent = WHITE
        else:
            opponent = BLACK

        self.set(move.to_x, move.to_y, self.turn)
        if move.is_double():
            self.set(move.fr_x, move.fr_y, EMPTY)

        for idx, val in enumerate(SINGLES):
            x, y = move.to_x + val[0], move.to_y + val[1]
            if self.get(x, y) == opponent:
                move.flipped[idx] = True
                self.set(x, y, self.turn)
            else:
                move.flipped[idx] = False

        self.history.append(move)
        self.halfmove_clock += 1
        self.turn = opponent

    def undo(self):
        if self.turn == BLACK:
            us = WHITE
        else:
            us = BLACK
        them = self.turn

        move = self.history.pop()

        # Remove the piece we placed
        self.set(move.to_x, move.to_y, EMPTY)

        # Restore the piece we removed
        if move.is_double():
            self.set(move.fr_x, move.fr_y, us)

        # Restore the pieces we captured
        for idx, val in enumerate(move.flipped):
            if val:
                square = SINGLES[idx]
                self.set(move.to_x + square[0], move.to_y + square[1], them)

        self.halfmove_clock -= 1
        self.turn = us

    def main_line(self):
        return self.history

    def legal_moves(self, side=None, full=False):
        if side is None:
            side = self.turn

        movelist = []
        for x in range(self.w):
            for y in range(self.h):
                # Singles
                if self.get(x, y) == EMPTY:
                    for n in SINGLES:
                        if self.get(x+n[0], y+n[1]) == side:

                            if full:
                                movelist.append(Move(x+n[0], y+n[1], x, y))
                            else:
                                movelist.append(Move(x, y, x, y))
                                break
                # Doubles
                elif self.get(x, y) == side:
                    for n in DOUBLES:
                        if self.get(x+n[0], y+n[1]) == EMPTY:
                            movelist.append(Move(x, y, x+n[0], y+n[1]))
        return movelist

    def is_legal(self, move):
        return move in self.legal_moves(full=True)

    def perft(self, depth, full=False):
        movelist = self.legal_moves()

        if depth == 0:
            return 1

        if depth == 1:
            return len(movelist)

        nodes = 0

        for move in movelist:
            self.makemove(move)
            nodes += self.perft(depth-1)
            self.undo()

        return nodes

    def parse_san(self, san):
        if type(san) is not str:
            raise Exception("TypeError")

        if len(san) not in [2, 4]:
            raise Exception(F"ValueError {san}")

        if len(san) == 2:
            san += san

        assert len(san) == 4

        # Moves should be given in lowercase
        # but we'll accept them regardless
        san = san.lower()

        if san[0] not in "abcdefgABCDEFG":
            raise Exception(F"ValueError {san}")

        if san[1] not in "1234567":
            raise Exception(F"ValueError {san}")

        if san[2] not in "abcdefgABCDEFG":
            raise Exception(F"ValueError {san}")

        if san[3] not in "1234567":
            raise Exception(F"ValueError {san}")

        fr_x = ord(san[0]) - ord('a') 
        fr_y = ord(san[1]) - ord('1')
        to_x = ord(san[2]) - ord('a')
        to_y = ord(san[3]) - ord('1')

        if fr_x < 0 or fr_x >= self.w or fr_y < 0 or fr_y >= self.h:
            raise Exception(F"ValueError {san}")

        return Move(fr_x, fr_y, to_x, to_y)

    def gameover(self):
        if self.fifty_move_draw():
            return True

        if self.max_length_draw():
            return True

        num_black, num_white, num_gaps, num_empty = self.count()
        if num_empty == 0 or num_black == 0 or num_white == 0:
            return True

        if self.legal_moves() == []:
            return True

        return False

    def result(self):
        if not self.gameover():
            return "*"

        num_black, num_white, num_gaps, num_empty = self.count()

        if num_black > num_white:
            return "1-0"
        elif num_white > num_black:
            return "0-1"
        else:
            return "1/2-1/2"
