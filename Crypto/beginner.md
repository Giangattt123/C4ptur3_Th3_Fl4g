### 1. chr và ord

chr(): Hàm này nhận vào một giá trị số nguyên (ASCII code) và trả về ký tự tương ứng

ord(): Hàm này nhận vào một ký tự và trả về giá trị ASCII tương ứng (hoặc Unicode code point cho các ký tự ngoài ASCII).

```
import sys
flag = [99, 114, 121, 112, 116, 111, 123, 65, 83, 67, 73, 73, 95, 112, 114, 49, 110, 116, 52, 98, 108, 51, 125]

print("".join(chr(i) for i in flag))
```

```
Flag: crypto{ASCII_pr1nt4bl3}
```

### 2. hex

Khi chúng ta mã hóa một cái gì đó, mã hóa chúng ta nhận được sẽ không phải là các ký tự ASCII có thể in ra được. Vì vậy, nếu chúng ta muốn chia sẻ dữ liệu được mã hóa của mình, chúng ta sẽ mã hóa dữ liệu đó thành những thứ thân thiện với người dùng ví dụ như chuỗi hex

`byte.fromhex()`: chuyển đổi các kí tự `hex` sang `ASCII` có thể in được
` bytes.hex()`: chuyển đổi các kí tự sang định dạng `hex`

```

hexxa = "63727970746f7b596f755f77696c6c5f62655f776f726b696e675f776974685f6865785f737472696e67735f615f6c6f747d"
x = bytes.fromhex(hexxa)
print(x)
x = bytes.hex(x)
print(x)
```

```
b'crypto{You_will_be_working_with_hex_strings_a_lot}'
63727970746f7b596f755f77696c6c5f62655f776f726b696e675f776974685f6865785f737472696e67735f615f6c6f747d
```

### 3. base64

Một mã hóa phổ biến khác là `base64`, cho phép dữ liệu nhị phân được biểu diễn dưới dạng chuỗi ASCII sử dụng 64 ký tự. Một ký tự của chuỗi `base64` mã hóa 6 bit, và do đó 4 ký tự của Base64 mã hóa ba byte 8 bit.

Trong Python có thư viện hỗ trợ cho base64 là `import base64` trong đó chúng ta sử dụng `base64.b64encode()` là hàm để mã hóa một chuỗi `byte` thành `base64` và ngược lại, chúng ta cũng có `base64.b64decode()` hàm để chuyển đổi từ `base64` trở lại `byte`

```import base64
x = "72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf"
x = bytes.fromhex(x)
print(x)
x = base64.b64encode(x)
print(x)
x = base64.b64decode(x)
print(x)
```

```
b'r\xbc\xa9\xb6\x8f\xc1j\xc7\xbe\xeb\x8f\x84\x9d\xca\x1d\x8ax>\x8a\xcf\x96y\xbf\x92i\xf7\xbf'
b'crypto/Base+64+Encoding+is+Web+Safe/'
b'r\xbc\xa9\xb6\x8f\xc1j\xc7\xbe\xeb\x8f\x84\x9d\xca\x1d\x8ax>\x8a\xcf\x96y\xbf\x92i\xf7\xbf'
```

### 4. pycryptdome

Pycryptodome là một thư viện mã hóa mã nguồn mở cho Python, để tải xuống dùng câu lệnh `pip3 install pycryptodome`

Để sử dụng các chức năng trong thư viện, hãy nhập thư viện bằng dòng lệnh `from Crypto.Util.number import *`

Các hàm thường dùng là `bytes_to_long() , long_to_bytes() , getPrime() , inverse()` , ...

- Ví dụ

  ```
  from Crypto.Util.number import *
  x = 11515195063862318899931685488813747395775516287289682636499965282714637259206269
  x = long_to_bytes(x)
  print(x)
  ## b'crypto{3nc0d1n6_4ll_7h3_w4y_d0wn}
  ```

### 5. xor

```
x = "label"
string = [ord(o) for o in x]
print(string)
print("".join((chr(13 ^ o) for o in string)))
"""
[108, 97, 98, 101, 108]
aloha
crypto{aloha}
"""
```

**XOR PROPERTIES:**

```
Commutative: A ⊕ B = B ⊕ A
Associative: A ⊕ (B ⊕ C) = (A ⊕ B) ⊕ C
Identity: A ⊕ 0 = A
Self-Inverse: A ⊕ A = 0
```

- Ví dụ 1:

```
KEY1 = a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313
KEY2 ^ KEY1 = 37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e
KEY2 ^ KEY3 = c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1
FLAG ^ KEY1 ^ KEY3 ^ KEY2 = 04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf
```

- `Solve:`

  - Ở đây tôi dùng hàm `xor(xor 2 chuỗi byte)` trong thư viện `pwntools`

  ```
  from Crypto.Util.number import *
  from pwn import *

  key1 = "a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313"
  key1_2 = "37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e"
  key2_3 = "c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1"
  key1_2_3 = "04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf"

  key2 = xor(bytes.fromhex(key1) , xor(bytes.fromhex(key1_2)))
  key3 = xor(bytes.fromhex(key2_3) , key2)
  key123 = xor(bytes.fromhex(key2_3),bytes.fromhex(key1))
  flag = xor(bytes.fromhex(key1_2_3) , key123)
  print(flag.decode())
  ```

- Ví dụ 2:

```
I've hidden some data using XOR with a single byte, but that byte is a secret. Don't forget to decode from hex first.
73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d
```

- `Solve:`

  ```
    str = "73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d"
    str = bytes.fromhex(str)
    print(str)
    for i in range(len(str)):
        print("".join(chr(i ^ o) for o in str))
  ```

  - `Output:`

    ```
    b"sbi`d\x7fk h! O!%O}iOv$f eb!'#Ori'um"
    sbi`d⌂k h! O!%O}iOv$f eb!'#Ori'um

    rchae~j!i !N $N|hNw%g!dc &"Nsh&tl

    q`kbf}i"j#"M#'M⌂kMt&d"g`#%!Mpk%wo

    pajcg|h#k"#L"&L~jLu'e#fa"$ Lqj$vn

    wfmd`{o$l%$K%!KymKr b$af%#'Kvm#qi

    vgleazn%m$%J$ JxlJs!c%`g$"&Jwl"ph

    udofbym&n'&I'#I{oIp"`&cd'!%Ito!sk

    tengcxl'o&'H&"HznHq#a'be& $Hun rj

    {jahlwc(`)(G)-GuaG~,n(mj)/+Gza/}e

    zk`imvb)a()F(,Ft`F⌂-o)lk(.*F{`.|d

    yhcjnua*b+*E+/EwcE|.l*oh+-)Exc-⌂g

    xibkot`+c*+D*.DvbD}/m+ni*,(Dyb,~f

    ⌂nelhsg,d-,C-)CqeCz(j,in-+/C~e+ya

    ~odmirf-e,-B,(BpdB{)k-ho,*.B⌂d*x`

    }lgnjqe.f/.A/+AsgAx*h.kl/)-A|g){c

    |mfokpd/g./@.*@rf@y+i/jm.(,@}f(zb

    crypto{0x10_15_my_f4v0ur173_by7e}

    bsxqunz1y01^04^lx^g5w1ts062^cx6d|

    ap{rvmy2z32]37]o{]d6t2wp351]`{5g⌂

    `qzswlx3{23\26\nz\e7u3vq240\az4f~

    gv}tpk⌂4|54[51[i}[b0r4qv537[f}3ay

    fw|uqj~5}45Z40Zh|Zc1s5pw426Zg|2`x

    et⌂vri}6~76Y73Yk⌂Y`2p6st715Yd⌂1c{

    du~wsh|7⌂67X62Xj~Xa3q7ru604Xe~0bz

    kzqx|gs8p98W9=WeqWn<~8}z9?;Wjq?mu

    j{py}fr9q89V8<VdpVo=⌂9|{8>:Vkp>lt

    ixsz~eq:r;:U;?UgsUl>|:⌂x;=9Uhs=ow

    hyr{⌂dp;s:;T:>TfrTm?};~y:<8Tir<nv

    o~u|xcw<t=<S=9SauSj8z<y~=;?Snu;iq

    n⌂t}ybv=u<=R<8R`tRk9{=x⌂<:>Rot:hp

    m|w~zau>v?>Q?;QcwQh:x>{|?9=Qlw9ks

    l}v⌂{`t?w>?P>:PbvPi;y?z}>8<Pmv8jr

    SBI@D_KH☺o☺♣o]IoV♦FEB☺♥oRIUM

    ```

    > Flag: crypto{0x10_15_my_f4v0ur173_by7e}

### 6. pwntool

- `pwntools` là một thư viện Python mạnh mẽ, được thiết kế để hỗ trợ các hacker và nhà nghiên cứu bảo mật trong các bài thi Capture The Flag (CTF) và khai thác lỗ hổng phần mềm. Thư viện này cung cấp các công cụ và hàm tiện ích để tương tác với các chương trình, thực hiện các phép toán liên quan đến mã hóa, khai thác (exploit), và phân tích các giao thức mạng.

- Tải xuống `pwntool`

```
sudo apt-get update
sudo apt-get install python3 python3-pip python3-dev git libssl-dev libffi-dev build-essential
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade pwntools
```

- `Example:`

```
from pwn import *
context(arch = 'i386', os = 'linux')

r = remote('exploitme.example.com', 31337)
# EXPLOIT CODE GOES HERE
r.send(asm(shellcraft.sh()))
r.interactive()
```

**Một số tính năng nổi bật của pwntools**
