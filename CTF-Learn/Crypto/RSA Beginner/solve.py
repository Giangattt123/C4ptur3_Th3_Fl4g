from Crypto.Util.number import *
from gmpy2 import mpz
e = mpz(3)
c = mpz(219878849218803628752496734037301843801487889344508611639028)
n = mpz(245841236512478852752909734912575581815967630033049838269083)

## Use factordb => find p , q
p = mpz(416064700201658306196320137931)
q = mpz(590872612825179551336102196593)
phi_n = (p - 1) * (q - 1)
d = inverse(e , phi_n)
plantext = pow(c , d , n)

flag = bytes.fromhex(hex(plantext)[2:])
print(flag)

## Flag: abctf{rs4_is_aw3s0m3}