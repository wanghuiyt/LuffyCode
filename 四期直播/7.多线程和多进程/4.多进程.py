from multiprocessing import Process
from concurrent.futures import ProcessPoolExecutor


def func(name):
    for i in range(1000):
        print("func", name, i)


if __name__ == '__main__':
    p1 = Process(target=func, args=("进程1",))
    p2 = Process(target=func, args=("进程2",))
    p3 = Process(target=func, args=("进程3",))

    p1.start()
    p2.start()
    p3.start()

    with ProcessPoolExecutor(10) as p:
        for i in range(4):
            p.submit(func, "进程{i}")
