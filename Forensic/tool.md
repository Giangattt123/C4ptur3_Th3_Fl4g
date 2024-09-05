# Forensic

## Các tool sử dụng để chơi forensic

### File hình ảnh

- Sử dụng lệnh `file` để biết thông tin về ảnh, định dạng file, dữ liệu

- [AperilSolve](https://www.aperisolve.com/) là một nền tảng trực tuyến thực hiện phân tích lớp trên hình ảnh. Nền tảng này cũng sử dụng `zsteg, steghide, outguess, exiftool, binwalk, priorit`,..

- Để trích xuất dữ liệu bên trong các tập tin hình ảnh

  ```
  zsteg -a <FILE_NAME>
  ```

- Để kiểm tra siêu dữ liệu của các tệp hình ảnh

  ```
  exiftool <FILE_NAME>
  ```

- Để tìm kiếm chuỗi hoặc ``flag``` cụ thể trong tệp hình ảnh.

  `strings <FILE_NAME> | grep flag{`

- Để trích xuất dữ liệu ẩn bên trong tệp hình ảnh được bảo vệ bằng mật khẩu.

  `steghide extract -sf <FILE_NAME>`

- Xác minh tính toàn vẹn của PNG và đổ tất cả thông tin cấp độ khối ở dạng có thể đọc được

  `pngcheck -cvt <FILE_NAME>.png`

### Binwalk

- `Binwalk` giúp tìm dữ liệu bên trong hình ảnh hoặc đôi khi nếu Binwalk báo cáo tệp là một kho lưu trữ `ZIP`, chúng ta có thể đổi tên tệp thành `<FILE_NAME>.zip`

```
    binwalk <IMAGE_NAME>
    binwakl --extract --dd=".*."
```

### File Carving

`File Carving` là một kỹ thuật phục hồi dữ liệu được sử dụng để trích xuất các tệp từ một nguồn dữ liệu như đĩa cứng, hình ảnh đĩa, hoặc bộ nhớ. Quá trình này không dựa trên hệ thống tệp hoặc bảng phân vùng mà thay vào đó tìm kiếm các mẫu dữ liệu đặc trưng của các định dạng tệp trong các khối dữ liệu thô.

Các bước cơ bản của `file carving` bao gồm:

- `Xác định Đầu và Cuối Tệp`: Bằng cách sử dụng các chữ ký `(signature) ` hoặc các đặc điểm nhận dạng khác để phát hiện vị trí bắt đầu và kết thúc của tệp trong dữ liệu thô.

- `Trích Xuất Tệp`: Khi vị trí của tệp được xác định, dữ liệu từ điểm bắt đầu đến điểm kết thúc sẽ được trích xuất và lưu lại như một tệp riêng lẻ.

- `Khôi Phục`: Sau khi trích xuất, các tệp có thể cần được kiểm tra và khôi phục nếu cần thiết để đảm bảo chúng có thể sử dụng được.

> File carving thường được sử dụng trong lĩnh vực điều tra số (digital forensics) khi cần khôi phục dữ liệu từ các ổ đĩa bị hỏng, hình ảnh đĩa, hoặc các thiết bị lưu trữ khác.

- [dd](https://man7.org/linux/man-pages/man1/dd.1.html) Sao chép một tập tin, chuyển đổi và định dạng theo các toán hạng.

- Hãy thử `file carve` bằng lệnh `foremost <filename>`. Trước hết hỗ trợ tất cả các file. Nhưng mất thời gian để trích xuất tất cả các file khi bạn gặp một file có kích thước lớn.

- [HxD](https://mh-nexus.de/en/hxd/) trình soạn thảo hex thân thiện với người dùng cho phép bạn thực hiện chỉnh sửa và sửa đổi cấp thấp của đĩa thô hoặc bộ nhớ chính (RAM)

### Network Analysis

- Được sử dụng để phân tích các tập tin pcap hoặc pcapng

  `wireshark <FILE_NAME>.pcapng`

- [NetworkMiner](https://www.netresec.com/index.ashx?page=NetworkMiner) Công cụ phân tích pháp y mạng được sử dụng như một công cụ đánh hơi mạng thụ động/công cụ bắt gói tin để phát hiện hệ điều hành, phiên, tên máy chủ, cổng mở

- [Aircrack-NG Tool](https://www.aircrack-ng.org/) Crack 802.11 WEP và WPA-PSK keys

  ` sudo apt-get install aircrack-ng`

### USB

- [usbrip](https://github.com/snovvcrash/usbrip) Công cụ pháp y CLI đơn giản để theo dõi các hiện vật của thiết bị USB (lịch sử các sự kiện USB) trên GNU/Linux

### Registry Viewers

- [OfflineRegistry View](https://www.nirsoft.net/utils/offline_registry_view.html#google_vignette) Công cụ đơn giản dành cho Windows cho phép bạn đọc các tệp Registry ngoại tuyến từ ổ đĩa ngoài và xem khóa Registry mong muốn ở định dạng tệp `.reg`.

- [RegistryViewer](https://www.exterro.com/ftk-product-downloads/registry-viewer-2-0-0) Dùng để xem sổ đăng ký Windows

### Extract NTFS Filesystem

```
If there is ntfs file, extract with 7Zip on Windowds.
If there is a file with alternative data strems, we can use the command `dir /R <FILE_NAME>`.
Then we can this command to extract data inside it `cat <HIDDEN_STREAM> > asdf.<FILE_TYPE>`
```

Để trích xuất hệ thống tập tin ntfs trên Linux

```
sudo mount -o loop <FILENAME.ntfs> mnt
```

### Recover Files from Deleted File Systems

Để khôi phục tập tin từ hệ thống tập tin đã xóa khỏi máy chủ từ xa.

```
> $ ssh username@remote_address "sudo dcfldd -if=/dev/sdb | gzip -1 ." | dcfldd of=extract.dd.gz
> $ gunzip -d extract.dd.gz
> $ binwalk -Me extract.dd
```

### Memory Forensics

Công cụ điều tra để dump bộ nhớ

- [volatility](https://github.com/volatilityfoundation/volatility) extraction of digital artifacts from volatile memory (RAM) samples

- [WindowsSCOPE](https://www.windowsscope.com/) cho phép giám định bộ nhớ cho máy tính Windows

### Audio forensics

Để trích xuất dữ liệu từ tệp âm thanh

- [Audacity](https://sourceforge.net/projects/audacity/) kiểm tra tính toàn vẹn, cải thiện độ rõ ràng của giọng nói, phiên âm hội thoại

### Zip Password Cracking

Để trích xuất mật khẩu `ZIP`, hãy sử dụng công cụ `fcrackzip` HOẶC `zip2john`

```
> $ zip2john <File-Name>.zip > <Name>.txt

> $ john <Name>.txt --wordlist=/usr/share/wordlists/rockyou.txt
```

### Pdf Password Cracking

Để trích xuất mật khẩu `PDF`, hãy sử dụng công cụ `pdf2john`

```
> $ pdf2john <File-Name>.pdf > <Name>.txt

> $ john <Name>.txt --wordlist=/usr/share/wordlists/rockyou.txt
```

### 7z Password Cracking

Để trích xuất mật khẩu `7z`, hãy sử dụng công cụ `7z2john`

```
> $ 7z2john <File-Name>.7z > <Name>.7z

> $ john id_rsa.txt --wordlist=/usr/share/wordlists/rockyou.txt
```

### SSH Password Cracking

Để bẻ khóa `ssh` được mã hóa hãy sử dụng công cụ `ssh2john`

```
> $ ssh2john id_rsa > id_rsa.txt

> $ john id_rsa.txt --wordlist=/usr/share/wordlists/rockyou.txt

> $ ssh -i id_rsa <Username>@<IP-Address>
   :Enter the Password Cracked
```
