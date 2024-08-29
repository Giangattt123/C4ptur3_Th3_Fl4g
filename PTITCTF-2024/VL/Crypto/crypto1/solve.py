rom Crypto.Cipher import DES
import base64

def decrypt(ciphertext, key):
    cipher = DES.new(key, DES.MODE_ECB)
    decrypted_text = cipher.decrypt(ciphertext)
    return decrypted_text

cipher_b64 = "Xfw54DbCB6IXKg/a1tdlG40kvNy/0z6CYtdmEvrC+2A="
cipher = base64.b64decode(cipher_b64)

key = b'PTITCTF{'
decrypted_text = decrypt(cipher, key)

print("Decrypted text:", decrypted_text.decode())