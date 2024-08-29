## Writeup

- Đề bài cho 1 file pcap , phân tích gói tin bằng `Wireshark` thấy 1 gói tin số 196 đến từ giao diện mạng `Ethernet`

![img1](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PTIT-CTF-2024/VL/images/image-1.png?raw=true)

- Đọc nội dung của gói tin ra thấy 1 đoạn mã base có thể là `flag`

![img2](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PTIT-CTF-2024/VL/images/image-2.png?raw=true)

- Copy đoạn mã base `KBKESVCDKRDHWYTBMJ4XO2LSMVRGCYTZONUGC4TLNNVWW7I=`
  đưa vào `basecrack` tool để xác định loại mã base và xem được giải mã

![img3](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PTIT-CTF-2024/VL/images/image-3.png?raw=true)

> Flag: PTITCTF{babywirebabysharkkkk}
