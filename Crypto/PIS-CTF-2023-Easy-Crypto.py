from Crypto.Util.number import *
from pwn import *
import base64
s = 56369025297691660392004556373781623445966955195801799383478576454199136227591253023415024495794577295554691617060609433091389

a = long_to_bytes(s)
print(a)
flag : str = base64.b64decode(a)
print(flag.decode())

## Flag: PISCTF{Th1s_1s_4_m3sS@g3_Fr0m_CrYpt0}