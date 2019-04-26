from router import *
from network import *
import os


class input_GUI():
    def __init__(self):
        self.flag = 0
        self.data = []
        self.root = Tk()
        self.root.title('OPSF')
        self.root.geometry('400x450+'+'800'+'+300')

        self.edge_labels = []
        for i in range(5):
            for j in range(i + 1, 5):
                self.edge_labels.append(Label(self.root, text=str(i+1) + ' -- ' + str(j+1)))
        for i in range(10):
            self.edge_labels[i].grid(row=i*5, column=0)

        self.edge_Texts = []
        for i in range(10):
            self.edge_Texts.append(Text(self.root, width=52, height=1))
            self.edge_Texts[i].grid(row=i*5+1, column=0, rowspan=2, columnspan=25)

        self.button = Button(self.root, text="确定", bg="lightgray", width=10, command=self.get_data)
        self.button.grid(row=60, column=1)

    def get_data(self):
        self.flag = 1
        for i in range(10):
            cost = self.edge_Texts[i].get(1.0, END)[:-1]
            if cost == '':
                cost = '999'
            self.data.append(int(cost))
        print(self.data)
        s = sk.socket()
        while s.connect_ex((sk.gethostname(), 6000)) != 0:
            pass
        s.send(bytes(str(self.data)[1:-1], encoding='utf-8'))
        s.close()

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    pid = os.fork()
    if pid == 0:
        # 输入网络拓扑数据
        win = input_GUI()
        win.run()
        exit(0)

    s = sk.socket()
    s.bind((sk.gethostname(), 6000))
    s.listen(5)
    c, _ = s.accept()
    data = str(c.recv(1024), 'utf=8').split(',')
    os.kill(pid, 9)

    # 初始化路由数据
    data = [int(x) for x in data]
    G = np.zeros([5, 5], dtype=int)
    index = 0
    for i in range(5):
        for j in range(i + 1, 5):
            G[i][j] = data[index]
            G[j][i] = data[index]
            index = index + 1
    # print(G)
    N = 5
    '''
    G = [
        [0, 5, 10, INF, INF],
        [5, 0, 3, 11, INF],
        [10, 3, 0, 2, INF],
        [INF, 11, 2, 0, INF],
        [INF, INF, INF, INF, 0]
    ]'''

    neighbors = []
    neighbors_cost = []
    for i in range(N):
        tmp = []
        tmp2 = []
        for j in range(N):
            if G[i][j] != INF and G[i][j] != 0:
                tmp = tmp + [j+1]
                if i < j:
                    tmp2 = tmp2 + [[i+1, j+1, G[i][j]]]
                else:
                    tmp2 = tmp2 + [[j+1, i+1, G[i][j]]]
        neighbors = neighbors + [tmp]
        neighbors_cost = neighbors_cost + [tmp2]

    fpid = os.getpid()
    cpids = []
    # 创建路由器
    for i in range(N):
        if fpid == os.getpid():
            pid = os.fork()
            if pid == 0:
                rid = i + 1
                r = ROUTER(rid, neighbors[i], neighbors_cost[i])
                r.run()
                break
            else:
                cpids = cpids + [pid]

    if fpid == os.getpid():
        # print(cpids)
        n = network_server(cpids)
        n.run()

        # 防止发生意外后子进程变为孤儿进程
        for p in cpids:
            os.kill(p, 9)
