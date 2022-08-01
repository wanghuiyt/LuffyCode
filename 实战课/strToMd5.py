from tkinter import *
import hashlib
import time

LOG_LINE_NUM = 0


class MyGUI:
    def __init__(self, init_windows_name):
        self.init_windows_name = init_windows_name  # type: Tk

    def set_init_window(self):  # 设置窗口
        self.init_windows_name.title("MD5转换工具")  # 设置窗口名称
        self.init_windows_name.geometry("1068x681+10+10")  # 1068 681为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_windows_name["bg"] = "pink"  # 窗口背景颜色，其他背景色见:blog.csdn.net/ch10000/article/details/7657887
        self.init_windows_name.attributes("-alpha", 0.9)  # 虚化，值越小虚化程度越高
        # 标签
        self.init_data_label = Label(self.init_windows_name, text="待处理数据")
        self.init_data_label.grid(row=0, column=0)
        self.result_data_label = Label(self.init_windows_name, text="输出结果")
        self.result_data_label.grid(row=0, column=12)
        self.log_label = Label(self.init_windows_name, text="日志")
        self.log_label.grid(row=12, column=0)
        # 文本框
        self.init_data_Text = Text(self.init_windows_name, width=67, height=35)  # 原始数据录入框
        self.init_data_Text.grid(row=1, column=0, rowspan=10, columnspan=10)
        self.result_data_Text = Text(self.init_windows_name, width=70, height=49)  # 处理结果展示
        self.result_data_Text.grid(row=1, column=12, rowspan=15, columnspan=10)
        self.log_data_Text = Text(self.init_windows_name, width=66, height=9)  # 日志框
        self.log_data_Text.grid(row=13, column=0, columnspan=10)
        # 单选框
        self.radio_label = Label(self.init_windows_name, text="是否大写")
        self.radio_label.grid(row=0, column=11)
        self.v = BooleanVar()
        self.radio_button = Radiobutton(self.init_windows_name, text="是", bg="lightblue", width=10, variable=self.v, value=True)
        self.radio_button.grid(row=1, column=11)
        self.radio_button2 = Radiobutton(self.init_windows_name, text="否", bg="lightblue", width=10, variable=self.v, value=False)
        self.radio_button2.grid(row=2, column=11)
        # 按钮
        self.str_trans_tomd5_button = Button(self.init_windows_name, text="字符串转MD5", bg="lightblue", width=10, command=self.str_trans_to_md5)  # 调用内部方法，加()为直接调用
        self.str_trans_tomd5_button.grid(row=3, column=11)

    def str_trans_to_md5(self):
        print(self.v.get())
        src = self.init_data_Text.get(1.0, END).strip().replace("\n", "").encode()
        if src:
            try:
                myMd5 = hashlib.md5()
                myMd5.update(src)
                myMd5_Digest = myMd5.hexdigest()
                if self.v.get():
                    myMd5_Digest = myMd5_Digest.upper()
                # 输出到界面
                self.result_data_Text.delete(1.0, END)
                self.result_data_Text.insert(1.0, myMd5_Digest)
                self.write_log_to_text("INFO:str_trans_to_nd5 success")
            except:
                self.result_data_Text.delete(1.0, END)
                self.result_data_Text.insert(1.0, "字符串转MD5失败")
        else:
            self.write_log_to_text("INFO:str_trans_to_nd5 success")

    # 获取当前时间
    def get_current_time(self):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        return current_time

    # 日志动态打印
    def write_log_to_text(self, msg):
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        msg_in = f"{current_time} {msg}\n"
        if LOG_LINE_NUM <= 7:
            self.log_data_Text.insert(END, msg_in)
            LOG_LINE_NUM += 1
        else:
            self.log_data_Text.delete(1.0, 2.0)
            self.log_data_Text.insert(END, msg_in)


def gui_start():
    # 实例化一个父窗口
    init_window = Tk()
    gui = MyGUI(init_window)
    # 设置根窗口默认属性
    gui.set_init_window()
    # 父窗口进入时间循环，可以理解为保持窗口运行，否则界面不显示
    init_window.mainloop()


if __name__ == '__main__':
    gui_start()

