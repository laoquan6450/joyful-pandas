#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：输出 9*9 乘法口诀表。

程序分析：
1. 输出9行，从1到9
2. 每行输出的个数递增，从1到当前行数
3. 每个数字都是行号和列号的乘积
"""

def print_multiplication_table():
    # 遍历行号，从1到9
    for i in range(1, 10):
        # 遍历列号，从1到当前行号
        for j in range(1, i + 1):
            # 计算乘积
            product = i * j
            # 格式化输出，保持对齐
            print(f"{j}×{i}={product:<3}", end=' ')
        print()  # 换行

if __name__ == '__main__':
    print_multiplication_table() 