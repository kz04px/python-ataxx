import ataxx
import queue
import re
import copy
from datetime import datetime

ANNOTATE_BRILLIANT_MOVE = "!!"
ANNOTATE_GOOD_MOVE      = "!"
ANNOTATE_MISTAKE        = "?"
ANNOTATE_BLUNDER        = "??"
ANNOTATE_INTERESTING    = "!?"
ANNOTATE_DUBIOUS        = "?!"

def parse_moves(board, parent, q):
    children = parent
    last_node = None

    while q.empty() == False:
        word = q.get()

        # Try parse the move
        try:
            move = ataxx.Move.from_san(word)
        except:
            move = None

        # We have a move
        if move and board.is_legal(move):
            # Create a new node
            node = Node()

            # Fill the node
            node.move = move
            if last_node:
                node.parent = last_node

            # Apply the move to the board
            board.makemove(move)

            # Add it
            children.append(node)

            # Set backups
            last_node = node
            last_children = children

            children = node.children
        # A comment just started
        elif word == "{":
            while True:
                if q.empty():
                    raise ValueError
                word = q.get()
                if word == "}":
                    break
                if last_node:
                    if last_node.comment == None:
                        last_node.comment = word
                    else:
                        last_node.comment += " " + word
        # An alternate line just started
        elif word == "(":
            nboard = copy.deepcopy(board)
            nboard.undo()
            n = parse_moves(nboard, last_children, q)
            if n != True:
                raise ValueError
        # An alternate line just finished
        elif word == ")":
            return True
        # We found a move number
        elif word[0].isdigit() and word[-1] == '.':
            pass
        # We found the game result
        elif word in ["1-0", "0-1", "1/2-1/2", "*"]:
            pass
        # Illegal token found
        else:
            raise ValueError

def parse(string):
    game = Game()
    board = ataxx.Board()

    q = queue.Queue()

    for line in string.split("\n"):
        if line == "\n" or len(line) < 2:
            continue

        # Header
        if line[0] == "[" and line[-1] == "]":
            key, *values = line[1:-1].split(" ")
            value = " ".join(values)[1:-1]

            # Store in the header
            game.headers[key] = value

            # Set the initial position if we get one
            if key.lower() == "fen":
                board.set_fen(value)
        # Moves
        else:
            # FIXME:
            # This is hideous
            for part in line.replace("{", " { ").replace("}", " } ").replace("(", " ( ").replace(")", " ) ").split(" "):
                # Ignore these
                if part in ["", " ", "\n"]:
                    continue

                q.put(part)

            parse_moves(board, game.root.children, q)

    return game

class MainLine():
    def __init__(self, start):
        self.start = start

    def __iter__(self):
        node = self.start
        while node.children:
            node = node.children[0]
            yield node

class Node():
    def __init__(self):
        # Tree
        self.parent = None
        self.children = []
        # Data
        self.move = None
        self.comment = None
        self.annotation = None

    def add_variation(self, move, comment=None, annotation=None):
        node = Node()
        node.move = move
        node.comment = comment
        node.annotation = annotation
        self.children.append(node)
        return node

    def add_main_variation(self, move, comment=None, annotation=None):
        node = Node()
        node.move = move
        node.comment = comment
        node.annotation = annotation
        self.children.insert(0, node)
        return node

    def main_line(self):
        return MainLine(self)

    def end(self):
        node = self
        while node.children:
            node = node.children[0]
        return node

class Game():
    def __init__(self):
        self.headers = {}
        self.headers["Event"] = "?"
        self.headers["Site"] = "?"
        self.headers["Date"] = datetime.today().strftime("%Y.%m.%d")
        self.headers["Round"] = "-"
        self.headers["White"] = "?"
        self.headers["Black"] = "?"
        self.headers["Result"] = '*'
        self.root = Node()

    def add_variation(self, move, comment=None, annotation=None):
        node = Node()
        node.move = move
        node.comment = comment
        node.annotation = annotation
        self.root.end().children.append(node)
        return node

    def from_board(self, board):
        node = self.root
        for move in board.history:
            node.add_main_variation(move)
            node = node.children[0]
        self.headers["Result"] = board.result()
        if board.start_fen() != ataxx.FEN_STARTPOS:
            self.headers["FEN"] = board.start_fen()
            self.headers["SetUp"] = "1"

    def set_white(self, w):
        self.headers["White"] = w

    def set_black(self, b):
        self.headers["Black"] = b

    def set_adjudicated(self, a):
        self.headers["Adjudicated"] = a

    def main_line(self):
        return self.root.main_line()

    def recurse(self, children=[], depth=1):
        if children == []:
            return ""

        string = ""
        main, *rest = children

        # Insert a space if there was a comment or variation previously
        if main.parent and (main.parent.comment or len(main.parent.children) > 1):
            string += ""

        if main.parent:
            string += ""

        # Print new move number
        if depth%2 == 1:
            string += F"{(depth+1)//2}. "
        # Print move number if we just left a comment or variation
        else:
            if main.parent and (main.parent.comment or len(main.parent.children) > 1):
                string += F"{depth//2}... "

        # Print main move
        if main.children:
            string += F"{main.move}"
        else:
            string += F"{main.move}"

        # Add comment
        if main.comment:
            string += F" {{ {main.comment} }}"

        # Print children
        if rest:
            # Always print the move number at the start of a variation
            if depth%2 == 0:
                string += F" ({depth//2}... {self.recurse(rest, depth)})"
            else:
                string += F" ({self.recurse(rest, depth)})"

        if main.children:
            string += " "

        string += self.recurse(main.children, depth+1)

        return string

    def __str__(self):
        string = ""

        for key, value in self.headers.items():
            string += F'[{key} "{value}"]\n'

        # One empty line between the headers and the moves
        string += "\n"

        # Moves
        string += self.recurse(self.root.children) + " " + self.headers["Result"]

        return string

class PGNIterator():
    def __init__(self, input_, is_string=False):
        self.path = input_
        self.file = None
        if is_string:
            self.iterator = iter(input_)
        else:
            self.file = open(self.path)
            self.iterator = iter(self.file)
        self.lines = []

    def __del__(self):
        if self.file:
            self.file.close()

    def __iter__(self):
        return self

    def get_string(self):
        # Make a copy of what we have
        complete = self.lines
        # Erase what we had
        self.lines = []
        # Return the game string
        # Every line should already end in "\n"
        return "".join(complete)

    def __next__(self):
        while True:
            try:
                line = self.iterator.__next__()
            except StopIteration:
                if self.lines == []:
                    raise StopIteration
                return self.get_string()

            # Have we found a new game?
            # "Event" should always be the first header listed
            if line.startswith("[Event"):
                # If this is our first game, collect more lines
                if self.lines == []:
                    self.lines.append(line)
                # If not, we already have a game saved up to return
                else:
                    complete = self.get_string()
                    self.lines.append(line)
                    return complete
            # Add to the current game string
            else:
                self.lines.append(line)

class GameIterator():
    def __init__(self, path, is_string=False):
        self.iterator = PGNIterator(path, is_string)

    def __iter__(self):
        return self

    def __next__(self):
        for string in self.iterator:
            try:
                return parse(string)
            except ValueError:
                pass
            except:
                raise
        raise StopIteration
