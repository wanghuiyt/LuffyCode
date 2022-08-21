# 解决execjs执行js时产生的乱码报错，需要在导入该模块之前，让(subprocess)Popen的encoding参数锁定为utf-8
from functools import partial  # 锁定一个函数的参数
import subprocess
# 锁定subprocess.Popen的encoding参数为utf-8
subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")
import execjs

print(execjs.get().name)

# 读取js内容
f = open("myjs.js", mode="r", encoding="utf-8")
j = f.read()

# 先加载
jj = execjs.compile(j)
# 运行js文件中的某个函数
res = jj.call("fn", 1, 2)  # node xxx.js 控制台跑的 -> windows GBK
print(res)