#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：利用递归方法求5!。

程序分析：
1. 递归公式：n! = n * (n-1)!
2. 递归终止条件：0! = 1
3. 同时实现递归和迭代两种方法
"""

def factorial_recursive(n):
    """递归方法计算阶乘"""
    if n < 0:
        raise ValueError("负数没有阶乘")
    if n == 0:
        return 1
    return n * factorial_recursive(n - 1)

def factorial_iterative(n):
    """迭代方法计算阶乘"""
    if n < 0:
        raise ValueError("负数没有阶乘")
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

def show_calculation_process(n):
    """显示阶乘的计算过程"""
    if n < 0:
        return "负数没有阶乘"
    
    process = []
    result = 1
    for i in range(1, n + 1):
        result *= i
        process.append(str(i))
    
    return " × ".join(process) + f" = {result}"

if __name__ == '__main__':
    try:
        n = int(input('请输入要计算阶乘的数：'))
        
        # 使用递归方法
        result1 = factorial_recursive(n)
        print(f"\n递归方法计算 {n}! = {result1}")
        
        # 使用迭代方法
        result2 = factorial_iterative(n)
        print(f"迭代方法计算 {n}! = {result2}")
        
        # 显示计算过程
        print(f"\n计算过程：")
        print(f"{n}! = {show_calculation_process(n)}")
        
    except ValueError as e:
        print(f"错误：{str(e)}") 