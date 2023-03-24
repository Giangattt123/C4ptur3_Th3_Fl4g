# Solution

Với thử thách này tôi đã dùng hết các cách và tool dùng đến trong các bài trước nhưng đều không thu được kết quả. Hmm,.. các bạn có thể thử nếu muốn. Sau một hồi đọc đề bài và search **google** mình đã biết có thể file dũ liệu thực sự có ích để tìm ra flag đã bị **tác giả** ẩn vào file **great-scott.jpg** . Ở đây ta sẽ sử dụng tool **steghide** .Nó không tích hợp sẵn trong kali vì vậy ta có thể tải xuống bằng câu lệnh

```
    sudo apt install steghide
```

Để hiển thị thông tin file ảnh sử dụng **steghide** kết hợp với tham số **info**, nếu bạn không biết có thể xem bằng cách dùng câu lệnh

```
    steghide --help
```

> steghide infor great-scott.jpg

```
    ┌──(kali㉿kali)-[~/Downloads]
    └─$ steghide info great-scott.jpg
    "great-scott.jpg":
    format: jpeg
    capacity: 32.0 KB
    Try to get information about embedded data ? (y/n) y
    Enter passphrase:
    embedded file "steganopayload615282.txt":
        size: 30.0 Byte
        encrypted: rijndael-128, cbc
        compressed: yes
```

Nhìn vào thông tin thu thập được ta có thể thấy nội dung gốc được nhúng trong **steganopayload615282.txt** và đang bị nén bởi **"compressed: yes"**. Bây giờ tiến hành **extract** và đọc nội dung file bình thường thôi:))

![image1](https://live.staticflickr.com/65535/52768369126_cc1eeca150_z.jpg)

> Flag: **"nicc{It's_All_About_the_Mets!}"**
