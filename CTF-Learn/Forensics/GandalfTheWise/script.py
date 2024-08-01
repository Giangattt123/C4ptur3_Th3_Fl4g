import base64

# Chuỗi base64
str1 = "xD6kfO2UrE5SnLQ6WgESK4kvD/Y/rDJPXNU45k/p"
str2 = "h2riEIj13iAp29VUPmB+TadtZppdw3AuO7JRiDyU"

# Giải mã base64 thành byte
bytes1 = base64.b64decode(str1)
bytes2 = base64.b64decode(str2)

if len(bytes1) != len(bytes2):
    raise ValueError("The two byte sequences must be of the same length.")

# XOR hai chuỗi byte
xor_result = bytes([b1 ^ b2 for b1, b2 in zip(bytes1, bytes2)])

# In kết quả dưới dạng chuỗi byte hoặc mã hóa base64
print(xor_result)

# Hoặc để mã hóa lại thành base64
print(base64.b64encode(xor_result).decode())
