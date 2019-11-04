from socket import *


class Dict_Client:
    def __init__(self):
        self.addr = ("127.0.0.1", 10086)

    def create_socket(self):
        s = socket()
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s.connect(self.addr)
        return s

    def run(self):
        s = self.create_socket()
        while True:
            s.send(b"ok")
            data=s.recv(1024)


if __name__ == '__main__':
    client = Dict_Client()
    client.run()
