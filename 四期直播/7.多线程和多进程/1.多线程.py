from threading import Thread


# # 多线程
# # 一个函数，多线程多进程中表示一个任务
# def work():
#     for i in range(1000):
#         print("work中的打印", i)
#
#
# # 一个程序在被运行起来时，会产生一个进程，进程中会有有一个默认的线程
# # 默认的进程和线程，我们叫它主进程和主线程
# if __name__ == '__main__':
#     # work()  # 函数的调用，和多线程无关
#     t = Thread(target=work)  # 创建一个线程
#     # 想要运行这个线程，需要start()
#     t.start()  # 启动这个线程
#
#     for i in range(1000):
#         print("主进程中的打印", i)
def work(name):
    for i in range(1000):
        print(f"work中的打印{name}: {i}")


def get_one_year_info(year):
    try:
        pass
    except Exception as e:
        pass


if __name__ == '__main__':
    # target的参数不能加括号
    # args必须是元组，如果只有一个参数，必须加括号
    # t1 = Thread(target=work, args=("线程1",))
    # t1.start()
    #
    # t2 = Thread(target=work, args=("线程2",))
    # t2.start()
    #
    # t3 = Thread(target=work, args=("线程3",))
    # t3.start()

    for i in range(1995, 2021):
        t = Thread(target=get_one_year_info, args=(i,))
        t.start()
    # 1.CPU未必扛得住
    # 2.创建线程也要消耗资源
    # 3.对方的服务器扛不住
    # 线程数量不易太多，一般选择CPU核数*2  普通电脑 8-16
    # python直接提供了线程池，帮助我们管理和监听任务的执行和分配
    # 线程池：装有一堆线程的一个池子，我们只需要把任务交进去就可以了
