#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：求完数。一个数如果恰好等于它的因子之和，这个数就称为"完数"。例如6=1＋2＋3。编程找出1000以内的所有完数。

程序分析：
1. 遍历1-1000的数
2. 对每个数找出它的所有因子（不包括自身）
3. 判断因子之和是否等于该数
"""

def get_factors(n):
    """获取一个数的所有因子（不包括自身）"""
    factors = []
    for i in range(1, n):
        if n % i == 0:
            factors.append(i)
    return factors

def find_perfect_numbers(limit):
    """找出指定范围内的所有完数"""
    perfect_nums = []
    for num in range(2, limit + 1):
        if sum(get_factors(num)) == num:
            perfect_nums.append(num)
    return perfect_nums

if __name__ == '__main__':
    limit = 1000
    perfect_numbers = find_perfect_numbers(limit)
    print(f"1000以内的完数有：{perfect_numbers}")
    
    # 验证结果
    for num in perfect_numbers:
        factors = get_factors(num)
        print(f"\n{num}的因子是：{factors}")
        print(f"因子之和：{sum(factors)} = {num}") 