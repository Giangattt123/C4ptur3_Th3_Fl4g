## Download: pip install z3-solver
"""
z3 là một bộ giải quyết logic mạnh mẽ, có thể được sử dụng để giải các hệ phương trình, bài toán logic và các vấn đề về ràng buộc (constraint problems)
"""
## Example: 6x^2 + 11x - 35 = 0
from z3 import *
s = Solver()
x = Real('x')
y = 6*x**2 + 11*x - 35
# Add constrains
s.add(y == 0) 
# s.add(6*x**2 + 11*x - 35 == 0)  # Also works
if s.check() == sat:  # If satisfiable
    print(s.model())  # [x = 5/3]

# Find all satisfiable
while s.check() == sat:
    m = s.model()
    print(m)
    s.add(x != m[x])

## Variable Type:
"""
1. Int('x') - Số nguyên
2. Real('x') - Số thực
3. Bool('x') - Kiểu bool (True/False)
4. BitVec(name , bits) : Dùng trong các bài toán liên quan đến mã hóa, phân tích và tối ưu các chuỗi bit, hoặc các bài toán tính toán thấp cấp (low-level).
"""


