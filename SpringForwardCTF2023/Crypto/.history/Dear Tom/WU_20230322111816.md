# Solution

Đây là mã hóa Vigenere, chúng ta không có bất kì gợi ý nào về mã hóa này, nhưng ta có thể đoán được bởi tấm ảnh cho trong thử thách với dòng **"TIME"** được in đậm , đó rất có thể là **key**

> Đây là một thuật toán mã hóa tương tự như **"Caesar"** nhưng thay vì dịch chuyển các kí tự của bãn rõ theo một khoảng k không đổi thì với **"Vigenere"** ta sẽ dịch chuyển khoảng cách các kí tự của bản rõ với các kí tự của **"KEY"** tương ứng, nếu trong trường hợp độ dài của bản rõ lớn hơn key, ta chỉ cần viết lặp lại các kí tự của key đến khi nào mà độ dài của key bằng với độ dài của bản rõ.
> Trước tiên ta cần nói về thuật toán xây dựng từ plain_text sang cipher_text với **Vigenere_Cipher** , rất đơn giản với mỗi kí tự trong bản mã, ta tiến hành cộng với kí tự tương ứng trong **key** ở đây dạng number của kí tự là chỉ số trong bảng alphabet[alphabet](https://anhnguathena.vn/bang-chu-cai-tieng-anh-chuan-nhat-id774), lấy tổng tương ứng **modular** cho 26 là ra được chỉ số của kí tự tương ứng trong bản cipher_text, nghe có vẻ khó hiểu nhể, ta cùng nhau lấy ví dụ nhé:

```
    Plain_text : HI
    Key : BC
    Plain_text[0] + Key[0] = 7 + 1 = 8 % 26 = 8 => Cipher_text[0] = I
    Plain_text[1] + Key[1] = 8 + 2 = 10 % 26 = 10 => Cipher_text[1] = K
    => Ciphertext : IK
```

Các bạn có thể đọc thêm về nó ở [Vigenere_Cipher](https://vi.wikipedia.org/wiki/M%E1%BA%ADt_m%C3%A3_Vigen%C3%A8re#C%C3%A1ch_gi%E1%BA%A3i_m%C3%A3_Vigen%C3%A8re)

> Ở đây chúng ta phải phân biệt rõ là đoạn text mà challenge đưa ra đang là bản cipher_text, vì vậy cần đưa ra thuật toán truy ngược lại tìm bản plain_text, điều đó rất đơn giản, bạn có thể làm tay hoặc viết code nếu muốn ở đây mình sẽ dùng **tool** cho nhanh nhé:)))...

![Flag](https://live.staticflickr.com/65535/52763802250_d3a610c4d2_z.jpg)
Flag : **nicc{see_you_in_the_future}**
