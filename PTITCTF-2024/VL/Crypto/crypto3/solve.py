from Crypto.Cipher import AES
from Crypto.Util import Counter

# Đọc `KEY` và giá trị `initial_value` từ file
with open('key_and_ctr.bin', 'rb') as kf:
    key = kf.read(16)
    initial_value = int.from_bytes(kf.read(16), byteorder='big')

# Tạo lại bộ đếm với giá trị ban đầu
ctr = Counter.new(128, initial_value=initial_value)

def decrypt(encrypted_hex, key, counter):
    aes = AES.new(key, AES.MODE_CTR, counter=counter)
    encrypted_bytes = bytes.fromhex(encrypted_hex)
    return aes.decrypt(encrypted_bytes)

# Dữ liệu mã hóa cần giải mã
encrypted_sample = "c12aa4660117f8efb687fd0a87f988786b34cee343be98f767015783ca7cb675e24ec91f631f6d397b565e985ef56196a1"
encrypted_flag = "c536a461620aedb4b9c8cc1a8cdbdd616c1be6ae3caf89ed6c116c9af452a3"

# Giải mã dữ liệu
decrypted_sample = decrypt(encrypted_sample, key, ctr)
decrypted_flag = decrypt(encrypted_flag, key, ctr)

print("Decrypted sample:", decrypted_sample.decode())
print("Decrypted flag:", decrypted_flag.decode())
