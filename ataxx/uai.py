import threading
import ataxx
import ataxx.process
import ataxx.socket

class Engine():
    def __init__(self, target, is_socket = False):
        self.client = ataxx.socket.Socket(target, self) if is_socket else ataxx.process.Process(target, self)
        self.name = None
        self.author = None

        self.bestmove = None
        self.ponder = None

        self.uaiok_received = threading.Condition()
        self.readyok_received = threading.Condition()
        self.bestmove_received = threading.Condition()

    def send_line(self, line):
        return self.client.send_line(line)

    def recv_line(self, line):
        if line == None:
            with self.uaiok_received:
                self.uaiok_received.notify_all()
            with self.readyok_received:
                self.readyok_received.notify_all()
            with self.bestmove_received:
                self.bestmove_received.notify_all()

            return

        words = line.split(' ')

        # FIXME:
        if len(words) > 2 and words[0] == "id" and words[1] == "name":
            self.name = ' '.join(words[2:])
        if len(words) > 2 and words[0] == "id" and words[1] == "author":
            self.author = ' '.join(words[2:])

        if len(words) > 1 and words[0] == "warn":
            print(line)

        if len(words) == 1:
            if words[0] == "uaiok":
                with self.uaiok_received:
                    self.uaiok_received.notify_all()
            elif words[0] == "readyok":
                with self.readyok_received:
                    self.readyok_received.notify_all()

        elif len(words) == 2:
            if words[0] == "bestmove":
                with self.bestmove_received:
                    self.bestmove = words[1]
                    self.bestmove_received.notify_all()

        elif len(words) == 3:
            if words[0] == "id" and words[1] == "name":
                self.name = words[2]
            elif words[0] == "id" and words[1] == "author":
                self.author = ' '.join(words[2:])

        elif len(words) == 4:
            if words[0] == "bestmove" and words[2] == "ponder":
                with self.bestmove_received:
                    self.bestmove = words[1]
                    self.ponder = words[3]
                    self.bestmove_received.notify_all()

        else:
            #print('"%s" not understood' % line)
            pass

    def uai(self):
        with self.uaiok_received:
            self.send_line("uai")
            self.uaiok_received.wait()

    def isready(self, to=0):
        with self.readyok_received:
            self.send_line("isready")

            if to:
                self.readyok_received.wait(to)
            else:
                self.readyok_received.wait()

    def uainewgame(self):
        self.send_line("uainewgame")

    def position(self, fen, moves=None):
        if moves:
            self.send_line(F"position fen {fen} moves {moves}")
        else:
            self.send_line(F"position fen {fen}")

    def go(self, times=None, movetime=None, depth=None, nodes=None, maxwait=None):
        self.bestmove = None

        with self.bestmove_received:
            if times:
                btime, wtime, binc, winc = times
                self.send_line(F"go btime {btime} wtime {wtime} binc {binc} winc {winc}")
            elif movetime:
                self.send_line(F"go movetime {movetime}")
            elif depth:
                self.send_line(F"go depth {depth}")
            elif nodes:
                self.send_line(F"go nodes {nodes} simulations {nodes}")

            if maxwait:
                self.bestmove_received.wait(maxwait)
            else:
                self.bestmove_received.wait()

        return self.bestmove, self.ponder

    def perft(self, depth):
        self.send_line(F"perft {depth}")

    def setoption(self, name, value):
        self.send_line(F"setoption name {name} value {value}")

    def quit(self):
        # FIXME:
        with self.bestmove_received:
            self.bestmove_received.notify_all()
        self.send_line("quit")
        self.client.terminate()
