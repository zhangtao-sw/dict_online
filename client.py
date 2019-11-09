from socket import *
import sys
import getpass


class Dict_Client:
    def __init__(self):
        self.addr = ("127.0.0.1", 10086)
        self.s = self.create_socket()

    def create_socket(self):
        s = socket()
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s.connect(self.addr)
        return s

    def do_register(self):
        while True:
            name = input("please input your name:")
            pasword = getpass.getpass("please input your password:")
            if " " in pasword or " " in name:
                print("用户名和密码不能有空格！重新输入")
                continue
            msg = "R" + " " + name + " " + pasword
            self.s.send(msg.encode())
            backmsg = self.s.recv(10).decode()
            if backmsg == "OK":
                print("注册成功!")
                self.sec_dir(name)
                break
            else:
                print("注册失败:", backmsg)

    def do_login(self):
        while True:
            name = input("please input your name:")
            pasword = getpass.getpass("please input your password:")
            if " " in pasword or " " in name:
                print("用户名和密码不能有空格！重新输入")
                continue
            msg = "L" + " " + name + " " + pasword
            self.s.send(msg.encode())
            backmsg = self.s.recv(10).decode()
            if backmsg == "OK":
                print("登入成功!")
                self.sec_dir(name)
                break
            else:
                print("登入失败:", backmsg)
    def do_query_word(self,name):
        while True:
            word=input("please input your query word:")
            if word=="#":
                break
            msg = "Q" + " " +name+" "+ word
            self.s.send(msg.encode())
            backmsg = self.s.recv(2048).decode()
            print (backmsg)
    def do_query_his(self,name):
        while True:
            name=input("please input your query name:")
            if name=="#":
                break
            msg = "H" + " " +name
            self.s.send(msg.encode())
            backmsg = self.s.recv(10).decode()
            if backmsg=="OK":
                temp_msg=""
                while True:
                    data=self.s.recv(100).decode()
                    if data=="#":
                        break
                    temp_msg=temp_msg+data+"\r\n"
                print (temp_msg)
            else:
                print ("fail")


    def sec_dir(self,name):
        while True:
            print("""
            =============Welcome=======================
            1. 查询单词　　　2.　查询历史记录　　3. 退出
            ===========================================
            """)
            cmd = input("输入选项:")
            if cmd =="1":
                self.do_query_word(name)
            elif cmd=="2":
                self.do_query_his(name)
            elif cmd=="3":
                self.s.send(b'E')
                break

    def run(self):
        while True:
            print("""
            =============Welcome===========
            1. 注册　　　2.　登录　　3. 退出
            ===============================
            """)
            cmd = input("输入选项:")
            if cmd == '1':
                self.do_register()
            elif cmd == '2':
                self.do_login()
            elif cmd == '3':
                self.s.send(b'E')
                sys.exit("谢谢使用")
            else:
                print("请输入正确选项")


if __name__ == '__main__':
    client = Dict_Client()
    client.run()
