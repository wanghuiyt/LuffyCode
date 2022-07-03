from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from chaojiying_Python.chaojiying import Chaojiying_Client

options = ChromeOptions()
options.binary_location = r"D:\SoftWare\Google\Chrome\Application\chrome.exe"
web = Chrome(options=options)
web.get("https://www.chaojiying.com/user/login/")
web.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div[1]/form/p[1]/input').send_keys("18614075987")
web.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div[1]/form/p[2]/input').send_keys("q6035945")
img = web.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div[1]/form/div/img')
# screenshot 截屏
bs = img.screenshot_as_png  # 返回的是字节
# 交给超级鹰来进行识别
chaojiying = Chaojiying_Client("18614075987", "q6035945", "935925")
dic = chaojiying.PostPic(bs, 1004)  # 把图片的字节传递进去即可
code = dic["pic_str"]
web.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div[1]/form/p[3]/input').send_keys(code)
web.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div[1]/form/p[4]/input').click()
