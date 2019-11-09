from socket import *
import sys
from multiprocessing import Process
import db
import signal
from time import sleep


class Dict_Server:
    def __init__(self):
        self.addr = ("127.0.0.1", 10086)
        self.db_obj = db.SqlDB()  #db 对象

    def run(self):
        s = self.create_socket()
        while True:
            try:
                c, add = s.accept()
                print("Connect from", add)
            except KeyboardInterrupt:
                db_obj.close()  # 关闭数据库连接
                os._exit(0)
            except Exception as e:
                print(e)
                continue
            client = Process(target=self.do_request, args=(c,))
            client.daemon = True
            client.start()

    def do_request(self, c):
        self.db_obj.creat_cur()  #每个子进程创建不同的游标
        while True:
            data = c.recv(1024)
            print(data)
            temp = data.decode().split(" ")[0]
            if not data or temp == "E":
                self.db_obj.exit_()
                sys.exit("exit")
            elif temp == "R":
                self.do_register(c, data)
            elif temp == "L":
                self.do_login(c,data)
            elif temp == "Q":
                self.do_query(c,data)
            elif temp =="H":
                self.do_his(c,data)
    def do_his(self,c,data):
        name = data.decode().split(" ")[1]
        resp=self.db_obj.his(name)
        if not resp:
            msg="不存在这个名字"
            c.send(msg.encode())
            return
        c.send(b"OK")
        sleep(0.1)
        for temp in resp:
            msg="%s  %-20s  %-40s"%(temp[1],temp[2],temp[3])
            c.send(msg.encode())
            sleep(0.1)
        c.send(b"#")


    def do_query(self,c,data):
        name = data.decode().split(" ")[1]
        word = data.decode().split(" ")[2]
        resp=self.db_obj.query(name,word)
        if not resp:
            msg="不存在这个单词"
            c.send(msg.encode())
            return
        msg=resp[-1]
        print (msg)
        c.send(msg.encode())

    def do_register(self, c, data):
        name = data.decode().split(" ")[1]
        password = data.decode().split(" ")[2]
        if not self.db_obj.register(name, password):
            meg = "Fail"
        else:
            meg = "OK"
        c.send(meg.encode())

    def do_login(self, c, data):
        name = data.decode().split(" ")[1]
        password = data.decode().split(" ")[2]
        if not self.db_obj.login(name, password):
            meg = "Fail"
        else:
            meg = "OK"
        c.send(meg.encode())

    def create_socket(self):
        s = socket()
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s.bind(self.addr)
        s.listen(3)
        signal.signal(signal.SIGCHLD, signal.SIG_IGN)  #window无法使用
        print("begin to listening port:", self.addr[1])
        return s


if __name__ == '__main__':
    server = Dict_Server()
    server.run()
