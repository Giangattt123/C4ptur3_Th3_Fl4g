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