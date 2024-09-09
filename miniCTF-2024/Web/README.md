## Solution

### Web: Hidden Flag

Trang web cho ta một form đăng nhập như sau

![img1](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/miniCTF-2024/Web/images/image-01.png?raw=true)

Check source code của trang web và kiểm tra các file được nhúng vào như `html, css , js`

Có hai file `.html` có thể khai thác được

![img2](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/miniCTF-2024/Web/images/image-02.png?raw=true)

Di chuyển đến đường dẫn `/forgotpass.html` và vẫn tiếp tục check source code , tìm được file `css` ở cuối file có một đoạn số `2340510522183513221474498965418877`

![img3](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/miniCTF-2024/Web/images/image-03.png?raw=true)

Sử dụng tool [kt.gy](https://kt.gy/tools.html#conv/see_m3_h3h3h3%7D) ta sẽ nhận ra đây là phần cuối cùng của `flag`

![img4](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/miniCTF-2024/Web/images/image-04.png?raw=true)

> see_m3_h3h3h3}

Tiếp tục đi đến `/register/html` và check source code và tương tự vào file `css` của page ta thấy một đoạn comment ở cuối file trông khá giống một mã base nào đó
`OVPWGNDOL4======`

![img5](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/miniCTF-2024/Web/images/image-05.png?raw=true)

Sử dụng tool `basecrack` để phát hiện loại `base` và tiến hành `decode`

![img6](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/miniCTF-2024/Web/images/image-06.png?raw=true)

Vậy nó là base32 và phần flag tìm được là `u_c4n_`

Vậy phần đầu chứa chuỗi bắt đầu của flag là `miniCTF{` đang nằm ở đâu. Sau một hồi làm đủ trò không tìm được thì tôi nhận ra ở ngay đầu lúc vào web trang web có chắc năng đăng nhập tài khoản, vì vậy tôi tiến hành đăng ký đại một tài khoản để vào bên trong

Sau khi đăng ký và đăng nhập vào sẽ thấy một `page` chỉ có đúng `background` màu vàng. Vẫn quen thuộc tiến hành check source code và sẽ thấy phần đầu của `flag`

![img7](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/miniCTF-2024/Web/images/image-07.png?raw=true)

> miniCTF{N0w\_

> Flag: miniCTF{N0w_u_c4n_see_m3_h3h3h3}

### Web: I love eating food

Ở bài này sau khi check source không thấy gì tôi bắt đầu kiểm tra cookie của trang web và thấy có một trường là `login_cookie` đang bị set giá trị là `0`

![img8](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/miniCTF-2024/Web/images/image-08.png?raw=true)

Tôi set lại với giá trị là 1, và `refresh` lại web sẽ thấy hộp `alert` báo `login success` nhưng không thấy `flag` xuất hiện

![img9](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/miniCTF-2024/Web/images/image-09.png?raw=true)

Ở đây bạn tinh ý một chút sẽ thấy một thẻ `p` bị ẩn ở ngay dưới button `login` , quét chuột vào sẽ thấy `flag`

![img10](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/miniCTF-2024/Web/images/image-10.png?raw=true)

Ở đây nếu check source sẽ không thấy `flag` hiện ra do thẻ p này tác giả đã set color cho nó cùng màu trắng với background của `form login` vì vậy để thấy flag nên `inspect element` để tìm thấy flag

> Flag: miniCTF{w0w*y0u_kn0w_c00kj3*:3}

### Web: TokenOfTrust

Tên thử thách nói về token khả năng cao đây là `chall` về `JWT`

Trang web cho 1 form login do chưa có tài khoản nên tôi tiến hành đăng ký và tiến hành đăng nhập, một `/dashboard.php` hiện ra

![img11](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/miniCTF-2024/Web/images/image-11.png?raw=true)

Trang web có gợi ý về `John` ý muốn nói đến `John The Ripper` một công cụ bảo mật nhằm crack `signature` ở phần mã token nhằm thay đổi mã token mới để mục đích leo thang đặc quyền

Khoan hãy nghĩ đến việc sử dụng `John` để crack `signature` tôi check source và ra luôn `key`:)))

![img12](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/miniCTF-2024/Web/images/image-12.png?raw=true)

> key: ilovePP

Sử dụng extension `EditThisCookie` để xem cookie của trang web nhanh hơn sẽ thấy một giá trị `token`

![img13](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/miniCTF-2024/Web/images/image-13.png?raw=true)

Copy mã `token` này và ném lên [jwt.io](jwt.io) để phân tích

![img14](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/miniCTF-2024/Web/images/image-14.png?raw=true)

Ở phần `data` của `token` key `auth` bị set thành `false` , cập nhật lại `true` -> leo thang đặc quyền , token sử dụng thuật toán `HMACSHA256` và được ký bằng một `key` ta vừa tìm được ở trên

![img15](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/miniCTF-2024/Web/images/image-15.png?raw=true)

Token mới `eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiaGloaTEyMyIsImF1dGgiOnRydWV9.QgeSmIgoRBR4SpagqBfdXUkcrJH5OIpmdhhHrlgQSzE`

Copy lại đoạn token vừa được thay thế vào và tiến hành `refresh` lại để lấy `flag`

![img16](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/miniCTF-2024/Web/images/image-16.png?raw=true)

![img17](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/miniCTF-2024/Web/images/image-17.png?raw=true)

> Flag: miniCTF{n3v3r_trust_JWT_w1th0ut_v3r1fy}
