## Trick

- Đối với những bài lồng thư mục cần trích xuất 1 chuỗi `base`

  ` strings -a * | grep -E "\b\w{50,}\b"`

- Đối với những bài tìm chuỗi `base64` từ file hình ảnh

  `grep -a -oE '[A-Za-z0-9+/]{10,}={0,2}' <file-name>.png | base64 -d`

- Nhảy đến cuối file khi phân tích file bằng trình soạn thảo `hex`

  `xxd <file-name> | less -> G`
