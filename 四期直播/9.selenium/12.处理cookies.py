import requests

lst = [{'domain': '.17k.com', 'httpOnly': False, 'name': 'Hm_lpvt_9793f42b498361373512340937deb2a0', 'path': '/', 'secure': False, 'value': '1658565206'}, {'domain': '.17k.com', 'expiry': 1674117205, 'httpOnly': False, 'name': 'accessToken', 'path': '/', 'secure': False, 'value': 'avatarUrl%3Dhttps%253A%252F%252Fcdn.static.17k.com%252Fuser%252Favatar%252F19%252F99%252F14%252F95041499.jpg-88x88%253Fv%253D1648893235000%26id%3D95041499%26nickname%3D%25E5%2598%25BB%25E5%2598%25BB%25E5%2598%25BB%25E7%259A%2584%25E6%259D%25B0%25E4%25BC%25A6%26e%3D1674117206%26s%3De737daba069ca9e3'}, {'domain': '.17k.com', 'expiry': 1674117205, 'httpOnly': False, 'name': 'c_csc', 'path': '/', 'secure': False, 'value': 'web'}, {'domain': '.17k.com', 'expiry': 1658591999, 'httpOnly': False, 'name': 'sajssdk_2015_cross_new_user', 'path': '/', 'secure': False, 'value': '1'}, {'domain': '.17k.com', 'expiry': 1690101206, 'httpOnly': False, 'name': 'Hm_lvt_9793f42b498361373512340937deb2a0', 'path': '/', 'secure': False, 'value': '1658565204'}, {'domain': '.17k.com', 'expiry': 1674117205, 'httpOnly': False, 'name': 'c_channel', 'path': '/', 'secure': False, 'value': '0'}, {'domain': '.17k.com', 'expiry': 7965765206, 'httpOnly': False, 'name': 'sensorsdata2015jssdkcross', 'path': '/', 'secure': False, 'value': '%7B%22distinct_id%22%3A%2295041499%22%2C%22%24device_id%22%3A%221822a309887ad1-04b2f55106da4d-673b5753-3110400-1822a309888cdc%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22a495f0a7-66f5-4a1e-ba98-464b5e2b993a%22%7D'}, {'domain': '.17k.com', 'expiry': 1690101201, 'httpOnly': False, 'name': 'GUID', 'path': '/', 'secure': False, 'value': 'a495f0a7-66f5-4a1e-ba98-464b5e2b993a'}]

result = {}
for item in lst:
    # print(item)
    # print(f"{item['name']}={item['value']};")
    result[item["name"]] = item["value"]
# print(result)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

resp = requests.get("https://user.17k.com/ck/author/shelf?page=1&appKey=2406394919", headers=headers, cookies=result)
print(resp.text)
