## Writeup

- Đề bài cho 1 file 7Z.rar nhưng không cung cấp password
  => `crack password`

- Sử dụng `rar2john` để lấy mã hash file

![img7](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PTIT-CTF-2024/VL/images/image-7.png?raw=true)

- Tiếp theo sử dụng `john` đi kèm với một `wordlist` để crack password

![img8](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PTIT-CTF-2024/VL/images/image-8.png?raw=true)

`Password: 123456789d`

- Sau khi crack được password, ta có thể giải nén file 7Z.rar, trong đó chứa 1 bức ảnh nhưng không mở được

![img9](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PTIT-CTF-2024/VL/images/image-9.png?raw=true)

- Tôi kiểm tra bằng `pngcheck` thì biết đây không phải file `PNG` hợp lệ

```
┌──(kali㉿B21DCAT077-Giang-Kali)-[~/…/VL/Forensic/7z/7Z]
└─$ pngcheck new_tonton.png
zlib warning:  different version (expected 1.2.13, using 1.3.1)

new_tonton.png  this is neither a PNG or JNG image nor a MNG stream
ERROR: new_tonton.png
```

- Tiến hành kiểm tra mã `hex` của file ảnh `hexeditor new_tonton.png`

![img10](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PTIT-CTF-2024/VL/images/image-10.png?raw=true)

> `Signature` của ảnh `P.GN` và `CHUNK HEADER` `IHDR` bị đổi thành `HIRD`. Vậy thuật toán encrypt file ảnh có thể là sẽ đổi chỗ các vị trí với nhau, vị trí lẻ sang vị trí chẵn và vị trí chẵn sang vị trí lẻ. Tôi viết script để `decrypt` file ảnh này.

```
with open('new_tonton.png', 'rb') as image_file:
	hex_data = image_file.read()
reversed_hex = bytearray(hex_data)
for i in range(0 , len(hex_data) - 1 , 2):
	reversed_hex[i] , reversed_hex[i + 1] = hex_data[i + 1] , hex_data[i]
with open('decrypted_tonton.png','wb') as new_file:
	new_file.write(reversed_hex)
```

- Sau khi chạy script, file ảnh được giải mã thành một bức ảnh bình thường và có thể xem được

![img11](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PTIT-CTF-2024/VL/images/image-11.png?raw=true)

- Bức ảnh chỉ dẫn ta đến 1 đường link github chứa một lượng lớn dữ liệu có thể bị mã hóa

![img](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PTIT-CTF-2024/VL/images/image-12.png?raw=true)

- Tôi thử decode nó với `base64` rồi tiếp tục decode `base64` thì nhận được lỗi do nó là mã `base32`, tôi decode với `base32` lại nhận được đoạn `base64`...

  > Từ đây thuật toán mã hóa là base64 - base32 - base64 - base32 - ....

- Script decrypt

```
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
```

- Sau khi chạy script, ta nhận được flag:

```
┌──(kali㉿B21DCAT077-Giang-Kali)-[~/…/VL/Forensic/7z/7Z]
└─$ python3 solve.py
Decoded flag: PTITCTF{T0n_T0n_1s_My_Fr13nd!@#txc!@#}
```
