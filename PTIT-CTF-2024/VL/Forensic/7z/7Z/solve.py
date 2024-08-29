import base64
with open('data.txt' , 'rb') as file:
	content = file.read().strip()

def decodebase64(data):
	return base64.b64decode(data).decode('utf-8')

def decodebase32(data):
	return base64.b32decode(data).decode('utf-8')

while True:
	content = decodebase64(content)
	content = decodebase32(content)
	if "PTITCTF{" in content:
		break

print(f"Decoded flag: {content}")

