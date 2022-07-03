# selenuim的包都很长
# 导入驱动的py包
from selenium.webdriver import Chrome, ChromeOptions

options = ChromeOptions()
options.binary_location = r"D:\SoftWare\Google\Chrome\Application\chrome.exe"
web = Chrome(options=options)

# 设置最大窗口
web.maximize_window()
# 打开url
web.get("https://www.baidu.com/")
# # 拿到一些内容
# print(web.title)
