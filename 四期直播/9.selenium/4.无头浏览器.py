import time
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select  # 专门用来处理下拉框的

options = ChromeOptions()
options.binary_location = r"D:\SoftWare\Google\Chrome\Application\chrome.exe"
options.add_argument("--headless")  # 无头
options.add_argument("--disable-gpu")  # 禁用GPU
options.add_argument("--window-size=4000,1600")  # 设置窗口大小，防止窗口堆叠，导致找不到相应元素

web = Chrome(options=options)
web.get("https://www.endata.com.cn/BoxOffice/BO/Year/index.html")
# 先拿数据，然后切换年份选项
table = web.find_element(By.ID, "TableList")
print(table.text)
print("==========================")
# 切换选项，以下内容只针对select标签
# 1.找到选择框
select = web.find_element(By.ID, "OptionDate")  # 只是一个普通标签
select = Select(select)

for option in select.options:  # 拿所有的选项
    o = option.text  # 选项
    select.select_by_visible_text(o)  # 通过文字进行选择
    # 等待新数据加载
    time.sleep(2)
    table = web.find_element(By.ID, "TableList")
    print(table.text)
    print("==========================")


