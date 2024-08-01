message : str = "q{vpln'bH_varHuebcrqxetrHOXEj"
## tool: https://www.dcode.fr/xor-cipher
flag = "flag{y0u_Have_bruteforce_XOR}" ## key: 23
def xor_decrypt(text, key):
    return ''.join(chr(ord(char) ^ key) for char in text)

for key in range(256):
    print(f"Key {key}: {xor_decrypt(message, key)}")
