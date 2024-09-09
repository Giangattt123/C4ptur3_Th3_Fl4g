from Crypto.Util.number import *
import random
import os

with open("flag.txt", "r") as f:
    flag = f.read().strip()
    
def encrypt(key):      
    flag=bytes_to_long(flag.encode())
    c= ((flag^key)<<256)
    return c

def secret():
    n= getStrongPrime(512)
    a,b,c= getStrongPrime(512),getStrongPrime(512),getStrongPrime(512)
    w=pow(2,512)+pow(2,255)-pow(2,256) 
    A=pow(2,a,n)
    B=pow(2,b,n)
    key=pow(B,a,n)
    r1=key&w
    C=pow(2,a+c,n)  
    r2=pow(C,b,n)
    
    return n,A,B,c,C,r1,r2,key

n,A,B,c,C,r1,r2,key=secret()
cipher=encrypt(key)
print(f"{n=}")
print(f"{A=}")
print(f"{B=}")
print(f"{c=}")
print(f"{C=}")
print(f"{r1=}")
print(f"{r2=}")
print(f"{cipher=}")



    

