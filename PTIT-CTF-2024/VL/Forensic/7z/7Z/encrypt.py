with open('new_tonton.png', 'rb') as image_file:
	hex_data = image_file.read()
reversed_hex = bytearray(hex_data)
for i in range(0 , len(hex_data) - 1 , 2):
	reversed_hex[i] , reversed_hex[i + 1] = hex_data[i + 1] , hex_data[i]
with open('decrypted_tonton.png','wb') as new_file:
	new_file.write(reversed_hex)