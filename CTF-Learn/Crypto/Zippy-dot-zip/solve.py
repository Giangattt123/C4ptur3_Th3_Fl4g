data = """
flag00.zip / flag00 : 'CTFl'
flag01.zip / flag01 : 'earn'
flag02.zip / flag02 : '{s0m'
flag03.zip / flag03 : '3t1m'
flag04.zip / flag04 : '35_u'
flag05.zip / flag05 : '$1ng'
flag06.zip / flag06 : '_h4r'
flag07.zip / flag07 : 'd_p4'
flag08.zip / flag08 : 's5w0'
flag09.zip / flag09 : 'rd_i'
flag10.zip / flag10 : '5_n0'
flag11.zip / flag11 : 't_3n'
flag12.zip / flag12 : '0ugh'
flag13.zip / flag13 : '}'
"""

lines = data.strip().split('\n')
flag = ""
for line in lines:
    arrLine = line.split(" : ")
    print(arrLine)
    flag += arrLine[1][1:-1]
print(flag)