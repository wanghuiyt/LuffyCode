import time
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome, ChromeOptions

options = ChromeOptions()
options.binary_location = r"D:\SoftWare\Google\Chrome\Application\chrome.exe"
web = Chrome(options=options)
web.implicitly_wait(10)
web.maximize_window()

url = "https://www.17k.com/"
web.get(url)
web.find_element(By.XPATH, '//*[@id="header_login_user"]/a[1]').click()
# 切换iframe
iframe = web.find_element(By.XPATH, '/html/body/div[20]/div/div[1]/iframe')
web.switch_to.frame(iframe)
web.find_element(By.XPATH, '/html/body/form/dl/dd[2]/input').send_keys("16538989670")
web.find_element(By.XPATH, '/html/body/form/dl/dd[3]/input').send_keys("q6035945")
# 勾选协议
web.find_element(By.XPATH, '//*[@id="protocol"]').click()
web.find_element(By.XPATH, '/html/body/form/dl/dd[5]/input').click()

# 登录成功之后，睡眠一下
time.sleep(1)
# 记录cookie
cookies = web.get_cookies()  # 加载的cookie是浏览器上的cookie，所以包括了服务器返回的cookie和js执行加载的cookie
# print(cookies)

# 假设cookie准备给requests使用得话
cookie = {}
for item in cookies:
    cookie[item["name"]] = item["value"]

# 后面得requests就可以直接使用cookie了
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

resp = requests.get("https://user.17k.com/ck/author/shelf?page=1&appKey=2406394919", headers=headers, cookies=cookie)
print(resp.text)
