import socket as sk


host = sk.gethostname() # 主机名
port = 8888             # 端口号


class network_server:
    def __init__(self, cpids):
        self.cpids = cpids

        # socket connect test
        self.s = sk.socket()
        self.s.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
        self.s.bind((host, port))   #绑定端口

        self.s.listen(5)
        self.cls = [None, None, None, None, None]
        for i in range(5):
            c, addr = self.s.accept()
            #print('client:', addr)
            self.cls[int(addr[1])-10001] = c
            #c.send(bytes('hello！', encoding="utf-8"))


    def run(self):
        while True:
            buff = ['', '', '', '', '']
            for i in range(5):
                data_groups = str(self.cls[i].recv(1024), 'utf-8').split('$')
                #print(data_groups)
                for data in data_groups:
                    aim = int(data[0])-1
                    if aim == -1:
                        continue
                    buff[aim] = buff[aim] + '$' + data

            for i in range(5):
                if buff[i] is not '':
                    buff[i] = buff[i][1:]   # 去掉第一个‘$’
                    #print(buff[i])
                    self.cls[i].send(bytes(buff[i], encoding='utf-8'))
            #break