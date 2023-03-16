# Solution

> Thử thách này là nối tiếp của thử thách NICC 98 , hiểu đơn giản đề bài gợi ý chúng ta tìm kiếm /robots.txt. File robots.txt là một tập tin văn bản đơn giản có dạng .txt. Tệp này là một phần của Robots Exclusion Protocol (REP) chứa một nhóm các tiêu chuẩn Web quy định cách Robot Web (hoặc Robot của các công cụ tìm kiếm) thu thập dữ liệu trên web, truy cập, index nội dung và cung cấp nội dung đó cho người dùng.

Để chắc chắn hơn về những điều mình nói, tôi sẽ recon trang web này bằng tool ffuf, để sử dụng tool này chúng ta sẽ cần thêm một wordlist , bản chất tool này sử dụng hình thức brute-force nên ta cần một bộ danh sách chứa các đường dẫn file/folder hay dùng.

![image1](https://live.staticflickr.com/65535/52750563069_614043ab3d_z.jpg)

Kết quả đúng như những gì ta suy đoán đúng là trang web có thiết lập robots.txt

![image2](https://live.staticflickr.com/65535/52750735980_78facd9d69_b.jpg)

Tiến hành truy cập vào [link](https://nicc-nicc-98.chals.io/robots.txt) để xem content:

![image3](https://live.staticflickr.com/65535/52750820953_5f4bb138b1_b.jpg)

> Ta để ý thấy sau tác nhân người dùng(User-agent) có một folder không cho phép xem **"/r0b0ts.txt"**. Truy cập vào thư mục này và lấy flag vô submit thui...

![image4](https://live.staticflickr.com/65535/52750741535_c7f4582cfc_c.jpg)

> Flag : **"nicc{@lw@ys_ch3ck_4_r0b0ts}"**
