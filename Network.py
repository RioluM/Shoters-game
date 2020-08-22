import pickle
import socket


class Network:
    def __init__(self, type=0):
        port = 5555
        host = "localhost"
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        if type == 1:
            self.socket.bind(("", port))
        else:
            self.socket.connect((host, port))
        self._header_size_ = 32

    def send(self, message, conn=False):
        if not conn:
            conn = self.socket
        msg = pickle.dumps(message)
        conn.sendall((f"{len(msg):<{self._header_size_}}".encode('utf-8')))
        conn.sendall(msg)

    def receive(self, conn=False):
        if not conn:
            conn = self.socket
        size = int(conn.recv(self._header_size_).decode('utf-8').strip())
        return pickle.loads(conn.recv(size))
