import subprocess
import threading

class Process():
    def __init__(self, path, engine):
        options = {"stdout": subprocess.PIPE, "stdin": subprocess.PIPE, "bufsize": 1, "universal_newlines": True}
        self.process = subprocess.Popen(path, stdout=subprocess.PIPE, stdin=subprocess.PIPE, bufsize=1)

        self.engine = engine
        self.stop = threading.Event()

        self.listener = threading.Thread(target=self.recv_thread)
        self.listener.daemon = True
        self.listener.start()

    def send_line(self, line):
        if self.is_alive():
            self.process.stdin.write((line + '\n').encode('utf-8'))
            self.process.stdin.flush()

    def recv_thread(self):
        while not self.stop.is_set():
            line = self.process.stdout.readline().decode('utf-8').rstrip()
            self.engine.recv_line(line)

    def is_alive(self):
        return self.process.poll() == None

    def pid(self):
        return self.process.pid()

    def terminate(self):
        self.stop.set()
        self.process.terminate()
        self.process.stdout.close()
        self.process.stdin.close()
        return self.process.wait()

    def kill(self):
        self.process.kill()
        self.stop.set()
        return self.process.wait()
