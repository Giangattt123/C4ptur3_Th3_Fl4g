from Crypto.Util.number import *
from gmpy2 import mpz
e = mpz(1)
c = mpz(9327565722767258308650643213344542404592011161659991421)
n = mpz(245841236512478852752909734912575581815967630033049838269083)

## Use factordb => find p , q
p = mpz(416064700201658306196320137931)
q = mpz(590872612825179551336102196593)
phi_n = (p - 1) * (q - 1)
d = inverse(e , phi_n)
plantext = pow(c , d , n)

flag = bytes.fromhex(hex(plantext)[2:])
print(flag)

## Flag: abctf{b3tter_up_y0ur_e}