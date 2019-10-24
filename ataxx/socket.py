import subprocess
import threading

class Socket():
    def __init__(self, sck, engine):
        self.socket = sck

        self.engine = engine
        self.stop = threading.Event()

        self.alive = True

        self.listener = threading.Thread(target=self.recv_thread)
        self.listener.daemon = True
        self.listener.start()

    def send_line(self, line):
        if self.is_alive():
            if self.socket.send((line + '\n').encode('utf-8')) == 0:
                self.alive = False
                print('Socket closed during send')
                self.engine.recv_line(None)

    def recv_thread(self):
        buffer = bytearray()

        while not self.stop.is_set():
            while True:
                if b'\r\n' in buffer or b'\n' in buffer:
                    break

                chunk = self.socket.recv(1500)
                if not chunk:
                    self.alive = False
                    print('Socket closed during recv')
                    self.engine.recv_line(None)
                    break

                #print('received data "%s"' % chunk)

                buffer.extend(chunk)

                if b'\r\n' in buffer or b'\n' in buffer:
                    break

            if not self.alive:
                break

            end = buffer.find(b'\r\n')
            if end >= 0:
                line = buffer[:end]
                line = line.decode('utf-8').rstrip()
                buffer = buffer[end + 2:]
            else:
                end = buffer.find(b'\n')

                line = buffer[:end]
                line = line.decode('utf-8').rstrip()
                buffer = buffer[end + 1:]

            #print('line: "%s"' % line)

            self.engine.recv_line(line)

    def is_alive(self):
        return self.alive

    def pid(self):
        return 1

    def terminate(self):
        self.kill()

    def kill(self):
        self.stop.set()
        self.socket.close()
        return True
