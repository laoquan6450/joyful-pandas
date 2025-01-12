#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：斐波那契数列的递归和非递归实现。

程序分析：
1. 斐波那契数列：1, 1, 2, 3, 5, 8, 13, 21, ...
2. 实现递归和非递归两种方式
3. 比较两种方式的性能差异
4. 添加缓存优化递归方式
"""

from functools import lru_cache
import time

@lru_cache(maxsize=None)
def fibonacci_recursive(n):
    """递归方式实现斐波那契数列（带缓存）"""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)

def fibonacci_iterative(n):
    """迭代方式实现斐波那契数列"""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def compare_performance(n):
    """比较两种方法的性能"""
    # 测试递归方法
    start_time = time.time()
    result1 = fibonacci_recursive(n)
    recursive_time = time.time() - start_time
    
    # 测试迭代方法
    start_time = time.time()
    result2 = fibonacci_iterative(n)
    iterative_time = time.time() - start_time
    
    return result1, result2, recursive_time, iterative_time

if __name__ == '__main__':
    try:
        n = int(input('请输入要计算的斐波那契数列项数：'))
        if n < 0:
            print("请输入非负整数！")
        else:
            result1, result2, rec_time, iter_time = compare_performance(n)
            print(f"\n第{n}项的值：")
            print(f"递归方法结果：{result1}")
            print(f"迭代方法结果：{result2}")
            print(f"\n性能比较：")
            print(f"递归方法耗时：{rec_time:.6f}秒")
            print(f"迭代方法耗时：{iter_time:.6f}秒")
            
            # 打印前n项
            print(f"\n斐波那契数列前{n}项：")
            sequence = [fibonacci_iterative(i) for i in range(n)]
            print(sequence)
    except ValueError:
        print("请输入有效的整数！") 