import struct
import getpass
import multiprocessing
import socket
import hashlib
import re
from multiprocessing import Process
class Text:
    def __init__(self):
        self.num = 10

    def Start(self):
        read = Process(target = self.read)
        write = Process(target = self.write)

        read.start()
        write.start()

        read.join()
        write.join()

    def read(self):
        print (self.num)

    def write(self):
        print (self.num)

# Text().Start()

temp=(14, 'zhangtao', 'class',"2015-18-14-55-8")
meg="%s  %-8s  %-50s"%(temp[1],temp[2],temp[3])
print (meg)
temp=(14, 'zhangtao', 'ee',"2015-18-14-55-8-34-778")
meg="%s  %-8s  %-50s"%(temp[1],temp[2],temp[3])
print (meg)