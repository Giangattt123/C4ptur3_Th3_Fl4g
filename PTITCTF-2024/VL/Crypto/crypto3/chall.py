from Crypto.Cipher import AES
from Crypto.Util import Counter
import os

KEY = os.urandom(16)

def encrypt(m):
    ctr = Counter.new(128)
    aes = AES.new(KEY, AES.MODE_CTR, counter=ctr)
    return aes.encrypt(m).hex()

sample = b'THIS IS A FORM FLAG: PTITCTF{This_is_a_fake_flag}'
print(encrypt(sample))

with open('flag.txt', 'r') as f:
    flag = f.read().strip().encode()  
print(encrypt(flag))

