# Solution

> Truy cập vào đường dẫn "https://nicc-apache-aint-so-bad.chals.io/" sẽ hiển thị trang web

![image1](https://live.staticflickr.com/65535/52748689072_49ab00deb7_c.jpg)

> Có dòng text "page" có thể là một đường dẫn và view source cho thấy đó là đường dẫn đến flag được lưu trữ ở **"secret/flag.txt"** với url là : **https://nicc-apache-aint-so-bad.chals.io/secret/flag.txt**
> Nhưng khi ta truy cập vào đường dẫn trang web đã hiện lên thông báo với status code là 403 Forbidden và đoạn text **"You don't have permission to access this resource."** nghĩa là quyền đối với user là không được phép.
> Quay lại trang web gốc ta thấy có đoạn hint cho challenge này

```
     RewriteEngine On
            RewriteCond %{THE_REQUEST} flag
            RewriteRule ".*" "-" [F]
```

> Ở đây ta có thể đọc hiểu nó một cách đơn giản đây là một đoạn mã trong tệp tin cấu hình của Apache web server để thực hiện chức năng "URL rewriting" và "access control". Nó sử dụng module "mod_rewrite" của Apache để ánh xạ lại URL và chặn các yêu cầu có chứa từ "flag".
> Cụ thể, đoạn mã này bao gồm:

- Dòng đầu tiên "RewriteEngine On" bật tính năng "URL rewriting" của module "mod_rewrite".
- Dòng thứ hai "RewriteCond %{THE_REQUEST} flag" thiết lập một điều kiện để kiểm tra xem yêu cầu có chứa từ "flag" không.
- Dòng thứ ba "RewriteRule ".\*" "-" [F]" áp dụng một quy tắc ánh xạ lại URL, trong đó mọi URL đều được ánh xạ đến dấu gạch ngang "-" và trả về mã trạng thái HTTP 403 "Forbidden" ([F]) cho bất kỳ yêu cầu nào thỏa mãn điều kiện của RewriteCond.

  > Vì vậy ở đây ta có thể tìm cách bypass khỏi bộ lọc từ flag này, đơn giản nhất đó chính là mã hóa URL hay đúng nhất là encode **flag** để **"fooling the filtering"**
  > Mã hóa URL chuyển đổi các ký tự thành một định dạng có thể được truyền qua Internet. URL chỉ có thể được gửi qua Internet bằng cách sử dụng bộ ký tự ASCII. Vì các URL thường chứa các ký tự bên ngoài bộ ASCII, URL phải được chuyển đổi thành định dạng ASCII hợp lệ. Mã hóa URL thay thế các ký tự ASCII không an toàn với "%" theo sau là hai chữ số thập lục phân.
  > Chúng ta có thể xem bộ mã hóa **"ASCII Encoding Reference"** ở [ASCII Encoding Reference](https://www.w3schools.com/tags/ref_urlencode.ASP). Và theo ta đọc được ở đây , tôi sẽ thay thế "f" thành "%66" , l thành "%6C" , "a" thành "%61" và cuối cùng "g" thành "%67". Vậy ta sẽ thay thế "flag" thành **"%66%6C%61%67"**.

  > Ta cũng có thể sử dụng CURL command hoặc sửa đổi trực tiếp trên URL, nhưng ở đây tôi sẽ sử dụng công cụ **BurpSuite**(...vì nó ngầu😁hmm...)

![image2](https://live.staticflickr.com/65535/52749679640_3cd90cb06e_c.jpg)

> Sau đó khởi động intercept ở trạng thái on để bắt request gửi lên server, sau đó truy cập vào **"page"**, lúc này request sẽ được giữ lại và ta có thể tùy ý tùy biến.

![image3](https://live.staticflickr.com/65535/52749275406_fed9733bff.jpg)

> Mã hóa URL ở header từ /flag.txt thành /%66%6C%61%67.txt rồi tiến hành **"Forward"** lại sẽ thu được flag.

![image4](https://live.staticflickr.com/65535/52749784628_21a3522e44.jpg)

>

![image5](https://live.staticflickr.com/65535/52749535249_ef02a13666_c.jpg)

> Flag : **"nicc{UrL_ENC0DED_STR1NgS_AR3_SC@ry}"**
