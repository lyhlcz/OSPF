import numpy as np

INF = 999


class GRAPH:
    def __init__(self, G_Matrix):
        self.G = G_Matrix
        self.N = G_Matrix.shape[1]

    # G 邻接矩阵
    # I 源结点号

    def DJ(self, I):
        # 初始化辅助数组
        last = -np.ones([1, self.N])[0]
        cost = np.zeros([1, self.N])[0]
        flag = np.zeros([1, self.N])[0]

        # 初始化
        flag[I] = 1
        for i in range(self.N):
            if self.G[I][i] != INF:
                cost[i] = self.G[I][i]
                last[i] = I
            else:
                cost[i] = INF

        for i in range(self.N-1):
            print(cost, " ", last, " ", flag)
            # 求下一个结点
            min_cost = INF
            for j in range(self.N):
                if flag[j] == 0 and cost[j] < min_cost:
                    min_cost = cost[j]
                    k = j
            flag[k] = 1

            print(str(k)+'->')

            # 更新cost
            for j in range(self.N):
                if flag[j] == 0:
                    tmp = cost[k] + self.G[k][j]
                    if tmp < cost[j]:
                        cost[j] = tmp
                        last[j] = k
        return


if __name__ == "__main__":
    G = GRAPH(np.array([
        [INF, INF,   2,   5,   4,  INF],
        [INF, INF,   3,   1, INF,    2],
        [  2,   3, INF,   3, INF,    4],
        [  5,   1,   3, INF,   2,  INF],
        [  4, INF, INF,   2, INF,  INF],
        [INF,   2,   4, INF, INF,  INF]
    ]))
    G.DJ(0)
