import Crypto
import base64
from Crypto.Util.number import long_to_bytes , getPrime, inverse, bytes_to_long
encrypt = bytes.fromhex("6c464b4d514b744817491714487449174b57")
from pwn import xor 
for i in range(256):
	flag = xor(i , encrypt)
	if b"Flag" in flag:
		print(flag)
