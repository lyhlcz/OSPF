from router import *
import os
import socket as sk


host = sk.gethostname() # 主机名
port = 8888             # 端口号


class network_server:
    def __init__(self):
        self.s = sk.socket()
        self.s.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
        self.s.bind((host, port))   #绑定端口

    def run(self):
        self.s.listen(5)


