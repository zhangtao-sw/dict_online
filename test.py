import struct
import getpass
import multiprocessing
import socket
import hashlib
import re

fd=open("dict.txt","r")
for line in fd:
    res = re.findall(r'(\S+)\s+(.*)',line)[0]
    print(res)
    break