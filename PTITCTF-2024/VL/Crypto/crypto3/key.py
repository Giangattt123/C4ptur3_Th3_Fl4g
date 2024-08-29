from Crypto.Cipher import AES
from Crypto.Util import Counter
import os

# Tạo khóa và giá trị ban đầu cho bộ đếm
KEY = os.urandom(16)
initial_value = 1

def encrypt(m, key, initial_value):
    ctr = Counter.new(128, initial_value=initial_value)
    aes = AES.new(key, AES.MODE_CTR, counter=ctr)
    return aes.encrypt(m).hex()

sample = b'THIS IS A FORM FLAG: PTITCTF{This_is_a_fake_flag}'
encrypted_sample = encrypt(sample, KEY, initial_value)
print("Encrypted sample (hex):", encrypted_sample)

with open('flag.txt', 'r') as f:
    flag = f.read().strip().encode()

encrypted_flag = encrypt(flag, KEY, initial_value)
print("Encrypted flag (hex):", encrypted_flag)


with open('key_and_ctr.bin', 'wb') as kf:
    kf.write(KEY)
    kf.write(initial_value.to_bytes(16, byteorder='big'))
