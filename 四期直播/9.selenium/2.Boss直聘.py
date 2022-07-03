import time

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # 所有按键的指令

options = ChromeOptions()
options.binary_location = r"D:\SoftWare\Google\Chrome\Application\chrome.exe"
web = Chrome(options=options)
# web.maximize_window()
web.get("https://www.zhipin.com/beijing/")

# 找到那个框框
# 当你使用find_xxx如果找不到东西，它会报错。也有可能不是下面代码的问题，而是浏览器没有加载完成
input_el = web.find_element(By.XPATH, '//*[@id="wrap"]/div[3]/div/div[1]/div[1]/form/div[2]/p/input')
# 向框框输入内容，敲回车
input_el.send_keys("python", Keys.ENTER)  # 输入回车
# 剩下的事情，抓数据就完了
time.sleep(5)
li_list = web.find_elements(By.XPATH, '//div[@class="search-job-result"]/ul/li')
# print(len(li_list))
for li in li_list:
    # selenium用的不是一个标准的xpath语法规则
    # 最后一项不可以是@xxx，text()
    a = li.find_element(By.XPATH, ".//a")
    href = a.get_property("href")  # @href
    name = a.find_element(By.XPATH, ".//span[@class='job-name']").text  # 直接 节点.text
    salary = a.find_element(By.XPATH, ".//span[@class='salary']").text
    # print(href, name, salary)
    a.click()  # 点击
    time.sleep(2)
    # 如果弹出了新窗口，那么你需要把程序调整到新窗口里，才能开始采集数据，否则会报错
    web.switch_to.window(web.window_handles[-1])  # 进入新窗口
    details = web.find_element(By.XPATH, '//div[@class="job-detail"]//div[@class="text"]').text
    print(details)
    print("===========================")
    # 关闭窗口
    web.close()
    # 关闭了新窗口之后，selenium需要手动调整窗口到原来的窗口上
    web.switch_to.window(web.window_handles[0])
    time.sleep(1)
    # break


