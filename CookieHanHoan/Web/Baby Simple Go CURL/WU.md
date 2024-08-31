Bài này thuộc chủ đề lỗ hổng web SSRF, có thể nói SSRF như sau:

> Server Side Request Forgery or SSRF is a vulnerability in which an attacker forces a server to perform requests on their behalf.

Giao diện trang web trông như sau:

![img1](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/CookieHanHoan/Web/Baby%20Simple%20Go%20CURL/images/1.png?raw=true)

Nó cho chúng ta 3 trường input để nhập vào, 1 trường có thể hiểu nó fetch đến `url` cần thiết, 1 trường `header-key`, 1 trường `header-value`, đối với lỗ hổng SSRF thì thông thường sẽ thuộc loại `bypass with localhost`

Tất nhiên server sẽ không lấy ip của nó mà sử dụng ip của docker engine để giao tiếp với bên thứ ba

Do gợi ý nó nói flag nằm ở `/flag` nên tôi sẽ test như sau:

![img2](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/CookieHanHoan/Web/Baby%20Simple%20Go%20CURL/images/2.png?raw=true)

Có thể ở response nó đã nằm ở một thẻ `a` với các param lần lượt là `url` , `header-key` , `header-value` đúng như ta dự đoán nhưng bị báo `Moved Permanently`

Hmm tôi chợt nhận ra có lẽ phần header-key và header-value sẽ phải truyền vào header nào đó để nói với máy chủ web là mình đang dùng ip là `127.0.0.1`

> Vì vậy tôi nghĩ đến `X-Forwarded-For` với value header là `127.0.0.1`

Tôi thử lại nhưng cũng vẫn vậy

Tôi nghĩ mình còn thiếu port do nếu chỉ truyền như vậy ở `url` thì mặc định nó sẽ chạy port 80, do được `build` bởi `docker` nên tôi kiểm tra `Dockerfile` và biết được rằng container đang lắng nghe ở port `1337`

![img3](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/CookieHanHoan/Web/Baby%20Simple%20Go%20CURL/images/3.png?raw=true)

Nhưng một lần nữa nó cũng không khả quan cho lắm

![img4](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/CookieHanHoan/Web/Baby%20Simple%20Go%20CURL/images/4.png?raw=true)

Đến đây tôi bắt đầu bí hướng tiếp theo, nhưng ở `tag` có gợi ý đến command `curl`, tôi bắt đầu suy nghĩ có lẽ các `param` như `header-key` và `header-value` thực sự không được đẩy vào `http header`, vì vậy tôi sử dụng curl và tôi đã đúng

> curl "http://103.97.125.56:32217/curl/?url=http://127.0.0.1:1337/flag&header_key=admin&header_value=admin" -H "X-Forwarded-For: 127.0.0.1"

![img5](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/CookieHanHoan/Web/Baby%20Simple%20Go%20CURL/images/5.png?raw=true)

> Flag: CHH{Serv3r_S1De_R3qu3s7_G0_cuRL_a8a8d9a3e5a33f0a67fe3490aac41890}
