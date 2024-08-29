## Writeup

- Đề bài tiếp tục cho 1 file pcap, ném file vào `wireshark` và tiến hành phân tích

- Có thể thấy các file đã được `curl` ở các object list. Ở đây có 2 file rất nghi ngờ là `flag.txt` và `pcap.exe` là 2 file được curl đến ip có port 1234

![img4](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PTIT-CTF-2024/VL/images/image-4.png?raw=true)

- Lưu 2 file đó về , đọc thử file `flag.txt` và không có flag

![img5](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PTIT-CTF-2024/VL/images/image-5.png?raw=true)

- Tiến hành phân tích file `pcap.exe` còn lại. Chạy thử file `pcap.exe` này

![img6](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PTIT-CTF-2024/VL/images/image-6.png?raw=true)

> Hiểu đơn giản mình sẽ được nhập 1 chuỗi và sau đó sẽ tiến hành kiểm tra chuỗi nhập vào có đúng hay không. Ở đây nhập bừa chuỗi **hihi** và hiện thông báo **Wrong!**. Tiến hành reverse file .exe này

```
int __fastcall main(int argc, const char **argv, const char **envp)
{
  FILE *v3; // rax
  char Buffer[112]; // [rsp+20h] [rbp-60h] BYREF
  int v6[34]; // [rsp+90h] [rbp+10h]
  int v7; // [rsp+118h] [rbp+98h]
  int i; // [rsp+11Ch] [rbp+9Ch]

  _main();
  v6[0] = 53;
  v6[1] = 57;
  v6[2] = 46;
  v6[3] = 57;
  v6[4] = 40;
  v6[5] = 57;
  v6[6] = 43;
  v6[7] = 96;
  v6[8] = 24;
  v6[9] = 93;
  v6[10] = 85;
  v6[11] = 21;
  v6[12] = 87;
  v6[13] = 89;
  v6[14] = 68;
  v6[15] = 43;
  v6[16] = 22;
  v6[17] = 81;
  v6[18] = 24;
  v6[19] = 68;
  v6[20] = 43;
  v6[21] = 87;
  v6[22] = 21;
  v6[23] = 82;
  v6[24] = 68;
  v6[25] = 85;
  v6[26] = 72;
  v6[27] = 25;
  v6[28] = 85;
  v6[29] = 9;
  v6[30] = 98;
  v7 = 31;
  printf("Nhap vao mot chuoi: ");
  v3 = __iob_func();
  fgets(Buffer, 100, v3);
  Buffer[strcspn(Buffer, "\n")] = 0;
  if ( strlen(Buffer) == v7 )
  {
    for ( i = 0; i < v7; ++i )
    {
      if ( Buffer[i] - 27 != v6[i] )
        goto LABEL_2;
    }
    puts("Correct!");
    return 0;
  }
  else
  {
LABEL_2:
    puts("Wrong!");
    return 0;
  }
}
```

- Đoạn mã này là một chương trình C đơn giản thực hiện kiểm tra chuỗi nhập vào và so sánh với một chuỗi được mã hóa sẵn. Code của chương trình có thể hiểu là chuỗi ta nhập vào được gán cho `Buffer`

- Biến `v7` được gán giá trị là 31 để kiểm tra độ dài của chuỗi nhập vào. Nếu độ dài của chuỗi nhập vào bằng giá trị `v7` thì nó sẽ thực hiện lấy các kí tự của `Buffer` `-27` và so sánh giá trị của mảng `v6` ở vị trí tương ứng.

> Lấy mảng v6 cộng ngược lại với `27` để tìm ra flag

- Solve

```
#!usr/bin/env python

v6 = [0] * 31
v6[0] = 53
v6[1] = 57
v6[2] = 46
v6[3] = 57
v6[4] = 40
v6[5] = 57
v6[6] = 43
v6[7] = 96
v6[8] = 24
v6[9] = 93
v6[10] = 85
v6[11] = 21
v6[12] = 87
v6[13] = 89
v6[14] = 68
v6[15] = 43
v6[16] = 22
v6[17] = 81
v6[18] = 24
v6[19] = 68
v6[20] = 43
v6[21] = 87
v6[22] = 21
v6[23] = 82
v6[24] = 68
v6[25] = 85
v6[26] = 72
v6[27] = 25
v6[28] = 85
v6[29] = 9
v6[30] = 98

flag : str = ""
for i in range(31):
	flag += chr(v6[i] + 27)
print(flag)
```

> Flag: PTITCTF{3xp0rt_F1l3_Fr0m_pc4p$}
