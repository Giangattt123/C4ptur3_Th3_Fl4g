import string
import random

with open("flag.txt", "r") as f:
    flag = f.read().strip()
    
def generate_key():
    return [random.randint(0, 94) for _ in range(4)]
    
def encrypted(key,flag) :
    data = [printable.index(i) for i in flag]
    encrypted = ''
    for i in range(len(flag)) :
        encrypted += words[(data[i] + key[i%4]) % 94]
    return encrypted
    
words =r"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
random.seed(random.randrange(0,65537))
printable_characters = list(r"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~")
printable = ''
for i in range(len(printable_characters)) :
    chosen_char = random.choice(printable_characters)
    if chosen_char != ' ' : 
      printable += chosen_char
      printable_characters.remove(chosen_char)

key = generate_key()
ct = encrypted(key,flag)
print(ct)
