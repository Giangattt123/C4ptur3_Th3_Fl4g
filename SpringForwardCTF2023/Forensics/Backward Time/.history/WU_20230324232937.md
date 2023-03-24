# Solution

Cách dễ nhất tôi tiếp cận với forensics là kéo file vào **notepad** và tìm kiếm format flag nhưng ở đây nó không có giúp ích nhiều..Hmm bài tập đâu có dễ xơi như vậy. Tiếp theo tôi sẽ đọc nội dung của file bằng cậu lệnh strings file_name

![image1](https://live.staticflickr.com/65535/52768734805_71de75035b_b.jpg)

Để ý thấy ở cuối file có phần text ở dạng ascii mà ta có thể đọc được, để rút ngắn bớt nội dung file và không hiển thị phần trên ta dùng thêm đối số **| tail** để hiển thị nội dung cuối file.

![image2](https://live.staticflickr.com/65535/52768578134_c46b045114_h.jpg)

> Phần nổi bật nhất css lẽ là dãy nhị phân biểu diễn dưới dạng đơn bị 8 bit hay một bytes. Đến đây ta dùng tool [kt.gy](https://kt.gy/tools.html#conv/) để chuyển về ascii và sẽ xuất hiện flag.

![image3](https://live.staticflickr.com/65535/52768584664_84f97a4914_h.jpg)

> Flag: **nicc{fa11ing_back_spr1ng_ah3ad}**
