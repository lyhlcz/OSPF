from tkinter import *
import time
from tkinter import scrolledtext


LOG_LINE_NUM = 0


class MY_GUI:
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name

    # 设置窗口
    def set_init_window(self):
        self.init_window_name.title("OSPF模拟")           # 窗口名
        self.init_window_name.geometry('1450x750+10+10')

        # 标签
        self.router_labels = []
        for i in range(5):
            self.router_labels = self.router_labels + [Label(self.init_window_name, text="router"+str(i+1))]
            self.router_labels[i].grid(row=0, column=i*30)

        self.edge_value_label = Label(self.init_window_name, text='edge cost')
        self.edge_value_label.grid(row=15, column=120)
        self.edge_labels = []
        for i in range(5):
            for j in range(i+1, 5):
                self.edge_labels = self.edge_labels + [Label(self.init_window_name, text=chr(65+i) + chr(65+j))]
        for i in range(10):
            self.edge_labels[i].grid(row=16+i*5, column=120)

        # 文本框
        self.router_Texts = []
        for i in range(5):
            self.router_Texts = self.router_Texts + [scrolledtext.ScrolledText(self.init_window_name, width=52, height=15)]
            self.router_Texts[i].grid(row=1, column=i*30, rowspan=10, columnspan=30)

        self.edge_Texts = []
        for i in range(10):
            self.edge_Texts = self.edge_Texts + [Text(self.init_window_name, width=52, height=2)]
            self.edge_Texts[i].grid(row=16+i*5+1, column=120, rowspan=2, columnspan=30)
        '''
        self.init_data_Text = scrolledtext.ScrolledText(self.init_window_name, width=67, height=35)  # 原始数据录入框
        self.init_data_Text.grid(row=1, column=0, rowspan=10, columnspan=10)
        self.mid_data_Text = scrolledtext.ScrolledText(self.init_window_name, width=50, height=49)  # 处理中间结果
        self.mid_data_Text.grid(row=1, column=12, rowspan=15, columnspan=10)
        self.result_data_Text = scrolledtext.ScrolledText(self.init_window_name, width=70, height=49)  # 处理结果展示
        self.result_data_Text.grid(row=1, column=56, rowspan=15, columnspan=10)
        self.log_data_Text = scrolledtext.ScrolledText(self.init_window_name, width=66, height=15)  # 日志框
        self.log_data_Text.grid(row=13, column=0, columnspan=10)'''


        #画布
        self.network_canvas = Canvas(self.init_window_name, width=500, height=500)
        self.network_canvas.grid(row=15, column=0, rowspan=50, columnspan=60)
        self.network_canvas.create_line(0, 0, 500, 500)

        # 按钮
        '''
        self.str_trans_to_md5_button = Button(self.init_window_name, text="编译", bg="lightgray", width=10,command=self.Compile_Run)  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button.grid(row=20, column=11)'''
        # 读取源代码
        '''f = open("code.txt", "r")
        self.init_data_Text.insert(1.0, f.read())
        f.close()'''
        #self.init_data_Text.insert(1.0, 'test')

    # 功能函数
    def Compile_Run(self):
        src = self.init_data_Text.get(1.0, END).strip().replace("\n", "").encode()
        src1 = self.init_data_Text.get(1.0, END)

        # 保存修改内容
        f = open("code.txt", "w")
        f.write(src1)
        f.close()

        # 分析源程序
        result, message = GL.grammaticalAnalysis()

        if result:
            # 语法制导翻译

            # 读取单词分析结果
            f1 = open("after_preprocess_code")
            mid = f1.read()
            f1.close()

            # 读取中间代码文件
            f2 = open("result.txt")
            result = f2.read()
            f2.close()
        else:
            mid = ""
            result = ""

        try:
            # 输出到界面
            self.result_data_Text.delete(1.0, END)
            self.result_data_Text.insert(1.0, result)
            self.mid_data_Text.delete(1.0, END)
            self.mid_data_Text.insert(1.0, mid)
            self.write_log_to_Text(message)
        except:
            self.result_data_Text.delete(1.0, END)
            self.result_data_Text.insert(1.0, "Run failed!")

    # 获取当前时间
    @staticmethod
    def get_current_time():
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return current_time

    # 日志动态打印
    def write_log_to_Text(self, logmsg):
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        logmsg_in = str(current_time) + " " + str(logmsg) + "\n"      # 换行
        if LOG_LINE_NUM <= 7:
            self.log_data_Text.insert(END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.log_data_Text.delete(1.0, 2.0)
            self.log_data_Text.insert(END, logmsg_in)


class router_GUI:
    def __init__(self, init_window_name, routerID):
        self.init_window_name = init_window_name
        self.rid = routerID

    def set_init_window(self):
        self.init_window_name.title('Router' + str(self.rid))           # 窗口名
        self.init_window_name.geometry('450x750+10+10')

        self.table_data_Text = scrolledtext.ScrolledText(self.init_window_name, width=60, height=35)
        self.table_data_Text.grid(row=0, column=0)
        self.table_data_Text.insert(1.0, self.rid)


if __name__ == "__main__":
    init_window = Tk()              # 实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()

    init_window.mainloop()          # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示