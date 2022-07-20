import time
import json
import base64
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains


def base64_api(uname, pwd, img, typeid):
    with open(img, "rb") as f:
        base64_data = base64.b64encode(f.read())
        b64 = base64_data.decode()
    data = {"username": uname, "password": pwd, "typeid": typeid, "image": b64}
    result = json.loads(requests.post("http://api.ttshitu.com/predict", json=data).text)
    if result["success"]:
        return result["data"]["result"]
    else:
        return result["message"]

options = ChromeOptions()
options.binary_location = r"D:\SoftWare\Google\Chrome\Application\chrome.exe"
web = Chrome(options=options)
web.implicitly_wait(10)
# web.maximize_window()
web.get("https://www.bilibili.com/")
web.find_element(By.XPATH, '//*[@class="header-login-entry"]/span').click()
web.find_element(By.XPATH, '//*[@class="bili-mini-account"]/input').send_keys("1738407610@qq.com")
web.find_element(By.XPATH, '//*[@class="bili-mini-password"]//input').send_keys("ccm1234ldl")
time.sleep(2)  # 这里只能硬等待
web.find_element(By.XPATH, '//*[@class="universal-btn login-btn"]').click()

tu = web.find_element(By.XPATH, '//*[@class="geetest_widget geetest_medium_fontsize"]')
tu.screenshot("tu.png")  # 把图片存在文件中
# tu.screenshot_as_png()  # 直接拿到字节
result = base64_api("q6035945", "q6035945", "tu.png", 27)
print(result)  # 157,150|43,189

rs = result.split("|")
for r in rs:
    x, y = r.split(",")
    # 转化成数字
    print(x, y)
    # 找截图的那个位置的左上角，横向移动xxx，纵向移动xxx，点击
    # 事件链，动作链，一系列动作，需要perform提交
    ActionChains(web).move_to_element_with_offset(to_element=tu, xoffset=x, yoffset=y).click(on_element=tu).perform()
    time.sleep(1)
time.sleep(1)
web.find_element(By.XPATH, '//*[@class="geetest_commit_tip"]').click()
















