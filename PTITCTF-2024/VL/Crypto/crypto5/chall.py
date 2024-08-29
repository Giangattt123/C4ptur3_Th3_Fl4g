from Crypto.Util.number import *
from secret import flag, p, q, e, d
from hashlib import *
import random

assert f'PTITCTF{{{md5(str(p).encode()).hexdigest()}}}' == flag
assert isPrime(p), isPrime(q)
assert p.bit_length() == 1024, q.bit_length() == 1024
assert hex(e) == '0x10001'

_k = random.getrandbits(400)

ri1, ri2, ri3 = getPrime(20), getPrime(20), getPrime(10)

_dop, _doq = d % (p - 1), d % (q - 1)
Sp, Sq = pow(_k + getPrime(10), _dop, ri1 * p), pow(_k, _doq, ri2 * q)
s1, s2 = pow(_k, _dop % (ri1 - 1), ri1), pow(_k, _doq % (ri2 - 1), ri2)
_sum = Sq + (q * ri2) * (int(inverse(q * ri2, p * ri1)) * (Sp - Sq) % (p * ri1))
c1, c2 = (_sum - s1 + 1) % ri1, (_sum - s2 + 1) % ri2
gamma = (ri3 * c1 + (2 ** 10 - ri3) * c2) // (2 ** 10)
sm = pow(_sum, gamma, p * q)

with open('bin', 'w') as f:
    f.write(''.join(format(ord(c), '08b') for c in hex(_k)) + '\n')
    f.write(''.join(format(ord(c), '08b') for c in hex(p * q)) + '\n')
    f.write(''.join(format(ord(c), '08b') for c in hex(_sum)) + '\n')
    f.write(''.join(format(ord(c), '08b') for c in hex(sm)) + '\n')
    f.close()