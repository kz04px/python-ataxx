import ataxx
import queue
import re
import copy

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

        # We have a move
        if word in [str(n) for n in board.legal_moves()]:
            # Create a new node
            node = Node()

            # Get the move
            move = board.parse_san(word)

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
                word = q.get()
                if word == "}":
                    break
                if last_node.comment == None:
                    last_node.comment = word
                else:
                    last_node.comment += " " + word
        # An alternate line just started
        elif word == "(":
            nboard = copy.deepcopy(board)
            nboard.undo()
            parse_moves(nboard, last_children, q)
        # An alternate line just finished
        elif word == ")":
            break

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

    def add_main_variation(self, move, comment=None, annotation=None):
        node = Node()
        node.move = move
        node.comment = comment
        node.annotation = annotation
        self.children.insert(0, node)

    def main_line(self):
        return MainLine(self)

class Game():
    def __init__(self):
        self.headers = {}
        self.headers["Event"] = "Example"
        self.root = Node()

    def from_board(self, board):
        node = self.root
        for move in board.history:
            node.add_main_variation(move)
            node = node.children[0]

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

        # Headers -- put "Event" first
        if "Event" in self.headers.keys():
            key = "Event"
            value = self.headers["Event"]
            string += F"[{key} \"{value}\"]\n"

        # Headers -- put the rest afterwards
        for key, value in self.headers.items():
            if key == "Event":
                continue
            string += F"[{key} \"{value}\"]\n"

        # One empty line between the headers and the moves
        string += "\n"

        # Moves
        string += self.recurse(self.root.children) + " " + self.headers["Result"]

        return string

class PGNIterator():
    def __init__(self, path):
        self.path = path
        self.iterator = iter(open(self.path))
        self.lines = []

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
    def __init__(self, path):
        self.iterator = PGNIterator(path)

    def __iter__(self):
        return self

    def __next__(self):
        for string in self.iterator:
            return parse(string)
        raise StopIteration
