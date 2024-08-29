from math import isqrt
from Crypto.Util.number import long_to_bytes , bytes_to_long
from sympy import factorint
from itertools import combinations

k = 6258410170491540915473187363385860218516146631238930775881603281781457715136165605511975000939331837790447577832384830476708724833318777335448868185507771522354089984

sqrt_k = 2 * isqrt(k)

factors = factorint(sqrt_k)
factor_list = []
first : str = ""
for factor, exponent in factors.items():
    for _ in range(exponent):
        factor_list.append(factor)

found = False
for i in range(1, len(factor_list) + 1):
    for comb in combinations(factor_list, i):
        num = 1
        for factor in comb:
            num *= factor
        x = num - 1
        y = (sqrt_k // num) - 1

        s = long_to_bytes(x).decode(errors='ignore')
        s1 = long_to_bytes(y).decode(errors='ignore')

        if "PTITCTF" in s:
            print("Found in x:", s)
            first = s
            found = True
            break
        if "PTITCTF" in s1:
            print("Found in y:", s1)
            first = s1
            found = True
            break
    if found:
        break

print(first)

known_num = bytes_to_long(first.encode())

remainder = sqrt_k // (known_num + 1) + 1

last = long_to_bytes(remainder).decode(errors='ignore')

full_flag = first + last
print("Full flag:", full_flag)


## PTITCTF{Y0u_Kn0w_
## Full flag: PTITCTF{Y0u_Kn0w_Br3ak_EqUa7I0nS!!}