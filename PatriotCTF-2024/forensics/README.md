# Forensic
## Forensic: Simple Exfiltration

Thử thách cho một file ```pcap``` và một đoạn mô tả có thể dịch như sau:

```
Chúng tôi nhận được một số báo cáo về việc thông tin được gửi ra khỏi mạng lưới của chúng tôi. Bạn có thể đoán được tin nhắn nào đã được gửi đi không?
```

Kiểm tra việc các gói tin gửi đi và nhận về -> ping -> icmp protocol -> `ICMP Tunneling`

Đối với `ICMP Tunneling`, nếu tin nhắn được gửi ra nó sẽ:

- Sử dụng các gói tin `ICMP` để truyền dữ liệu.

- Thường ẩn thông tin trong các gói `ICMP Echo Request` và `Echo Reply`.


Đối với thử thách này, nó được ẩn trong các `ICMP Echo Request`

![img1]()

![img2]()

![img3]()

![img4]()

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

> Flag: pctf{time_to_live_exfiltration}

## Forensic: Bad Blood

Thử thách cho chúng ta một file `evtx(Window Event Log File)` , đây là định dạng tệp nhật ký sự kiện của hệ điều hành Windows. Nó lưu trữ các sự kiện liên quan đến hoạt động của hệ thống, ứng dụng và bảo mật, giúp quản trị viên và người dùng theo dõi các sự kiện quan trọng như lỗi hệ thống, sự cố phần mềm, cảnh báo bảo mật, và các hoạt động khác.

Sử dụng ```Event Viewer``` để mở file ```evtx```

![img5]()

Sau đó connect đến server bằng câu lệnh ```nc chal.competitivecyber.club 10001``` để trả lời các câu hỏi của thử thách

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

## Forensic: 

