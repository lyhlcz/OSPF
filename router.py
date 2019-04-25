import socket as sk
import os
from tkinter import *
import time
from tkinter import scrolledtext
import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import imageio


INF = 9999

host = sk.gethostname()     # 主机名
port = 8888                 # 端口号

time_size = 10   # 刷新时间间隔，单位秒

img = None
im = None

def tableToBytes(i, table):
    str_data = str(i) + '|'
    for l in table:
        tmp = ''
        for i in l:
            tmp = tmp + str(i) + ' '
        str_data = str_data + tmp + ';'
    # print(str_data)

    return bytes(str_data, encoding='utf-8')


def bytesToTable(bytes_data):
    table = []
    str_data = str(bytes_data, encoding='utf-8')
    i = str_data.split('|')[0]
    str_data = str_data.split('|')[1]
    lines = str_data.split(';')[:-1]
    for l in lines:
        tmp = l.split(' ')[:-1]
        table = table + [[int(x) for x in tmp]]
    # print('rec: ',table)

    return i, table


def resize(w, h, w_box, h_box, pil_image):
    f1 = 1.0 * w_box / w
    f2 = 1.0 * h_box / h
    factor = min([f1, f2])
    width = int(w * factor)
    height = int(h * factor)
    return pil_image.resize((width, height), Image.ANTIALIAS)


class router_GUI:
    def __init__(self, init_window_name, routerID, router_data):
        self.init_window_name = init_window_name
        self.rid = routerID
        self.rdata = router_data

    def set_init_window(self):
        global img, im

        self.init_window_name.title('Router' + str(self.rid))           # 窗口名
        self.init_window_name.geometry('380x800+'+str((self.rid-1)*380)+'+10')

        self.table_data_Text = scrolledtext.ScrolledText(self.init_window_name, width=50, height=35)
        self.table_data_Text.grid(row=0, column=0)
        self.table_data_Text.insert(1.0, '拓扑表'+str(self.rdata[0])+'\n证实表'+str(self.rdata[1])+'\n试探表'+str(self.rdata[2]))

        g = nx.Graph()
        g.clear()
        g.add_edge('A', 'B')
        g.add_edge('A', 'C')
        g.add_edge('C', 'B')
        g.add_edge('D', 'B')
        g.add_edge('C', 'D')
        nx.draw(g)
        plt.savefig('./tree'+str(self.rid)+'.png')
        img = Image.open('./tree'+str(self.rid)+'.png')
        w, h = img.size
        print(w, h)
        im = ImageTk.PhotoImage(resize(w, h, 360, 200, img))
        self.pic = Canvas(self.init_window_name, width=360, height=300)
        self.pic.create_image(150, 150, image=im)
        # img.close()

        self.pic.grid(row=1, column=0)


class ROUTER:
    def __init__(self, i, neighbor, neighbor_cost):
        self.ID = i
        self.neighbor = neighbor        # 邻居表
        self.topoTable = neighbor_cost  # 拓扑表: [起点号， 终点号， 花费]
        self.conTable = [[i, 0, -1]]    # 证实表: [目的地, 花费, 下一跳]
        self.testTable = []             # 试探表: [目的地, 花费, 下一跳]
        self.flag = -1                  # 是否已初始化链路状态
        # print(i, neighbor, neighbor_cost)

        self.gui_id = os.fork()
        if self.gui_id == 0:
            router_window = Tk()
            PORTAL = router_GUI(router_window, i, [self.topoTable, self.conTable, self.testTable])
            PORTAL.set_init_window()
            router_window.mainloop()

        self.router_name = str(i)
        self.port = 10080 + i
        self.s = sk.socket()

        # 持续连接直到连接成功
        while self.s.connect_ex((host, port)) != 0:
            pass
        print(str(self.ID), 'connecting success')

    # 接收路由表(更新试探表)
    def recTable(self, message):
        rid, table_data = bytesToTable(message)
        if rid != self.flag and self.flag != -1:
            return -1
        tmp = [x[0] for x in self.testTable]
        tmp2 = [x[0] for x in self.conTable]

        for i, t in enumerate(table_data):
            if t[0] in tmp:
                j = tmp.index(t[0])
                if self.testTable[j][1] > t[1]:
                    self.testTable[j] = t
                del(table_data[i])
            elif t[0] in tmp2:
                del(table_data[i])

        self.testTable = self.testTable + table_data
        return 0

    def test(self):
        self.s.connect((host, port))
        self.s.send(bytes('it\'s router'+str(self.ID), encoding='utf-8'))
        self.s.close()

    # 发送拓扑数据库
    def sendTable(self):
        bytes_data  = tableToBytes(self.ID, self.conTable)
        return bytes_data

    # 更新证实表
    def updateTable(self):
        # 找最小费用
        min_cost = INF
        k = -1
        for i, c in enumerate(self.testTable):
            if c[1] < min_cost:
                min_cost = c[1]
                k = i
        # print('k = ', k, '  min = ', min_cost)
        if k < 0:
            print('error')
            exit(1)
        else:
            self.conTable = self.conTable + [self.testTable[k]]
            self.flag = self.testTable[k][0]    # 更新结点
            del(self.testTable[k])

        # self.testTable = []
        return

    # 刷新显示数据
    def updateGUI(self):
        os.kill(self.gui_id, 9)
        self.gui_id = os.fork()
        if self.gui_id == 0:
            router_window = Tk()
            PORTAL = router_GUI(router_window, self.ID, [self.topoTable, self.conTable, self.testTable])
            PORTAL.set_init_window()
            router_window.mainloop()

    # 输出路由表信息
    def display(self):
        print('ROUTER ', self.ID)
        print('Confirm Table: ', self.conTable)
        print('Test Table: ', self.testTable)
        print('Flag: ', self.flag)
        print()

    def run(self):
        while True:
            # 定时
            time.sleep(time_size)

            # 交换路由数据


            # 更新数据


            # 刷新界面
            self.updateGUI()
            # print(time.time())


if __name__ == '__main__':
    # r = ROUTER(4)
    # r.display()
    # d = tableToBytes([[1,2,3],[2,3,4],[8,5,56]])
    # bytesToTable(d)

    '''
    print('>>', end='')
    ss = input()
    while ss != 'exit':
        if ss == 'up':
            r.updateTable()
        else:
            r.recTable(bytes(ss, encoding='utf-8'))
        r.display()
        print('>>', end='')
        ss = input()

    ss = [
        '2|2 11 2 ;',
        '3|3 2 3 ;',
        'up',
        '3|2 5 3 ;1 12 3 ;',
        'up',
        '2|1 10 3 ;',
        'up'
    ]
    for s in ss:
        if s != 'up':
            r.recTable(bytes(s, encoding='utf-8'))
        else:
            r.updateTable()
        r.display()
        print()
    '''
