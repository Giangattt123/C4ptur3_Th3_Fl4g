# Solution

> Truy cập vào đường dẫn [link](https://nicc-hostile-takeover.chals.io/) để xem content web

![image1](https://live.staticflickr.com/65535/52749806867_83bb346e74_b.jpg)

Mô tả của nó là đây là một trang web được thiết lập siêu an toàn. **Admin** xuất hiện trên kia có thể là một cổng quản trị và họ nói chỉ có họ mới có thể truy cập vào đó. Khi chúng ta truy cập vào cổng đó sẽ nhận được thông báo 403.

> Có một gợi ý nho nhỏ có cuối là háy "STOP" truy cập vào cổng đó. Ohhh, ta nảy ra một suy nghĩ rằng uhmm.. tôi nghĩ là tôi chưa có ý tưởng gì. Ta xem hint của challenge, đây thực sự là hint có ích nhất tôi từng xem ở một số bài CTF **"The admin page may only be accessed by people on the local computer"** ý nói trang web này chỉ có thể truy cập bởi những người trên máy tính cục bộ => phải kết nối với **localhost** khi truy cập trang quản trị

Hiểu đơn giản thì khi kết nối với **"localhost"**, nó sẽ trỏ đến địa chỉ IP của máy tính mà trang web đang chạy trên đó. Điều này đảm bảo rằng chỉ có những người có quyền truy cập từ máy tính cục bộ mới có thể truy cập trang quản trị viên, và không ai khác từ các thiết bị khác trên mạng Internet.

Việc sử dụng kết nối "localhost" là một biện pháp an ninh cơ bản nhưng hiệu quả để bảo vệ dữ liệu nhạy cảm của trang quản trị viên tránh khỏi các cuộc tấn công từ các nguồn bên ngoài.

> Ở đây làm tương tự tôi sẽ sử dụng **Burp Suite** để bắt request trước khi gửi lên server và đảm bảo rằng **Intercept is on**, sau đó click vào trang quản trị để request được ghi lại

![image2](https://live.staticflickr.com/65535/52749822707_22b2ae2b81_w.jpg)

> Sau đó ta tùy ý tùy biến, chỉnh sửa **Host** thành **localhost**, tiến hành Forward lại và lấy flag vô submit thui ...))

![image3](https://live.staticflickr.com/65535/52750769820_0b955b6cc9.jpg)

> Flag : **"nicc{H0ST_H3AdEr_AtTack}"**
