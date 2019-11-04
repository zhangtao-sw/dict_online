from socket import *
import os
from multiprocessing import Process


class Dict_Server:
    def __init__(self):
        self.addr = ("127.0.0.1", 10086)

    def run(self):
        s = self.create_socket()
        while True:
            try:
                c, add = s.accept()
                print("Connect from", add)
            except KeyboardInterrupt:
                os._exit(0)
            except Exception as e:
                print(e)
                continue
            client = Process(target=self.do_request, args=(c,))
            client.daemon = True
            client.start()

    def do_request(self, c):
        data = c.recv(1024)
        print(data)

    def create_socket(self):
        s = socket()
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s.bind(self.addr)
        s.listen(3)
        # signal.signal(signal.SIGCHLD, signal.SIG_IGN)
        print("begin to listening port:", self.addr[1])
        return s


if __name__ == '__main__':
    server = Dict_Server()
    server.run()
