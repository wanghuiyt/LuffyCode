from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains

options = ChromeOptions()
options.binary_location = r"D:\SoftWare\Google\Chrome\Application\chrome.exe"
# 可以去掉显示的那个“Chrome正受到自动测试软件的控制”
options.add_experimental_option("excludeSwitches", ["enable-automation"])
# 取消window.navigator.webdriver
options.add_argument('--disable-blink-features=AutomationControlled')
web = Chrome(options=options)
web.implicitly_wait(10)

web.get("https://kyfw.12306.cn/otn/resources/login.html")
web.find_element(By.ID, "J-userName").send_keys("123456")
web.find_element(By.ID, "J-password").send_keys("123456")
web.find_element(By.ID, "J-login").click()

# 滑块，怎么处理，超级粗糙的处理
btn = web.find_element(By.ID, "nc_1_n1z")
action = ActionChains(web)
action.click_and_hold(on_element=btn)  # 按住
action.move_by_offset(xoffset=300, yoffset=0)  # 拖拽
action.release()  # 松手
action.perform()  # 提交
