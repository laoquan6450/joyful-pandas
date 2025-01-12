#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：一个整数，它加上100后是一个完全平方数，再加上168又是一个完全平方数，请问该数是多少？

程序分析：
1. 假设该数为 x
2. 则：x + 100 = n², x + 100 + 168 = m² (n,m为某些整数)
3. 设：m² - n² = 168
4. 计算n²的值，从而求出x的值
"""

# import math

# from numpy import isin

# def find_number():
#     k = [] # 存储符合条件的数
#     for i in range(1, 100000):
#         # 假设x + 100 = n²
#         n2 = i * i
#         x = n2 - 100
#         # 检查x + 268是否为完全平方数
#         m2 = x + 268
#         m = int(math.sqrt(m2))
#         if m * m == m2:
#             k.append(x)
#     return k if k else None

# if __name__ == '__main__':
#     result = find_number()
#     if result is not None:
#         print(f"符合条件的数是：{result}")
#         # 验证结果
#         for i in result:
#             print(f"验证{i}:")
#             print(f"{i} + 100 = {i + 100} = {int(math.sqrt(i + 100))}²")
#             print(f"{i} + 268 = {i + 268} = {int(math.sqrt(i + 268))}²")
#     else:
#         print("未找到符合条件的数") 




# 方法二：

# 导入math库以使用sqrt函数
import math

def find_integer():
    # 找到所有满足 (m - n)(m + n) = 168 的整数对 (m, n)
    factors = [(i, 168 // i) for i in range(1, int(math.sqrt(168)) + 1) if 168 % i == 0]
    possible_x_values = set()
    
    for a, b in factors:
        # 解方程组 m - n = a, m + n = b
        m = (a + b) / 2
        n = (b - a) / 2
        
        # 检查 m 和 n 是否为整数
        if m.is_integer() and n.is_integer():  #is_integer()是判断是否为整数
        # if isinstance(m,int) and isinstance(n,int):  #isinstance()是判断是否为某种类型
            m, n = int(m), int(n)
            # 计算 x = n^2 - 100
            x = n * n - 100
            possible_x_values.add(x)
    
    return possible_x_values

# 打印结果
print(find_integer())
