from Crypto.Util.number import *
import random
def gen_prime_rsa_p(nbits,e):
    while True:
        p = getPrime(nbits)
        if (p-1) % e == 0 and (p-1) % e**2 != 0:
            return p 

def gen_prime_rsa_q_z(nbits,e):
    while True:
        q = getPrime(nbits)
        if (q-1) % e != 0:
            return q 


flag = b"flag{???????????????????}"

e = 71
nbits = 64
p = gen_prime_rsa_p(256,e)
q = gen_prime_rsa_q_z(256,e)
z = gen_prime_rsa_q_z(256,e)
N = p * q * z
cipher = pow(bytes_to_long(flag), e, N)
x_random = []
x_result = []
for i in range(16):
    x = random.getrandbits(nbits)
    x_random.append(x)
    r = (q * x + z) % p  + random.randint(-2**32 + 1, 2**32)
    x_result.append(r)


print(x_random)
print(x_result)
print(f"p = {p}")
print(f"e = {e}")
print(f"C = {cipher}")

        
