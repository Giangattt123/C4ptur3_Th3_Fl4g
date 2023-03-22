# Solution

Đầu tiên ta mở file **log.txt** đây chính là file data ta cần sử dụng để tìm flag. Dòng đầu tiên của file trông giống như là Base64(**Đây là một tính năng của mã hóa Base64. Base64 được sử dụng để mã hóa dữ liệu nhị phân thành các ký tự ASCII, trong đó mỗi ký tự được biểu diễn bởi 6 bit. Tuy nhiên, độ dài của dữ liệu có thể không phải lúc nào cũng chia hết cho 6, do đó Base64 sẽ thêm các ký tự đệm để đảm bảo độ dài của dữ liệu đủ để chia hết cho 6.Và trong base64, các kí tự đệm thường biểu diễn bằng hai dấu bằng(==)**).
Tiến hành giải mã dòng đầu tiên ta được đoạn text như trong hình dưới đây:

![decode_base64](https://live.staticflickr.com/65535/52764430364_c14cbc38a9_h.jpg)

Ta thấy đoạn giải mã có nói đến **time** chính là key. Có lẽ nó chính là để giải mã dòng text thứ 2 trong file log.txt, với key cho trước rất quen thuộc nó lại là mã hóa **Vigenere-Cipher**, tiếp tục dùng **tool** để giải quyết

![Vigenere_Cipher](https://live.staticflickr.com/65535/52764189866_827bca60bb_b.jpg)

> Đoạn text ta thu được là **"the_secret_is_SAFE"**. Uh,hmmm... từ SAFE được in hoa hết với phần còn lại có thể nó sẽ là một gợi ý.

Dòng thứ 3 trong file log.txt, đoạn text khá khó hiểu, hmm tôi cũng thử với **Vigenere-Cipher** với key là time và ra được đoạn text như bên dưới:

![iamge](https://live.staticflickr.com/65535/52764451209_bcddacd91d_z.jpg)

Hmm tạm thời tôi chưa biết xử lí sao với đoạn text này, tôi chợt nhớ ra mình còn một file **encrypt.py** đề bài cung cấp mà chưa sử dụng đến.

```
    def encrypt(message, key):
        encrypted = ""
        for i in range(len(message)):
            encrypted += chr(ord(message[i]) ^ ord(key[i % len(key)]))
        return encrypted.encode("utf-8").hex()

    message = #//////ERROR ERROR ERROR
    key = #/////// ERROR OERROR ERROR ERROR
    encrypted = encrypt(message,key)
```

Sau khi đọc đoạn code ta có thể hiểu đoạn code trên mã hóa một dòng message với một key. Ở đây key theo tôi là **SAFE** được in hoa hết ở trên. Với key có được, vòng lặp for được sử dụng để lặp lại các ký tự trong tin nhắn và sử dụng phép XOR để mã hóa các ký tự đó với các ký tự tương ứng trong khóa. Để đảm bảo rằng khóa được sử dụng đủ lâu để mã hóa toàn bộ tin nhắn, phép chia lấy dư được sử dụng để lặp lại các ký tự trong khóa khi cần thiết. Sau khi mã hóa, chuỗi kết quả sẽ được chuyển đổi sang mã hex bằng cách sử dụng phương thức **encode("utf-8").hex()**. Việc này cho phép lưu trữ kết quả mã hóa dưới dạng chuỗi hex để dễ dàng truyền tải hoặc lưu trữ mà không bị mất thông tin.

> Với những gì ở trên code đó là cách thức mã hóa và có thể như sau khi mã hóa ta sẽ thu được đoạn text chính là chuỗi hex ở cuối file log.txt. Vì vậy ở đây ta cần phải tìm được **plain-text** dựa trên **cipher-text** là 3 dòng cuối file log.txt

Để dịch ngược trở lại ta cần biết một công thức quan trọng trong phép **xor**

```
a = b ^ c => a ^ b = c
```

> Vì vậy ý tưởng ở đây là chuyển bản cipher về hex() rồi tiến hành xor với SAFE ở dạng UTF-8. Ở đây ta sẽ dùng tool [cybercheft](https://gchq.github.io/CyberChef/) để giúp ta làm điều này.

![FLAG](https://live.staticflickr.com/65535/52764746813_583a0000a8_c.jpg)

> Flag: **nicc{h3lp_m3_0b1_w@n}**
