Đây là một bài lab về JWT(Json Web Token), nhìn qua thì có vẻ sẽ bypass token để truy cập vào url/flag dưới quyền `Admin`

![anh1](https://raw.githubusercontent.com/Giangattt123/C4ptur3_Th3_Fl4g/master/CookieHanHoan/Web/The%20JWT%20Algorithm/images/anh1.jpg)

Trang web hiện ra với 1 form đăng nhập như bao gồm có username và password

![anh2](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/CookieHanHoan/Web/The%20JWT%20Algorithm/images/anh2.jpg?raw=true)

Sử dụng tool `dirsearch` trích xuất các directory , param ẩn của trang web thấy có hai đường dẫn rất có thể là điểm khai thác là `/robots.txt` và `/secret`(có thể sử dụng Scan trên Burp Suite , ffuf ,...)

![anh3](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/CookieHanHoan/Web/The%20JWT%20Algorithm/images/anh3.jpg?raw=true)

Truy cập vào `/robots.txt` cũng sẽ thấy `/secret`.

![anh4](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/CookieHanHoan/Web/The%20JWT%20Algorithm/images/anh4.jpg?raw=true)

Chúng ta thấy có `User-agent` là `Googlebot` thay vì `Mozilla` mặc định theo trình duyệt. Vì vậy ở đây tôi sẽ thay đổi `User-agent` trên url `/secret` bằng câu lệnh **curl** với tham số **--user-agent** có `value` là **Googlebot**

![anh5](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/CookieHanHoan/Web/The%20JWT%20Algorithm/images/anh5.jpg?raw=true)

Một **username:password** hiện ra, lấy account và tiến hàng đăng nhập nó sẽ `redirect` đến `/flag` và tất nhiên ta không phải **admin** nên không có quyền

![anh6](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/CookieHanHoan/Web/The%20JWT%20Algorithm/images/anh6.jpg?raw=true)

Chúng ta bắt request bằng burpsuite sẽ thấy có cookie như đề bài đã nói. Ý tưởng sẽ là copy lên `JWT decode` để sửa `user` thành **admin** . Nhưng mà chúng ta có 2 cái JWT, nếu để ý bạn sẽ thấy JWT thứ hai có vấn đề ở phần **payload** , tiếp nữa JWT thứ nhất đang lồng vào token của JWT thứ hai

![anh7](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/CookieHanHoan/Web/The%20JWT%20Algorithm/images/anh7.jpg?raw=true)
![anh8](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/CookieHanHoan/Web/The%20JWT%20Algorithm/images/anh8.jpg?raw=true)

Nếu cố gắng sửa JWT thì nó sẽ hiện thông báo lỗi `Invalid Token`. Ở đây tôi sẽ chính sửa JWT ngay trên `BurpSuite` ở tab `Repeater`.

> Để có thể chỉnh sửa được ta cần chỉnh `alg` về `none`
> Chi tiết cách giải thích `bypass` có thể xem ở : [jwt-token-bypass](https://cyb3rlant3rn.medium.com/jwt-token-bypass-f12a2e63622a)

- Hiểu đơn giản khi sửa `alg` thành `none` sẽ giúp loại bỏ đi phần `signature`
- Khi máy chủ nhận được dạng mã thông báo như vậy, do thuật toán là **“none”**, nó không thực hiện xác minh chữ ký. Do đó, kẻ tấn công có thể thao túng tải trọng giá trị mà không bị phát hiện từ phía máy chủ và nhận được sự leo thang đặc quyền theo chiều dọc hoặc chiều ngang

![anh9](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/CookieHanHoan/Web/The%20JWT%20Algorithm/images/anh9.jpg?raw=true)
