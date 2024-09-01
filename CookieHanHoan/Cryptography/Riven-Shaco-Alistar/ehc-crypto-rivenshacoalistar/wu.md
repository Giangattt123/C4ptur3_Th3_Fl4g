## Writeup

Tên chall là `Riven-Shaco-Alistar` có thể đang nhắc đến thuật toán mã hóa khóa công khai `RSA`, đề bài cho ta 1 file `python` như sau:

```
from Crypto.Util.number import getPrime, inverse, bytes_to_long
from string import ascii_letters, digits
from random import choice

def generate_random_string(length):
    return "".join(choice(ascii_letters + digits) for _ in range(length))

def encrypt_flag(flag):
    flag = flag.encode()
    key = ###SECRET###

    res = []
    for i in range(len(flag)):
        res.append(flag[i] ^ ord(key[i % len(key)]))

    hex_flag = ''.join(format(c, '02x') for c in res)
    return hex_flag

def get_flag(message):
    print("Question: What did Malphite say?")
    answer = input("Enter your answer: ").strip()

    if answer == malphite:
        print("Nice! You got it right.")
        print("Heres your reward:")
        with open("/flag.txt") as f:
            reward = f.read().strip()
            flag = encrypt_flag(reward)
            print(flag)
    else:
        print("Oops! Thats not the correct answer.")
        print("Maybe next time?")

malphite = generate_random_string(16)
poppy = getPrime(128)
quinn = getPrime(128)
nasus = poppy * quinn
ezreal = 65537

draven = inverse(ezreal, (poppy - 1) * (quinn - 1))

chogath = pow(bytes_to_long(malphite.encode()), ezreal, nasus)

print(f"Chogath: {chogath}")
print(f"Draven: {draven}")

get_flag(malphite)
```

Giải thích chi tiết về từng phần mã:

Đối với các thư viện được `import`

- `getPrime , inverse , bytes_to_long`: Từ thư viện `Crypto.Util.number` để làm việc với số nguyên lớn, bao gồm việc tạo `số nguyên tố`, `tính toán nghịch đảo modulo` và chuyển đổi `chuỗi byte thành số nguyên`.
- `ascii_letters`, `digits`: Từ thư viện `string`, bao gồm các ký tự chữ cái và chữ số.
- `choice`: Từ thư viện `random`, dùng để chọn ngẫu nhiên một phần tử từ một chuỗi hoặc danh sách.

Đối với các hàm có trong đoạn mã:

- Hàm `generate_random_string(length)`: Tạo một chuỗi ngẫu nhiên có độ dài `length` bao gồm các ký tự chữ cái (cả in hoa và in thường) và chữ số.
- Hàm `encrypt_flag(flag)`:
  - Mã hóa chuỗi `flag` bằng cách sử dụng một `khóa bí mật` (chưa được tiết lộ) để XOR từng ký tự của `flag` với từng ký tự của khóa. Kết quả sẽ được chuyển đổi thành dạng `hex`.
  - Chú ý: `Khóa bí mật` **key** trong đoạn mã này chưa được cung cấp (###SECRET###).

Các biến số:

- `malphite`: Chuỗi ngẫu nhiên có độ dài 16 ký tự, tạo bởi hàm `generate_random_string`.
- `poppy` và `quinn`: Hai số nguyên tố ngẫu nhiên có độ dài 128 bit.
- `nasus`: Tích của poppy và quinn.
- `ezreal`: Số mũ công khai trong RSA (65537).
- `draven`: Nghịch đảo modulo của ezreal với (poppy - 1) \* (quinn - 1), đây là khóa bí mật trong RSA.
- `chogath`: Kết quả của phép lũy thừa `malphite^ezreal mod nasus`, đây là thông tin công khai.

Tác giả đã cho `p` và `q` được sinh ngẫu nhiên có độ dài 128 bit, `e` có giá trị 65537 , do `p` và `q` được sinh ngẫu nhiên nên sẽ phải tìm được cặp số `p` , `q` thỏa mãn

Trong thuật toán mã hóa `RSA` ta đã biết

```
d = pow(e , -1 , phi(n)) hay d * e ≡ 1 (mod phi(n))
=> d * e - 1 = r * phi(n) = r * (p - 1) * (q - 1)
```

> Vậy thì (p - 1) \* (q - 1) sẽ là ước của `de - 1` . Với các bộ số `p` và `q` tìm được có thể thử `decrypt` đối với từng cặp. Nếu kết quả nào chỉ bao gồm `chữ cái` và `chữ số` thì đó là kết quả(do hàm `generate_random_string` chỉ `generate` ra `chữ cái` và `chữ số`)

Vấn đề là ở hàm `encrypt_flag` nó cần 1 `key` để có thể giải mã, bởi nếu có ra được bản rõ dựa vào việc sinh ra hai cặp số `p` và `q` thì `flag` cũng sẽ bị mã hóa bởi hàm này.

Việc `bruteforce` **SECRET KEY** có thể sẽ không đem lại kết quả tốt do độ dài của `key` lớn hơn 1 kí tự. Tôi để ý đến `format` của đề là `EHC{}` vậy thì sẽ có cách để lấy được 4 kí tự đầu tiên của **SECRET KEY** bằng toán tử `XOR`

Ở hàm `get_flag` này nếu tìm đúng message thì sẽ nhận lại được chuỗi `flag` đã bị mã hóa bởi hàm `encrypt_flag`

```
def get_flag(message):
    print("Question: What did Malphite say?")
    answer = input("Enter your answer: ").strip()
    if answer == malphite:
        print("Nice! You got it right.")
        print("Heres your reward:")
        with open("/flag.txt") as f:
            reward = f.read().strip()
            flag = encrypt_flag(reward)
            print(flag)
    else:
        print("Oops! Thats not the correct answer.")
        print("Maybe next time?")
```

- Vì vậy tôi sẽ sinh ra hết các cặp ước của `d*e - 1` để tìm ra các bộ số `p,q` thỏa mãn và tính toán để tìm được chuỗi `flag` được cho dưới dạng `hex`, sau đó từ chuỗi `hex` này tôi sẽ tiếp tục đem đi `xor` và tìm được `secret_key`

- Tôi `netcat` đến server và được cho 2 con số `c(bản mã)` và `d(khóa riêng tư)` , tôi viết đoạn code sau để tìm được `message` đúng và nhận lại được `hex_value` từ server

![img1](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/CookieHanHoan/Cryptography/Riven-Shaco-Alistar/ehc-crypto-rivenshacoalistar/player/images/image-01.png?raw=true)

```
from pwn import remote
from Crypto.Util.number import isPrime, long_to_bytes
from string import ascii_letters, digits
from itertools import combinations
from sympy import divisors
from math import log2
chogath = 22446322029400420795314507171254080351453809895135156247116538962768590851447
draven = 28741457797835351483164014455521307444127402736806491158419931700244968153361

ezreal = 65537
divisor = divisors(draven * ezreal - 1)
primes = [x + 1 for x in divisor if isPrime(x + 1)]
size_primes = [x for x in primes if log2(x) // 1 == 127]

message_valid = ascii_letters + digits
print(message_valid)
message = []
for p, q in combinations(size_primes, 2):
    try:
        s = long_to_bytes(pow(chogath, draven, p * q)).decode("ascii")
        if all([c in message_valid for c in s]):
            print(s)
            message.append(s)
    except Exception:
        continue
```

![img2](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/CookieHanHoan/Cryptography/Riven-Shaco-Alistar/ehc-crypto-rivenshacoalistar/player/images/image-02.png?raw=true)

> Message: 2BllPbQqohYpATyI

- Ghi giá trị này vào và nhận được chuỗi `hex` từ server

![img3](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/CookieHanHoan/Cryptography/Riven-Shaco-Alistar/ehc-crypto-rivenshacoalistar/player/images/image-03.png?raw=true)

- Sau đó tôi viết script để tìm được 4 kí tự đầu của flag

```
def find_key(hex_value , s: str):
    cipher_bytes = bytes.fromhex(hex_value)
    key = []
    for i in range(len(s)):
        key.append(cipher_bytes[i] ^ ord(s[i % len(s)]))

    return bytes(key).decode()

hex_value = "111a1635773d360b2b653b183d2461260a2c740f303a0d277b730f323c663922743e36672028"
s = "EHC{"
key = find_key(hex_value , s)
```

> Tôi tìm được 4 kí tự là `TRUN`, tôi nghĩ đến tác giả là `TRUNGPQ` nên đoán `secret_key` là `TRUNGPQ`

Cuối cùng `xor` từng byte của `secret_key` với chuỗi `hex` nhận được ta sẽ tìm được flag

```
def find_key(hex_value , s: str):
    cipher_bytes = bytes.fromhex(hex_value)
    key = []
    for i in range(len(s)):
        key.append(cipher_bytes[i] ^ ord(s[i % len(s)]))

    return bytes(key).decode()

hex_value = "111a1635773d360b2b653b183d2461260a2c740f303a0d277b730f323c663922743e36672028"
s = "EHC{"
key = find_key(hex_value , s)
key_real = key + "GPQ"

def decypt_flag(hex_value , key_real):
    cipher_bytes = bytes.fromhex(hex_value)
    key_bytes = key_real.encode()
    flag = []
    for i in range(len(cipher_bytes)):
        flag.append(cipher_bytes[i] ^ key_bytes[i % len(key_bytes)])
    return bytes(flag).decode(errors='ignore')

flag : str = decypt_flag(hex_value , key_real)
print(flag)
```

> Flag: EHC{0mg_y0u_mu5t_b3_an_r54_ch4ll3ng3r}
