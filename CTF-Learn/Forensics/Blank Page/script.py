file = open("TheMessage.txt", "r" , encoding="utf-8").read()
ans = ""
for char in file:
	if char == ' ':
		ans += "0"
	else:
		ans += "1"
print(ans)