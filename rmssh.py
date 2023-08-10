import requests

domain = "sg-do.lizsvr.me"
AUTH_KEY = "lizid"
headers = ({'AUTH_KEY':AUTH_KEY })

url = "http://"+domain+f":6969/deluser?user=lizadm2"

x = requests.get(url, headers=headers, timeout=3)
print(x.status_code)

# try:
#     x = requests.get(url, headers=headers, timeout=3)
#     print("berhasil")
#     print(x.status_code)
# except:
#     print("gagal")