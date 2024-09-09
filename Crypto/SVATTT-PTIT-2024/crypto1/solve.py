import string
import random

flag = "flag{"
    
def generate_key():
    return [random.randint(0, 94) for _ in range(4)]
    
def encrypted(key,flag) :
    data = [printable.index(i) for i in flag]
    encrypted = ''
    for i in range(len(flag)) :
        encrypted += words[(data[i] + key[i%4]) % 94]
    return encrypted

_seed = None
for seed in range(65538):
    words =r"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    random.seed(seed)
    printable_characters = list(r"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~")
    printable = ''
    for i in range(len(printable_characters)) :
        chosen_char = random.choice(printable_characters)
        if chosen_char != ' ' : 
            printable += chosen_char
            printable_characters.remove(chosen_char)

    key = generate_key()
    ct = encrypted(key,flag)
    if ct.startswith('3u?Zs'):
        _seed = seed

print(f"seed: %s" %_seed)
random.seed(_seed)

printable_characters = list(r"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~")
printable = ''
for i in range(len(printable_characters)) :
    chosen_char = random.choice(printable_characters)
    if chosen_char != ' ' : 
        printable += chosen_char
        printable_characters.remove(chosen_char)

key = generate_key()

words =r"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"

ct = "3u?Zs5M>vY`06DB0EE\>vE%(Wf&XAW&-T[-0vD_K"
flag = ''
for i in range(len(ct)) :
    for w in words:
        test = flag + w 
        _ct = encrypted(key,test)
        if ct.startswith(_ct):
            flag += w
            print(flag)