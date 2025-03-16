#自动生成屏保
import requests
import time

def getpng():
    url = "https://v2.xxapi.cn/api/random4kPic?type=wallpaper"

    payload = {}
    headers = {
    'User-Agent': 'xiaoxiaoapi/1.0.0 (https://xxapi.cn)'
    }

    response = requests.request("GET", url, headers = headers, data = payload)
    return response.json()["data"]

url = getpng()
print(url)
filename = time.strftime("%Y%m%d%H%M%S", time.localtime()) + ".jpg"
print(filename)

r = requests.get(url)
with open(filename, "wb") as f:
    f.write(r.content)