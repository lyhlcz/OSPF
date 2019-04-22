from router import *
import os


G = [
    [0, 5, 10, INF, INF],
    [5, 0, 3, 11, INF],
    [10, 3, 0, 2, INF],
    [INF, 11, 2, 0, INF],
    [INF, INF, INF, INF, 0]
]


if __name__ == '__main__':
    fpid = os.getpid()
    cpids = []
    # 创建进程
    for i in range(5):
        if fpid == os.getpid():
            pid = os.fork()
            if pid == 0:
                rid = i + 1
                r = ROUTER(rid, [])
                r.run()
                break
            else:
                cpids = cpids + [pid]

    if fpid == os.getpid():
        print(cpids)
        init_window = Tk()
        ZMJ_PORTAL = MY_GUI(init_window)
        ZMJ_PORTAL.set_init_window()
        init_window.mainloop()
