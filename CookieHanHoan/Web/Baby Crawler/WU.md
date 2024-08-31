Đây là một trang web crawl data
Truy cập vào `path/?debug` sẽ thấy logic xử lí của nó

```
$result = shell_exec('curl '. escapeshellcmd($url));
     $cache_file = './cache/'.md5($url);
     file_put_contents($cache_file, $result);
     $data = parse_html($cache_file);
```

> Vậy website này sẽ crawl web bằng lệnh `curl`, sau đó lưu file vừa `crawl` được vào một file nằm trong thư mục `./cache`.

> Sử dụng `curl` gửi file crawl được đến một `webhook` với param `-F`

![img1]()

Kiểm tra bên `webhook`

![img2]()

> Flag:
