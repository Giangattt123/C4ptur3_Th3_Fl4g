# Forensic

## Forensic: Simple Exfiltration

Thử thách cho một file `pcap` và một đoạn mô tả có thể dịch như sau:

```
Chúng tôi nhận được một số báo cáo về việc thông tin được gửi ra khỏi mạng lưới của chúng tôi. Bạn có thể đoán được tin nhắn nào đã được gửi đi không?
```

Kiểm tra việc các gói tin gửi đi và nhận về -> ping -> icmp protocol -> `ICMP Tunneling`

Đối với `ICMP Tunneling`, nếu tin nhắn được gửi ra nó sẽ:

- Sử dụng các gói tin `ICMP` để truyền dữ liệu.

- Thường ẩn thông tin trong các gói `ICMP Echo Request` và `Echo Reply`.

Đối với thử thách này, nó được ẩn trong các `ICMP Echo Request`

![img1](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PatriotCTF-2024/forensics/images/image-01.png?raw=true)

![img2](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PatriotCTF-2024/forensics/images/image-02.png?raw=true)

![img3](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PatriotCTF-2024/forensics/images/image-03.png?raw=true)

![img4](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PatriotCTF-2024/forensics/images/image-04.png?raw=true)

Lần lượt ta thu được là `pctf` đúng với định dạng `flag`(
Chú ý là các kí tự flag được lấy từ trường Time To Live(ttl) của gói tin). Tôi sẽ viết 1 `script` python sử dụng thư viện `Scapy` như sau:

```
from scapy.all import rdpcap, ICMP, IP

pcap_file = "exfiltration_activity_pctf_challenge.pcapng"
packets = rdpcap(pcap_file)

arr = []
for packet in packets:
    if IP in packet and ICMP in packet and packet[ICMP].type == 8:
        arr.append(packet[IP].ttl)

print(arr)
flag : str = "".join(chr(val) for val in arr)
print(flag)
```

![img15]()

> Flag: pctf{time_to_live_exfiltration}

## Forensic: Bad Blood

Thử thách cho chúng ta một file `evtx(Window Event Log File)` , đây là định dạng tệp nhật ký sự kiện của hệ điều hành Windows. Nó lưu trữ các sự kiện liên quan đến hoạt động của hệ thống, ứng dụng và bảo mật, giúp quản trị viên và người dùng theo dõi các sự kiện quan trọng như lỗi hệ thống, sự cố phần mềm, cảnh báo bảo mật, và các hoạt động khác.

Sử dụng `Event Viewer` để mở file `evtx`

![img5](https://github.com/Giangattt123/C4ptur3_Th3_Fl4g/blob/master/PatriotCTF-2024/forensics/images/image-05.png?raw=true)

Sau đó connect đến server bằng câu lệnh `nc chal.competitivecyber.club 10001` để trả lời các câu hỏi của thử thách

![img6]()

Câu hỏi liên quan đến kẻ tấn công đã chạy tập lệnh nào để khai thác câu lệnh -> event id `4104`

![img7]()

> Invoke-P0wnedshell.ps1

Câu hỏi thứ hai thì có vẻ như Jack đã sử dụng kỹ thuật process injection (tiêm vào tiến trình) để che giấu các hoạt động độc hại của mình, khiến các công cụ kiểm tra không phát hiện được tiến trình nào bất thường. Tuy nhiên, lưu lượng mạng cho thấy đã có một kết nối từ hệ thống của Jack tới một thiết bị bên ngoài mạng nội bộ, và điều này cho thấy rằng Jack có thể đã dùng process injection để thực hiện hành vi này.

> Invoke-UrbanBishop.ps1

![img10]()

![img11]()

> WinRM

![img12]()

> Flag: pctf{3v3nt_l0gs_reve4l_al1_a981eb}

## Forensic: A Dire Situation

Thử thách cho ta một file `.wim`. Đây là một file hình ảnh của `Windows Imaging Format`. Đây là một định dạng `file` được sử dụng để lưu trữ một hoặc nhiều hình ảnh của hệ thống `Windows`, bao gồm cả hệ điều hành, ứng dụng, và các tệp dữ liệu khác. Các file `.wim` thường được sử dụng trong các tình huống như:

- Cài đặt Hệ điều hành: File `.wim` có thể chứa hình ảnh cài đặt của hệ điều hành Windows, cho phép cài đặt hệ điều hành trên nhiều máy tính khác nhau.

- Sao lưu và Phục hồi: Bạn có thể sử dụng file `.wim` để sao lưu và phục hồi hệ thống, giúp dễ dàng khôi phục lại trạng thái trước đó.

- Triển khai Hệ thống: Trong các môi trường doanh nghiệp, file `.wim` thường được sử dụng để triển khai hàng loạt hệ thống, cho phép cài đặt đồng nhất trên nhiều máy tính.

Công cụ để làm việc với file `.wim`:

- `DISM` (Deployment Image Servicing and Management): Một công cụ dòng lệnh của Windows cho phép bạn quản lý và thao tác với file `.wim.` -` Windows System Image Manager (WSIM)`: Dùng để tạo và chỉnh sửa file .wim.
- `7-Zip`: Bạn có thể sử dụng phần mềm này để giải nén file `.wim` như một file nén thông thường.

Ở đây tôi sử dụng `7-Zip` để giải nén file `.wim`, sau khi `extract` tôi được một file cùng tên với nội dung

```
Can someone please help me budget? My family is dying.

Rent: $750
Insurance: $100
Streaming: $5000
Food: $200
```

Trong file có nói đến `streaming` và bên cạnh là 1 con số, tôi không quan tâm đến các con số này nhưng `streaming` giúp tôi gợi ý về `ADS (Alternate Data Stream)` - là một tính năng của hệ thống tập tin `NTFS (New Technology File System)` trên Windows, cho phép lưu trữ dữ liệu bổ sung dưới dạng các `stream` ẩn đằng sau file chính. Điều này có nghĩa là ngoài nội dung chính của một file, có thể có thêm các luồng dữ liệu phụ được gắn kèm mà không hiển thị khi mở hoặc xem file theo cách thông thường.

Tiếp theo tôi sử dụng cmd để trích xuất tất cả các `ADS` bằng câu lệnh `dir /R`(lưu ý câu lệnh này sẽ không chạy được trên `powershell`)

```
cd "C:\Users\Admin\OneDrive - ptit.edu.vn\Progaming Course\GIT\C4ptur3_Th3_Fl4g\PatriotCTF-2024\forensics\A Dire Situation"

dir /R
```

![img14]()

Chúng ta đã tìm thấy hai `Alternate Data Streams (ADS)` liên quan đến file `budget`:

- `budget:streamingjpegjfif:$DATA` - Đây là ADS chứa dữ liệu quan trọng (kích thước 121,151 bytes)
- `budget:Zone.Identifier:$DATA` - Đây là ADS hệ thống, được sử dụng để lưu thông tin bảo mật về nguồn gốc file (thường là do file được tải từ internet).

Bây giờ, cần trích xuất dữ liệu từ `ADS budget:streamingjpegjfif`, tôi chạy hai câu lệnh sau:

```
$output = Get-Content .\budget:streamingjpegjfif -Encoding Byte -ReadCount 0
Set-Content .\streaming -Encoding Byte -Value $output
```

![image15]()

Đầu ra sẽ là file `streaming`, với gợi ý là `streamingjpegjfif` ta biết được đây là file `jpeg`, tôi sử dụng `HxD` để chỉnh sửa `header` của file là
`FF D8 FF E0 00 10 4A 46
49 46 00 01
`

![imag16]()

Bây giờ kiểm tra định dạng file và đọc `flag`

![image17]()

> Flag: PCTF{alternate\*d4t4*str3aming*&\_chill}
