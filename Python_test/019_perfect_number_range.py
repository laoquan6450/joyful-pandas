#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：一个数如果恰好等于它的因子之和，这个数就称为"完数"。
例如6=1＋2＋3。编程找出1000以内的所有完数。

程序分析：
1. 函数要返回一个数的所有因子
2. 判断因子之和是否等于原数
3. 注意优化性能
"""

def get_factors(num):
    """获取一个数的所有因子（不包括自身）"""
    factors = set()  # 使用集合避免重复
    for i in range(1, int(num ** 0.5) + 1):
        if num % i == 0:
            factors.add(i)
            if i > 1:  # 避免将自身加入因子集合
                factors.add(num // i)
    return factors

def is_perfect(num):
    """判断一个数是否为完数"""
    if num < 2:
        return False
    return sum(get_factors(num)) == num

def find_perfect_numbers(start, end):
    """在指定范围内找出所有完数"""
    return [num for num in range(start, end + 1) if is_perfect(num)]

def verify_perfect_number(num):
    """验证一个完数，返回其因子和计算过程"""
    factors = sorted(get_factors(num))
    return f"{num} = " + " + ".join(map(str, factors))

if __name__ == '__main__':
    start, end = 1, 1000
    perfect_numbers = find_perfect_numbers(start, end)
    
    print(f"在{start}到{end}之间的完数有：{perfect_numbers}")
    print("\n验证每个完数：")
    for num in perfect_numbers:
        print(verify_perfect_number(num)) 