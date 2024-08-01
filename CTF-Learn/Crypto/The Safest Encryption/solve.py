from pwn import xor
with open('CTFLearn.pdf', 'rb') as file1, open('CTFLearn.txt', 'rb') as file2:
    var1 = file1.read()
    var2 = file2.read()
    flag = xor(var1, var2)
    with open('result', 'wb') as result:
        result.write(flag)
## flag: CTFlearn{CTFlearn_is_fun_hope_you_enjoyed_it!}
