s = "0xc4115 0x4cf8"
## xor c4115 vs 4cf8 => c0ded
flag = "CTFlearn{0xc0ded}"

## code python
print(hex(0xc4115 ^ 0x4cf8)) ## 0xc0ded

