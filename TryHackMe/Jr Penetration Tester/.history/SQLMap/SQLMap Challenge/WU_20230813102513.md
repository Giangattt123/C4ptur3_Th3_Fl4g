# Solution

Thử thách được cho bởi như sau

![image1](https://live.staticflickr.com/65535/53111650072_3f0412156d_z.jpg)

Truy cập đến địa chỉ 10.10.31.188 ta thấy một trang web như sau:

![image2](https://live.staticflickr.com/65535/53112272996_7d02d65349_c.jpg)

Bước đầu tiên khi làm việc với một **target** trước hết ta phải tiến hành recon. Ở đây mình sẽ thử kiểm tra xem **target** có tiết lộ đến một directory hidden nào hay không. Ở đây mình sử dụng tool **dirsearch** như sau

![image3](https://live.staticflickr.com/65535/53112687595_0cffe70b34_w.jpg)

![image4](https://live.staticflickr.com/65535/53112774928_187d0b7644.jpg)

Nhưng có lẽ nó không tiết lộ điều gì. Ở đây có thể là do dirseach không thực sự tốt đối với bài này. Ở đây tôi sẽ thử với gobuster đi kèm với một worldlist mạnh mẽ hơn.

![image5](https://live.staticflickr.com/65535/53111691307_261e1f71b4_w.jpg)

Và ta tìm thấy một /blood. Tiến hành truy cập đến 10.10.31.188/blood

![image6](https://live.staticflickr.com/65535/53112322506_671a043f05_c.jpg)

Mình sẽ cần đăng kí một tài khoản, bây giờ chúng ta sẽ tiến hành đăng kí

![image7](https://live.staticflickr.com/65535/53112823248_45c3dc1629_z.jpg)

![image8](https://live.staticflickr.com/65535/53112823218_9cc8bcf424_z.jpg)

Sau khi đăng kí tài khoản xong, ta login tài khoản mới lập vào trang web

![image9](https://live.staticflickr.com/65535/53112823208_3ab88b9abb_z.jpg)

![image10](https://live.staticflickr.com/65535/53112528629_df78ebefbf_z.jpg)

Tôi để ý có một panel chứa các khung điều hướng, tôi click vào biểu tượng danh sách người hiến máu và nhìn thấy một người có name là **Nare**, tất cả mọi thứ về người này bao gồm phone , address ,.., Ở đây ta có thể xem chi tiết info của người này và chú ý trên Url

![image11](https://live.staticflickr.com/65535/53112528599_3f3a47830e_b.jpg)

![image12](https://live.staticflickr.com/65535/53112823173_01254877e8.jpg)

Bây giờ nhận thấy id chính là một param dễ bị tấn công, tôi sẽ dùng sqlmap để retrieve ra các database, tôi sẽ dùng một GET based như sau:

```bash
sqlmap -u http://10.10.31.188/blood/view.php?id=1 --dbs
```

![image13](https://live.staticflickr.com/65535/53112528619_19e66d971b.jpg)

Nhìn vào kết quả trả về ta đã **fetch** được 6 database, bây giờ ta sẽ retrieve tất cả mọi thứ từ database **blood**

```bash
sqlmap -u http://10.10.31.188/blood/view.php?id=1 -D blood --dump-all
```

Kaka bây giờ mọi thứ đã được retrieve ra, ta sẽ tìm được flag

![image14](https://live.staticflickr.com/65535/53112737485_2a81310af5_w.jpg)

```
Flag: thm{sqlm@p_is_L0ve}
```
