import os
from Crypto.Util.number import bytes_to_long, getPrime
from random import getrandbits
from sympy import nextprime


flag = b"flag{???????????????????}"+os.urandom(50)
flag = bytes_to_long(flag)
e = 0x10001
p = getPrime(1024)
secret_num = int(bin(p)[len(bin(p))//2:][::-1], 2)

q = nextprime(p+secret_num)
n = p*q
ct = pow(flag,e,n)

print(f"{n = }")
print(f"{ct = }")

