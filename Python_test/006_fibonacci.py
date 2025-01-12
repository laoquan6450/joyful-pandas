#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：斐波那契数列。

程序分析：斐波那契数列（Fibonacci sequence），从第3项开始，每一项都等于前两项之和。
"""

def fibonacci_recursive(n):
    """递归方法生成斐波那契数列"""
    if n <= 0:
        return []
    elif n == 1:
        return [1]
    elif n == 2:
        return [1, 1]
    else:
        fib = fibonacci_recursive(n - 1)
        fib.append(fib[-1] + fib[-2])
        return fib

def fibonacci_iterative(n):
    """迭代方法生成斐波那契数列"""
    if n <= 0:
        return []
    elif n == 1:
        return [1]
    
    fib = [1, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib

if __name__ == '__main__':
    try:
        n = int(input('请输入要生成的斐波那契数列项数：'))
        if n <= 0:
            print('请输入正整数！')
        else:
            print(f'递归方法结果：{fibonacci_recursive(n)}')
            print(f'迭代方法结果：{fibonacci_iterative(n)}')
    except ValueError:
        print('请输入有效的整数！') 