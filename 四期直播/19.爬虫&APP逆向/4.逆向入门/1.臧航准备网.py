import requests

resp = requests.post(
    url="http://cd.tibetairlines.com.cn:9100/login",
    headers={
        "User-Agent": "android_system_webview"
    },
    data={
        'grant_type':	'password',
        'isLogin':	'true',
        'password':	'123123',
        'username':	'alex,F'
    }
)

print(resp.text)

