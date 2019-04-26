from router import *
from network import *
import os


if __name__ == '__main__':
    # 初始化路由数据
    N = 5
    G = [
        [0, 5, 10, INF, INF],
        [5, 0, 3, 11, INF],
        [10, 3, 0, 2, INF],
        [INF, 11, 2, 0, INF],
        [INF, INF, INF, INF, 0]
    ]
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
