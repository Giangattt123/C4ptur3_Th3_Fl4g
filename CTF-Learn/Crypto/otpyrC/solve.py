s : str = "d733432373937303734373666343730373937323733343b7644534"
sRev = s[::-1]
flag = ''.join([chr(int(sRev[i:i+2], 16)) for i in range(0, len(sRev), 2)])
print(flag)

## flag: CTF{43727970746f7470797243}