## Solution

<table border="1">
  <tr>
    <th>Challenge</th>
    <th>Difficult</th>
    <th>Flag</th>
  </tr>
  <tr>
    <td>c0rrupt</td>
    <td>Medium</td>
    <td>Data 2</td>
  </tr>
</table>

Tôi kiểm tra file bằng lệnh `file` nhưng nó chỉ hiện đó là file `data`

```
┌──(kali㉿B21DCAT077-Giang-Kali)-[~/…/CTF/PicoCTF/Forensics/c0rrupt]
└─$ file mystery
mystery: data
```

Các câu lệnh cơ bản như `strings , exiftool , binwalk,...` không đem lại được gì

```
┌──(kali㉿B21DCAT077-Giang-Kali)-[~/…/CTF/PicoCTF/Forensics/c0rrupt]
└─$ exiftool mystery
ExifTool Version Number         : 12.76
File Name                       : mystery
Directory                       : .
File Size                       : 203 kB
File Modification Date/Time     : 2024:09:04 22:25:25-04:00
File Access Date/Time           : 2024:09:04 22:25:44-04:00
File Inode Change Date/Time     : 2024:09:04 22:25:33-04:00
File Permissions                : -rw-r--r--
Error                           : Unknown file type

┌──(kali㉿B21DCAT077-Giang-Kali)-[~/…/CTF/PicoCTF/Forensics/c0rrupt]
└─$ binwalk mystery

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
91            0x5B            Zlib compressed data, compressed
```

Tôi kiểm tra phần đầu của tệp để xem định dạng có thể có của file là gì

```
┌──(kali㉿B21DCAT077-Giang-Kali)-[~/…/CTF/PicoCTF/Forensics/c0rrupt]
└─$ xxd mystery|head
00000000: 8965 4e34 0d0a b0aa 0000 000d 4322 4452  .eN4........C"DR
00000010: 0000 066a 0000 0447 0802 0000 007c 8bab  ...j...G.....|..
00000020: 7800 0000 0173 5247 4200 aece 1ce9 0000  x....sRGB.......
00000030: 0004 6741 4d41 0000 b18f 0bfc 6105 0000  ..gAMA......a...
00000040: 0009 7048 5973 aa00 1625 0000 1625 0149  ..pHYs...%...%.I
00000050: 5224 f0aa aaff a5ab 4445 5478 5eec bd3f  R$......DETx^..?
00000060: 8e64 cd71 bd2d 8b20 2080 9041 8302 08d0  .d.q.-.  ..A....
00000070: f9ed 40a0 f36e 407b 9023 8f1e d720 8b3e  ..@..n@{.#... .>
00000080: b7c1 0d70 0374 b503 ae41 6bf8 bea8 fbdc  ...p.t...Ak.....
00000090: 3e7d 2a22 336f de5b 55dd 3d3d f920 9188  >}*"3o.[U.==. ..
```

Ở đây tôi sẽ tách từng byte thành từng cột cho dễ nhìn

```
┌──(kali㉿B21DCAT077-Giang-Kali)-[~/…/CTF/PicoCTF/Forensics/c0rrupt]
└─$ xxd -g 1 mystery | head
00000000: 89 65 4e 34 0d 0a b0 aa 00 00 00 0d 43 22 44 52  .eN4........C"DR
00000010: 00 00 06 6a 00 00 04 47 08 02 00 00 00 7c 8b ab  ...j...G.....|..
00000020: 78 00 00 00 01 73 52 47 42 00 ae ce 1c e9 00 00  x....sRGB.......
00000030: 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61 05 00 00  ..gAMA......a...
00000040: 00 09 70 48 59 73 aa 00 16 25 00 00 16 25 01 49  ..pHYs...%...%.I
00000050: 52 24 f0 aa aa ff a5 ab 44 45 54 78 5e ec bd 3f  R$......DETx^..?
00000060: 8e 64 cd 71 bd 2d 8b 20 20 80 90 41 83 02 08 d0  .d.q.-.  ..A....
00000070: f9 ed 40 a0 f3 6e 40 7b 90 23 8f 1e d7 20 8b 3e  ..@..n@{.#... .>
00000080: b7 c1 0d 70 03 74 b5 03 ae 41 6b f8 be a8 fb dc  ...p.t...Ak.....
00000090: 3e 7d 2a 22 33 6f de 5b 55 dd 3d 3d f9 20 91 88  >}*"3o.[U.==. ..
```

Để ý 8 byte đầu tiên là `89 65 4e 34 0d 0a b0 aa` trông nó khá giống định dạng của file `png` là `89 50 4E 47 0D 0A 1A 0A`, lưu ý phần còn lại của luồng dữ liệu chứa một hình ảnh `PNG` duy nhất, bao gồm một loạt các khối bắt đầu bằng một khối `IHDR` và ​​kết thúc bằng một khối `IEND`.

Tôi sẽ thử sửa đổi 8 byte đầu đó về đúng định dạng sau đó lưu lại

![img01]()

Nhưng đó là chưa đủ, sau 8 byte đầu tiên là `header file signature` thì theo sau nó là một loạt các khối `CHUNK`. Mỗi `CHUNK` chứa 4 byte lần lượt là `Length , Chunk type, Chunk data, CRC`
[Chunk-layout](https://www.w3.org/TR/2003/REC-PNG-20031110/#5Chunk-layout)

Khối đầu tiên được gọi `IHDR`(với hình ảnh `PNG` hợp lệ sẽ chỉ có 1 khối `IHDR` duy nhất) và có độ dài là `0xD`(13 byte), nó bao gồm:

- Width: 4 bytes
- Height: 4 bytes
- Bit depth: 1 byte
- Color type: 1 byte
- Compression method: 1 byte
- Filter method: 1 byte
- Interlace method: 1 byte

Trước tiên để bắt đầu với một khối `IHDR` 8 byte tiếp theo đi sau 8 byte `file header signature` phải là `00 00 00 0D 49 48 44 52`. Trong đó:

- 00 00 00 0D: Độ dài của dữ liệu khối `IHDR`, tức là 13 byte (theo hệ thập lục phân).
- 49 48 44 52: Chuỗi ký tự `"IHDR"` (tên của khối).

![img02]()

Bây giờ check bằng lệnh `file` và nó đã được nhận dạng là một file `PNG` hợp lệ nhưng khi tôi mở tấm ảnh lên thì nó vẫn nhận được thông báo lỗi và không mở được ảnh

![img03]()

Tôi kiểm tra bằng `pngcheck` để xem mình sẽ cần phải chỉnh sửa thêm gì ở `header file`

```
┌──(kali㉿B21DCAT077-Giang-Kali)-[~/…/CTF/PicoCTF/Forensics/c0rrupt]
└─$ pngcheck -v mystery
zlib warning:  different version (expected 1.2.13, using 1.3.1)
File: mystery (202940 bytes)
  chunk IHDR at offset 0x0000c, length 13
    1642 x 1095 image, 24-bit RGB, non-interlaced
  chunk sRGB at offset 0x00025, length 1
    rendering intent = perceptual
  chunk gAMA at offset 0x00032, length 4: 0.45455
  chunk pHYs at offset 0x00042, length 9: 2852132389x5669 pixels/meter
  CRC error in chunk pHYs (computed 38d82c82, expected 495224f0)
ERRORS DETECTED in mystery
```

- **File information:**

  - `Chunk IHDR`: Đây là chunk đầu tiên trong tệp `PNG`, chứa các thông tin cơ bản về hình ảnh.

  - `Kích thước ảnh`: 1642 x 1095
  - `Định dạng`: 24-bit RGB, không interlaced.
  - `Chunk sRGB`: Chứa thông tin về intent rendering của hình ảnh (trong trường hợp này là perceptual, một trong những phương thức điều chỉnh màu sắc dựa trên cảm nhận của người xem).

  - `Chunk gAMA`: Chứa gamma value, giá trị ở đây là 0.45455.

  - Chunk `pHYs`: Cung cấp thông tin về độ phân giải pixel trong đơn vị pixel/mét. Tuy nhiên, ở đây, chunk này có lỗi về `CRC`.

- **CRC Error:**

  - `Chunk pHYs` có một lỗi về `CRC`. `CRC (Cyclic Redundancy Check)` được dùng để kiểm tra tính toàn vẹn của dữ liệu trong các chunk. Trong trường hợp này, giá trị CRC được tính toán là `38d82c82`, nhưng giá trị mong đợi là `495224f0`. Điều này có nghĩa là chunk pHYs đã bị thay đổi hoặc bị lỗi trong quá trình lưu trữ hoặc truyền tải tệp tin.

> Để fix lỗi này , trong `chunk pHYs` chúng ta chỉ cần thay thế giá trị `CRC` (tính toán) bằng giá trị mong đợi. Mục đích của phần `CRC` là kiểm tra dữ liệu bị hỏng.

Tôi tìm kiếm thông tin về `chunk pHYs`

![img04]()

Vì các pixel trên mỗi đơn vị chỉ khác nhau một byte và `0xaa` sẽ tương ứng với trục X, giá trị sẽ rất lớn, nên việc đặt số 0 thay thế là hợp lý. Điều này sẽ sửa lỗi `CRC`.

![img05]()

Tôi sẽ kiểm tra lại nhưng lần này nó bị lỗi `invalid chunk length (too large)`

```
┌──(kali㉿B21DCAT077-Giang-Kali)-[~/…/CTF/PicoCTF/Forensics/c0rrupt]
└─$ pngcheck -v mystery
zlib warning:  different version (expected 1.2.13, using 1.3.1)

File: mystery (202940 bytes)
  chunk IHDR at offset 0x0000c, length 13
    1642 x 1095 image, 24-bit RGB, non-interlaced
  chunk sRGB at offset 0x00025, length 1
    rendering intent = perceptual
  chunk gAMA at offset 0x00032, length 4: 0.45455
  chunk pHYs at offset 0x00042, length 9: 5669x5669 pixels/meter (144 dpi)
:  invalid chunk length (too large)
ERRORS DETECTED in mystery
```

Lần này nó không chỉ rõ khối nào là nguyên nhân sinh ra lỗi, vì vậy chúng ta phải bắt đầu kiểm tra từng khối(`Length , Type , Data , CRC`)

Theo sau khối `pHys` có khối có tên là `DET` có vẻ nó không tồn tại -> sửa thành `IDAT`(`49 44 41 54`)

![img06]()

Bây giờ cần giải quyết độ dài khối `IDAT` quá lớn nó đang có kích thước là `0xaaaaf5` , mình thử sửa `aaaa` thành `0000` và sau đó `check` lại

![ing07]()

```
┌──(kali㉿B21DCAT077-Giang-Kali)-[~/…/CTF/PicoCTF/Forensics/c0rrupt]
└─$ pngcheck -v mystery
zlib warning:  different version (expected 1.2.13, using 1.3.1)

File: mystery (202940 bytes)
  chunk IHDR at offset 0x0000c, length 13
    1642 x 1095 image, 24-bit RGB, non-interlaced
  chunk sRGB at offset 0x00025, length 1
    rendering intent = perceptual
  chunk gAMA at offset 0x00032, length 4: 0.45455
  chunk pHYs at offset 0x00042, length 9: 5669x5669 pixels/meter (144 dpi)
  chunk IDAT at offset 0x00057, length 65445
    zlib: deflated, 32K window, fast compression
  chunk IDAT at offset 0x10008, length 65524
  chunk IDAT at offset 0x20008, length 65524
  chunk IDAT at offset 0x30008, length 6304
  chunk IEND at offset 0x318b4, length 0
No errors detected in mystery (9 chunks, 96.3% compression).
```

Bây giờ có thể xem được hình ảnh và flag hiện ngay trên ảnh

![flag]()

> Flag: picoCTF{c0rrupt10n_1847995}
