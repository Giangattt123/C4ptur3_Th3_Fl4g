# SQL Injection

## What is SQL injection (SQLi)?

- SQL injection là một lỗ hổng bảo mật web cho phép kẻ tấn công can thiệp vào các truy vấn mà ứng dụng thực hiện đối với cơ sở dữ liệu. Nó giúp kẻ tấn công xem dữ liệu mà mà thông thường chúng không truy xuất được. Trong nhiều trường hợp, kẻ tấn công có thể sửa đổi hoặc xóa dữ liệu của úng dụng.

- [sqlinjection-cheat sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)

  ![img1](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PortSwiggers/SQL-Injection/images/image-1.png?raw=true)

## What is the impact of a successful SQL injection attack?

Một cuộc tấn công tiêm SQL thành công có thể dẫn đến truy cập trái phép vào dữ liệu nhạy cảm, chẳng hạn như:

- Mật khẩu.
- Chi tiết thẻ tín dụng.
- Thông tin cá nhân của người dùng.

Các cuộc tấn công tiêm SQL đã được sử dụng trong nhiều vụ vi phạm dữ liệu cấp cao trong nhiều năm qua. Những vụ tấn công này đã gây ra thiệt hại về uy tín và các khoản tiền phạt theo quy định. Trong một số trường hợp, kẻ tấn công có thể có được một cửa hậu liên tục vào hệ thống của một tổ chức, dẫn đến sự xâm phạm lâu dài có thể không được phát hiện trong một thời gian dài.

## How to detect SQL injection vulnerabilities

Bạn có thể phát hiện `SQL injection` theo cách thủ công bằng cách sử dụng một tập hợp các bài kiểm tra có hệ thống đối với mọi điểm vào trong ứng dụng. Để thực hiện việc này, bạn thường sẽ gửi:

- Ký tự dấu nháy đơn ' và tìm kiếm lỗi hoặc các bất thường khác.
- Một số cú pháp SQL cụ thể đánh giá theo giá trị cơ sở (gốc) của điểm nhập và một giá trị khác, đồng thời tìm kiếm sự khác biệt có hệ thống trong phản hồi của ứng dụng.
- Các điều kiện `boolean` như `OR 1=1` và `OR 1=2` , và tìm kiếm sự khác biệt trong phản hồi của ứng dụng.
- Tải trọng được thiết kế để kích hoạt độ trễ thời gian khi được thực hiện trong truy vấn SQL và tìm kiếm sự khác biệt về thời gian phản hồi.
- [OAST payloads](https://portswigger.net/burp/application-security-testing/oast) được thiết kế để kích hoạt tương tác mạng ngoài băng tần khi được thực hiện trong truy vấn SQL và giám sát mọi tương tác phát sinh.

Ngoài ra, bạn có thể tìm thấy phần lớn các lỗ hổng `SQL injection` một cách nhanh chóng và đáng tin cậy bằng [Burp Scanner](https://portswigger.net/burp/vulnerability-scanner)

## SQL injection in different parts of the query

Hầu hết các lỗ hổng SQL injection xảy ra trong mệnh đề `WHERE` của truy vấn `SELECT`. Hầu hết các kiểm thử viên có kinh nghiệm đều quen thuộc với loại SQL injection này.

Tuy nhiên, lỗ hổng SQL injection có thể xảy ra ở bất kỳ vị trí nào trong truy vấn và trong các loại truy vấn khác nhau. Một số vị trí phổ biến khác mà SQL injection phát sinh là:

- Trong các câu lệnh `UPDATE`, trong các giá trị được cập nhật hoặc mệnh đề `WHERE`
- Trong các câu lệnh `INSERT`, bên trong các giá trị được chèn vào.
- Trong các câu lệnh `SELECT`, bên trong tên bảng hoặc cột.
- Trong các câu lệnh `SELECT`, trong mệnh đề `ORDER BY`.

## SQL injection examples

Có rất nhiều lỗ hổng, cuộc tấn công và kỹ thuật SQL injection xảy ra trong nhiều tình huống khác nhau. Một số ví dụ phổ biến về SQL injection bao gồm:

- `Retrieving hidden data`, where you can modify a SQL query to return additional results.
- `Subverting application logic`, where you can change a query to interfere with the application's logic.
- `UNION attacks`, where you can retrieve data from different database tables.
- `Blind SQL injection`, where the results of a query you control are not returned in the application's responses.

## Retrieving hidden data ( Truy xuất dữ liệu ẩn )

- Hãy xem xét một ứng dụng mua sắm hiển thị các sản phẩm trong các danh mục khác nhau. Khi người dùng nhấp vào danh mục Quà tặng, trình duyệt của họ sẽ yêu cầu URL:

  ` https://insecure-website.com/products?category=Gifts`

- Điều này khiến ứng dụng tạo một truy vấn SQL để truy xuất thông tin chi tiết về các sản phẩm có liên quan từ cơ sở dữ liệu:

  ` SELECT * FROM products WHERE category = 'Gifts' AND released = 1`

- Ứng dụng không thực hiện bất kỳ biện pháp bảo vệ nào chống lại các cuộc tấn công SQL injection, vì vậy kẻ tấn công có thể tạo ra một cuộc tấn công như:

  ` https://insecure-website.com/products?category=Gifts'--`

  - Điều này khiến ứng dụng tạo một truy vấn SQL như sau:
    `SELECT * FROM products WHERE category = 'Gifts'--' AND released = 1`

- OR

  ` SELECT * FROM products WHERE category = 'Gifts' OR 1=1--' AND released = 1`

## Subverting application logic (Phá vỡ logic)

Hãy xem xét một ứng dụng cho phép người dùng đăng nhập bằng tên người dùng và mật khẩu. Nếu người dùng gửi tên người dùng là `wiener` và mật khẩu là `bluecheese`, ứng dụng sẽ kiểm tra thông tin đăng nhập bằng cách thực hiện truy vấn SQL sau:

```
SELECT * FROM users WHERE username = 'wiener' AND password = 'bluecheese'
```

Nếu truy vấn trả về thông tin chi tiết của người dùng thì đăng nhập thành công. Nếu không, nó bị từ chối.

Kẻ tấn công có thể đăng nhập bất kì với tư cách là người dùng mà không cần mật khẩu như sau `administrator'--`

```
SELECT * FROM users WHERE username = 'administrator'--' AND password = ''
```

Điều này khiến ứng dụng trả về thông tin chi tiết của người dùng `administrator` mà không cần kiểm tra mật khẩu

## Retrieving data from other database tables (Lấy dữ liệu từ các bảng cơ sở dữ liệu khác)

```
SELECT name, description FROM products WHERE category = 'Gifts'
```

Kẻ tấn công có thể gửi input nhập vào như sau:

```
' UNION SELECT username, password FROM users--
```

Giả sử data của bảng `products` như sau:

```
id	| name	| description	| category

1	| Teddy Bear |	Soft toy bear |	Gifts

2	| Flower Bouquet |	Fresh flowers| Gifts

3	|Phone Case	| Protective case	| Accessories
```

Giả sử data của bảng `users` như sau:

```
id	| username	| password
1	| admin	| 12345
2	| john_doe	| qwerty
3	| alice	| alice_password
```

Truy vấn ban đầu (an toàn):

```
SELECT name, description FROM products WHERE category = 'Gifts';
```

Kết quả của truy vấn an toàn

```
name	| description
Teddy Bear|	Soft toy bear
Flower Bouquet| Fresh flowers
```

Truy vấn khi bị tấn công SQL Injection:

- Kẻ tấn công có thể nhập chuỗi **' UNION SELECT username, password FROM users--**, biến câu truy vấn ban đầu thành:

  ```
  SELECT name, description FROM products WHERE category = '' UNION SELECT username, password FROM users --';
  ```

- Kết quả sau khi bị SQL Injection:

  ```
  name	| description
  admin	| 12345
  john_doe|	qwerty
  alice	|alice_password
  ```

Kẻ tấn công có thể lấy được danh sách `username` và `password` từ bảng `users` thay vì chỉ lấy dữ liệu từ bảng `products`. Đây là ví dụ minh họa cách mà SQL Injection có thể bị lợi dụng để đánh cắp dữ liệu nhạy cảm từ cơ sở dữ liệu.

## Examining the database

Để khai thác lỗ hổng SQL injection , thường cần phải tìm thông tin về cơ sở dữ liệu. Bao gồm:

Loại và phiên bản của phần mềm cơ sở dữ liệu.
Các bảng và cột có trong cơ sở dữ liệu.

> Truy vấn loại cơ sở dữ liệu và phiên bản

- Microsoft, MySQL: `SELECT @@version`
- Oracle: `SELECT * FROM v$version`
- PostgreSQL: `SELECT version()`

Ví dụ, bạn có thể sử dụng lệnh `UNION` để tấn công với thông tin đầu vào sau: `' UNION SELECT @@version--`

> Liệt kê nội dung của cơ sở dữ liệu

Hầu hết các loại cơ sở dữ liệu (trừ Oracle) đều có một tập hợp các chế độ xem được gọi là lược đồ thông tin. Điều này cung cấp thông tin về cơ sở dữ liệu.

Ví dụ, bạn có thể truy vấn `information_schema.tables` để liệt kê các bảng trong cơ sở dữ liệu:

Xác định csdl đang tồn tại những bảng nào và chúng chứa những cột nào

```
SELECT * FROM information_schema.tables;
```

![img3](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PortSwiggers/SQL-Injection/images/image-3.png?raw=true)

## Blind SQL injection vulnerabilities

Nhiều khi ứng dụng không trả về kết quả truy vấn của sql hoặc chi tiết về bất cứ cơ sơ dữ liệu nào. Các lỗ hổng `blind sql` vẫn có thể bị khai thác truy cập dữ liệu trái phép , nhưng các kỹ thuật liên quan thường phức tạp hơn và khó thực hiện hơn

- Bạn có thể thay đổi logic của truy vấn để kích hoạt sự khác biệt có thể phát hiện được trong phản hồi của ứng dụng tùy thuộc vào tính đúng đắn của một điều kiện duy nhất. Điều này có thể bao gồm việc đưa một điều kiện mới vào một số logic `boolean` hoặc kích hoạt có điều kiện một lỗi như chia cho số không.

- Bạn có thể kích hoạt có điều kiện thời gian trễ trong quá trình xử lý truy vấn. Điều này cho phép bạn suy ra sự thật của điều kiện dựa trên thời gian ứng dụng phản hồi.

- Bạn có thể kích hoạt tương tác mạng ngoài băng tần, sử dụng các kỹ thuật `OAST`. Kỹ thuật này cực kỳ mạnh mẽ và hoạt động trong những tình huống mà các kỹ thuật khác không làm được.
  Thông thường, bạn có thể trực tiếp trích xuất dữ liệu qua kênh ngoài băng tần. Ví dụ, bạn có thể đặt dữ liệu vào tra cứu DNS cho một tên miền mà bạn kiểm soát.

### Exploiting blind SQL injection by triggering conditional responses

Hãy xem xét một ứng dụng sử dụng cookie theo dõi để thu thập phân tích . Yêu cầu đối với ứng dụng bao gồm tiêu đề cookie như sau:

```
Cookie: TrackingId=u5YD3PapBcR4lN3e7Tj4
```

Khi yêu cầu chứa `TrackingIdcookie` được xử lý, ứng dụng sẽ sử dụng truy vấn SQL để xác định xem đây có phải là người dùng đã biết hay không:

```
SELECT TrackingId FROM TrackedUsers WHERE TrackingId = 'u5YD3PapBcR4lN3e7Tj4'
```

Truy vấn này dễ bị `SQL injection`, nhưng kết quả từ truy vấn không được trả về cho người dùng. Tuy nhiên, ứng dụng sẽ hoạt động khác nhau tùy thuộc vào việc truy vấn có trả về dữ liệu nào không. Nếu bạn gửi một truy vấn được công nhận `TrackingId`, truy vấn sẽ trả về dữ liệu và bạn nhận được thông báo "Welcome back" trong phản hồi.

Hành vi này đủ để có thể khai thác lỗ hổng SQL injection. Bạn có thể lấy thông tin bằng cách kích hoạt các phản hồi khác nhau có điều kiện, tùy thuộc vào điều kiện được tiêm.

Để hiểu cách khai thác này hoạt động, hãy giả sử có hai yêu cầu được gửi `TrackingId` lần lượt chứa các giá trị `cookie` sau:

```
…xyz' AND '1'='1
…xyz' AND '1'='2
```

- Giá trị đầu tiên trong số các giá trị này khiến truy vấn trả về kết quả, vì AND '1'='1 điều kiện được đưa vào là đúng. Kết quả là, thông báo "Chào mừng trở lại" được hiển thị.

- Giá trị thứ hai khiến truy vấn không trả về bất kỳ kết quả nào vì điều kiện được đưa vào là sai. Thông báo "Chào mừng trở lại" không được hiển thị.

Điều này cho phép chúng ta xác định câu trả lời cho bất kỳ điều kiện nào được đưa vào và trích xuất dữ liệu từng phần một.

Ví dụ, giả sử có một bảng được gọi `Users` với các cột `Username` và `Password`, và một người dùng được gọi là `Administrator`. Bạn có thể xác định mật khẩu cho người dùng này bằng cách gửi một loạt các đầu vào để kiểm tra mật khẩu từng ký tự một. Để thực hiện việc này, hãy bắt đầu bằng thông tin sau:

```
xyz' AND SUBSTRING((SELECT Password FROM Users WHERE Username = 'Administrator'), 1, 1) > 'm
```

Lệnh này trả về thông báo "Chào mừng trở lại", cho biết điều kiện được đưa vào là đúng và do đó ký tự đầu tiên của mật khẩu lớn hơn `m`

Tiếp theo, chúng ta gửi thông tin đầu vào sau:

```
xyz' AND SUBSTRING((SELECT Password FROM Users WHERE Username = 'Administrator'), 1, 1) > 't
```

Điều này không trả về thông báo "Chào mừng trở lại", cho biết điều kiện được đưa vào là sai và do đó ký tự đầu tiên của mật khẩu không lớn hơn `t`.

Cuối cùng, chúng tôi gửi dữ liệu đầu vào sau, trả về thông báo "Chào mừng trở lại", qua đó xác nhận ký tự đầu tiên của mật khẩu là `s`:

Chúng ta có thể tiếp tục quá trình này để xác định một cách có hệ thống toàn bộ mật khẩu cho người dùng `Administrator`

> Lab: Blind SQL injection with conditional responses

Mục tiêu của bài lab là lấy được `password` của `administrator`, sau đó đăng nhập với `password` vừa tìm được đó

Truy cập vào tab `Home` sẽ thấy dòng chữ `Welcom back`, kiểm tra `cookie` có trên trang web ta thấy có trường `TrackingId`, ứng dụng xử lí giá trị này để kiểm tra xem đây có phải một người dùng đã được track rồi hay không

![img4](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PortSwiggers/SQL-Injection/images/image-4.png?raw=true)

Ở đây đề bài đã cung cấp là trường `TrackingId` dễ bị tấn công, trong trường hợp không biết chúng ta có thể `fuzzing` cả param `session` nhé

Mở burpsuite để dễ dàng phân tích và khai thác hơn

![img5](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PortSwiggers/SQL-Injection/images/image-5.png?raw=true)

Bây giờ chúng ta sẽ thử xem liệu param `TrackingId` có phải là một `param` dễ bị các cuộc tấn công hay không bằng cách thử sai và thử đúng để xem cách mà server sẽ phản hồi lại

- Đối với một giá trị `TrackingId` đã tồn tại ví dụ như trong bảng `TrackingTable` chúng ta sẽ nhận được thông báo với message `Welcome back`, ví dụ như chính là giá trị trên

- Đối với giá trị không tồn tại chắc chắn server sẽ phản hồi khác, bằng chứng là khi tôi điền thêm 1 vài kí tự lạ khác vào giá trị ban đầu và tiến hành gửi request ở response không còn hiện message `Welcome back` nữa

  ![img6](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PortSwiggers/SQL-Injection/images/image-6.png?raw=true)

- Tôi tiếp tục thử nghiệm nếu kết hợp toán tử `and` đi kèm với một biểu thức luôn đúng

  ![img7](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PortSwiggers/SQL-Injection/images/image-7.png?raw=true)

  ![img8](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PortSwiggers/SQL-Injection/images/image-8.png?raw=true)

- Tiếp theo chúng ta sẽ kiểm tra sự tồn tại của bảng `users` bằng câu lệnh đi kèm `(select 'x' from users LIMIT 1) = 'x'`

  - Nếu bảng `users` có ít nhất một dòng , truy vấn con sẽ trả về 'x', và điều kiện so sánh = 'x' sẽ là đúng.
  - Nếu bảng `users` trống (không có dòng nào), truy vấn con sẽ không trả về giá trị nào, và do đó điều kiện sẽ không được thỏa mãn, trả về false.

  ![img9](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PortSwiggers/SQL-Injection/images/image-9.png?raw=true)

  => có sự tồn tại của bảng `users`

- Tiếp tục mình sẽ kiểm tra xem user `administrator` có thực sự tồn tại trong bảng `users` hay không

  ```
  sgEetNS5vVXUQTP6' and (select username from users where username='administrator')='administrator'--
  ```

  ![img10](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PortSwiggers/SQL-Injection/images/image-10.png?raw=true)

  => có sự tồn tại của user `administrator`

Bây giờ sau khi biết chắc chắn param `TrackingId` là param dễ bị tấn công và table `users` hay user `administrator` đều tồn tại chúng ta sẽ đi lần mò ra `password` của administrator để hoàn thành lab

- Chúng ta có thể thử kiểm tra độ dài của `password` trước

  ```
  Qi2EGJmKAvvASkFp' and (select username from users where username='administrator' and length(password)>1)='administrator'--
  ```

  ![img11](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PortSwiggers/SQL-Injection/images/image-11.png?raw=true)

  => `password` của admin lớn hơn một kí tự

- Nhưng nếu thử như vậy hẳn sẽ rất lâu tôi sẽ sử dụng `burp intruder`

  ![img12](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PortSwiggers/SQL-Injection/images/image-12.png?raw=true)

  ![img13](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PortSwiggers/SQL-Injection/images/image-13.png?raw=true)

  ![img14](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PortSwiggers/SQL-Injection/images/image-14.png?raw=true)

  => `password` có độ dài 20 kí tự

  - Đề bài cũng nói rõ là `password` chỉ bao gồm các kí tự chữ cái và số, bây giờ chắc chắn chúng ta sẽ phải `bruteforce` , tôi tiếp tục sử dụng `burp intruder`

    ```
    Qi2EGJmKAvvASkFp' and (select substring(password,1,1) from users where username='administrator')='a'--
    ```

  - Nếu chỉ làm như này chúng ta sẽ phải brutefore 20 vị trí của password, như trong hình kí tự đầu tiên của `password` là chữ `i`

    ![img15](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PortSwiggers/SQL-Injection/images/image-15.png?raw=true)

  - Vì vậy tôi sẽ sử dụng `cluster bomb attack`

    ![img16](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PortSwiggers/SQL-Injection/images/image-16.png?raw=true)

  - Filter với dòng `welcome` sẽ thấy được kí tự đúng ứng với từng vị trí

    ![img17](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PortSwiggers/SQL-Injection/images/image-17.png?raw=true)

  > `password`: `idqfj2ag1nd4hphkjqlu`

Cuối cùng nhập `username` là `administrator` và `password` ở trên để `solve` bài lab

![img18](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PortSwiggers/SQL-Injection/images/image-18.png?raw=true)

Tôi sẽ viết thêm 1 script bằng python để làm việc này như sau: [script](), nó cũng không khác là mấy chúng ta vẫn `bruteforce` được `password`

![img19](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PortSwiggers/SQL-Injection/images/image-19.png?raw=true)

## SQL injection UNION attacks

Khi một ứng dụng dễ bị `SQL injection` và kết quả của truy vấn được trả về trong phản hồi của ứng dụng, bạn có thể sử dụng từ khóa `UNION` để truy xuất dữ liệu từ các bảng khác trong cơ sở dữ liệu. Điều này thường được gọi là `SQL injection UNION attack`.

Từ khóa này cho phép bạn thực hiện một hoặc nhiều truy vấn `SELECT` bổ sung và thêm kết quả vào truy vấn ban đầu. Ví dụ:

`SELECT a, b FROM table1 UNION SELECT c, d FROM table2`

Truy vấn SQL này trả về một tập kết quả duy nhất với hai cột, chứa các giá trị từ các cột a và b trong table1 và các cột c và d trong table2.

Để truy vấn `UNION` hiệu quả, hai yêu cầu chính cần được đáp ứng:

- Các truy vấn riêng lẻ phải trả về cùng số cột
- Các kiểu dữ liệu trong mỗi cột phải tương thích giữa các truy vấn riêng lẻ

Để thực hiện một cuộc tấn công `SQL injection UNION`, hãy đảm bảo rằng cuộc tấn công của bạn đáp ứng được hai yêu cầu trên. Điều này thường liên quan đến việc tìm hiểu:

- Có bao nhiêu cột được trả về từ truy vấn ban đầu.

- Những cột nào được trả về từ truy vấn gốc có kiểu dữ liệu phù hợp để lưu trữ kết quả từ truy vấn được đưa vào.

## Determining the number of columns required(xác định số lượng cột cần thiết)

Khi bạn thực hiện tấn công SQL injection UNION, có hai phương pháp hiệu quả để xác định có bao nhiêu cột được trả về từ truy vấn gốc.

Một phương pháp bao gồm việc chèn một loạt các mệnh đề `ORDER BY` và tăng chỉ số cột được chỉ định cho đến khi xảy ra lỗi. Ví dụ, nếu điểm chèn là một chuỗi được trích dẫn đề `WHERE` của truy vấn gốc, bạn sẽ gửi:

```
' ORDER BY 1--
' ORDER BY 2--
' ORDER BY 3--
etc.
```

Chuỗi `payload` này sửa đổi truy vấn gốc để sắp xếp kết quả theo các cột khác nhau trong tập kết quả. Cột trong mệnh đề `ORDER BY` có thể được chỉ định theo chỉ mục của nó, do đó bạn không cần biết tên của bất kỳ cột nào. Khi chỉ mục cột được chỉ định vượt quá số lượng cột thực tế trong tập kết quả, cơ sở dữ liệu trả về lỗi, chẳng hạn như:

```
The ORDER BY position number 3 is out of range of the number of items in the select list.
```

Ứng dụng có thể thực sự trả về lỗi cơ sở dữ liệu trong phản hồi HTTP của nó, nhưng nó cũng có thể đưa ra phản hồi lỗi chung. Trong những trường hợp khác, nó có thể chỉ trả về không có kết quả nào cả. Dù bằng cách nào, miễn là bạn có thể phát hiện ra một số khác biệt trong phản hồi, bạn có thể suy ra có bao nhiêu cột đang được trả về từ truy vấn.

Phương pháp thứ hai bao gồm việc gửi một loạt `UNION SELECT` các dữ liệu chỉ định số lượng giá trị `null` khác nhau:

```
' UNION SELECT NULL--
' UNION SELECT NULL,NULL--
' UNION SELECT NULL,NULL,NULL--
etc.
```

Nếu số lượng giá trị `null` không khớp với số lượng cột, cơ sở dữ liệu sẽ trả về lỗi, chẳng hạn như:

```
All queries combined using a UNION, INTERSECT or EXCEPT operator must have an equal number of expressions in their target lists.
```

Chúng ta sử dụng NULL là gì các giá trị trả về từ truy vấn được đưa vào SELECTvì kiểu dữ liệu trong mỗi cột phải tương thích giữa truy vấn gốc và truy vấn được đưa vào. NULLcó thể chuyển đổi sang mọi kiểu dữ liệu phổ biến, do đó, nó tối đa hóa cơ hội tải trọng sẽ thành công khi số cột là chính xác.

Tương tự như `ORDER BY` ứng dụng có thể thực sự trả về lỗi cơ sở dữ liệu trong phản hồi HTTP của nó, nhưng có thể trả về lỗi chung hoặc đơn giản là không trả về kết quả nào. Khi số lượng giá trị `null` khớp với số lượng cột, cơ sở dữ liệu trả về một hàng bổ sung trong tập kết quả, chứa các giá trị `null` trong mỗi cột. Hiệu ứng đối với phản hồi HTTP phụ thuộc vào mã của ứng dụng. Nếu may mắn, bạn sẽ thấy một số nội dung bổ sung trong phản hồi, chẳng hạn như một hàng bổ sung trên bảng HTML. Nếu không, các giá trị `null` có thể kích hoạt một lỗi khác, chẳng hạn như `NullPointerException`. Trong trường hợp xấu nhất, phản hồi có thể trông giống như phản hồi do số lượng giá trị `null` không chính xác gây ra. Điều này sẽ khiến phương pháp này không hiệu quả.

> Lab: SQL injection UNION attack, finding a column containing text

Trang web hiện ra trông khá giống với một shop có dữ liệu các sản phẩm và ta có thể lấy được các sản phầm thông qua `category`

![img20](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PortSwiggers/SQL-Injection/images/image-20.png?raw=true)

```
https://0a33009e03ea1a238065128c0057001b.web-security-academy.net/filter?category=Tech+gifts
```

Xác định số cột được truy vấn trả về như sau:

```
'+UNION+SELECT+NULL,NULL,NULL--
```

![img21](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PortSwiggers/SQL-Injection/images/image-21.png?raw=true)

Tôi sẽ xem nó rõ ràng hơn trong trình duyệt

![img22](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PortSwiggers/SQL-Injection/images/image-22.png?raw=true)

Truy vấn trả về 3 cột
Bây giờ bài yêu cầu làm cho cơ sở dữ liệu lấy được chuỗi `4KMCMA` tôi sẽ thay nó vào bât kỳ trường `NULL` nào

```
'+UNION+SELECT+'4KMCMA',NULL,NULL--
'+UNION+SELECT+NULL,'4KMCMA',NULL--
'+UNION+SELECT+NULL,NULL'4KMCMA'--
```

## Database-specific syntax

Trên Oracle, mọi truy vấn `SELECT` phải sử dụng từ khóa `FROM` và chỉ định một bảng hợp lệ. Có một bảng tích hợp trên Oracle được gọi là `dual` có thể được sử dụng cho mục đích này. Vì vậy, các truy vấn được tiêm vào trên Oracle sẽ cần trông giống như sau:

`' UNION SELECT NULL FROM DUAL--`

## Finding columns with a useful data type

Tấn công SQL injection UNION cho phép bạn lấy kết quả từ truy vấn inject. Dữ liệu thú vị mà bạn muốn lấy thường ở dạng chuỗi. Điều này có nghĩa là bạn cần tìm một hoặc nhiều cột trong kết quả truy vấn gốc có kiểu dữ liệu là hoặc tương thích với dữ liệu chuỗi.

Sau khi xác định số lượng cột cần thiết, bạn có thể thăm dò từng cột để kiểm tra xem nó có thể chứa dữ liệu chuỗi hay không. Bạn có thể gửi một loạt tải trọng `UNION SELECT` đặt giá trị chuỗi vào từng cột theo lượt. Ví dụ, nếu truy vấn trả về bốn cột, bạn sẽ gửi:

```
' UNION SELECT 'a',NULL,NULL,NULL--
' UNION SELECT NULL,'a',NULL,NULL--
' UNION SELECT NULL,NULL,'a',NULL--
' UNION SELECT NULL,NULL,NULL,'a'--
```

Nếu kiểu dữ liệu cột không tương thích với dữ liệu chuỗi, truy vấn được đưa vào sẽ gây ra lỗi cơ sở dữ liệu, chẳng hạn như:

```
Conversion failed when converting the varchar value 'a' to data type int.
```

Nếu không xảy ra lỗi và phản hồi của ứng dụng chứa một số nội dung bổ sung bao gồm giá trị chuỗi được đưa vào thì cột có liên quan sẽ phù hợp để truy xuất dữ liệu chuỗi.

## Using a SQL injection UNION attack to retrieve interesting data

Khi bạn đã xác định được số cột trả về bởi truy vấn ban đầu và tìm ra cột nào có thể chứa dữ liệu chuỗi, bạn đã có thể truy xuất dữ liệu thú vị.

Giả sử rằng:

- Truy vấn ban đầu trả về hai cột, cả hai đều có thể chứa dữ liệu chuỗi.
- Điểm chèn là một chuỗi được trích dẫn trong mệnh đề `WHERE`
- Cơ sở dữ liệu chứa một bảng có tên users có các cột `username` và `password`.

Trong ví dụ này, bạn có thể lấy nội dung của bảng `user` bằng cách gửi dữ liệu đầu vào:

```
' UNION SELECT username, password FROM users--
```

Để thực hiện cuộc tấn công này, bạn cần biết rằng có một bảng được gọi là `users` có hai cột được gọi là `username` và `password`. Nếu không có thông tin này, bạn sẽ phải đoán tên của các bảng và cột. Tất cả các cơ sở dữ liệu hiện đại đều cung cấp các cách để kiểm tra cấu trúc cơ sở dữ liệu và xác định chúng chứa những bảng và cột nào.

> Lab: SQL injection UNION attack, retrieving data from other tables

Sau khi kiểm tra bằng câu lệnh `UNION SELECT` tôi biết được kết quả của truy vấn trả về có hai cột

![img23](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PortSwiggers/SQL-Injection/images/image-23.png?raw=true)

Tiếp theo để kiểm tra xem trong database sẽ tồn tại những bảng nào, tôi thực hiện tấn công như sau:

```
'UNION SELECT NULL,table_name FROM information_schema.tables--
```

Và tôi tìm thấy một bảng là bảng `users` đây có thể nơi chứa thông tin người dùng

![img24](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PortSwiggers/SQL-Injection/images/image-24.png?raw=true)

Bây giờ để xem các cột có trong bảng `users` tôi thực hiện tấn công như sau:

```
' UNION SELECT NULL, column_name FROM information_schema.columns WHERE table_name='users'--
```

![img25](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PortSwiggers/SQL-Injection/images/image-25.png?raw=true)

Vậy trong table `users` có 3 cột là `email , username , password`. Tôi không quan tâm đến `email` lắm do đăng nhập chỉ cần `username` và `password`, tôi thực hiện tấn công như sau để lấy thông tin bảng `users`

```
'UNION SELECT username , password FROM users--
```

Từ đây tôi sẽ lấy được hết danh sách `users` bao gồm cả người quản trị

![img26](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PortSwiggers/SQL-Injection/images/image-26.png?raw=true)
