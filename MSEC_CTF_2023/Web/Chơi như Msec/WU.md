# Solution

Mở url challenge lên ta được một trang web với bản nhạc và dòng thông báo `Bạn không phải Admin` đây cũng là một gợi ý mở ra hướng làm bài này.

![image1](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/MSEC_CTF_2023/Web/Ch%C6%A1i%20nh%C6%B0%20Msec/images/image1.jpg)

Trước khi nghĩ đến làm như nào, tôi sẽ tiến hành **recon** trang web ở đây tôi sử dụng **dirsearch**

![image2](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/MSEC_CTF_2023/Web/Ch%C6%A1i%20nh%C6%B0%20Msec/images/image2.jpg)

Ta tìm thấy một **directory hidden** là **/backup**. Truy cập vào đường dẫn đó, ta sẽ nhìn thấy một file **public.pem**. Tôi sẽ download nó bằng wget command và đọc xem nội dung của nó là gì bằng lệnh cat.

![image3](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/MSEC_CTF_2023/Web/Ch%C6%A1i%20nh%C6%B0%20Msec/images/image3.jpg)

![image4](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/MSEC_CTF_2023/Web/Ch%C6%A1i%20nh%C6%B0%20Msec/images/image4.jpg)

![image5](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/MSEC_CTF_2023/Web/Ch%C6%A1i%20nh%C6%B0%20Msec/images/image5.jpg)

Nó có vẻ là một **public key** được sử dụng với mục đích làm gì thì tôi chưa biết =: 🙃

Tôi đọc source code cũng không có điểm gì có thể khai thác, nhớ đến gợi ý của bài rằng mình không phải `Admin` nên tôi nghĩ đến việc kiểm tra cookie và tìm thấy một token còn ở lại trình duyệt.

![image6](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/MSEC_CTF_2023/Web/Ch%C6%A1i%20nh%C6%B0%20Msec/images/image6.jpg)

> Tôi nghĩ đến việc rằng mình sẽ tìm `value` của admin để trang web nhận dạng được và mình có thể đang đứng ở trang web với vai trò là `Admin`

Trước tiên tôi lấy giá trị của **token** và tiến hành decode. Sử dụng trang web ![jwt.io](https://jwt.io/)

![image7](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/MSEC_CTF_2023/Web/Ch%C6%A1i%20nh%C6%B0%20Msec/images/image7.jpg)

Bây giờ chúng ta cần thay đổi **username** từ `Vera` thành `Admin` bằng cách sử dụng public.pem ở trên vừa tìm được. Ở đây type là **JWT** và alg là **RS256** và có file là public.pem, ta sẽ sử dụng tool [tool](https://github.com/3v4Si0N/RS256-2-HS256) để làm điều này. Chúng ta thực hiện như sau:

![image8](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/MSEC_CTF_2023/Web/Ch%C6%A1i%20nh%C6%B0%20Msec/images/image8.jpg)

![image9](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/MSEC_CTF_2023/Web/Ch%C6%A1i%20nh%C6%B0%20Msec/images/image9.jpg)

Bây giờ ta sử dụng token vừa tìm được để hoán đổi vai trò trở thành `Admin` để lấy flag. Các bạn có thể tahy trực tiếp trên trình duyệt và tiến hành refresh, ở đây tôi sử dụng `Curl` **command**

![image10](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/MSEC_CTF_2023/Web/Ch%C6%A1i%20nh%C6%B0%20Msec/images/image10.jpg)

![image11](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/MSEC_CTF_2023/Web/Ch%C6%A1i%20nh%C6%B0%20Msec/images/image11.jpg)

> Flag: MSEC{ms3c_q0t_4_b4nq_n0_c4p}
