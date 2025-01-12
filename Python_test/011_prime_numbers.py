#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：判断101-200之间有多少个素数，并输出所有素数。

程序分析：
1. 判断素数的方法：用一个数分别去除2到sqrt(这个数)，如果能被整除，则表明此数不是素数，反之是素数。
2. 使用列表推导式和filter函数可以使代码更简洁。
"""

import math

def is_prime(n):
    """判断一个数是否为素数"""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def find_primes(start, end):
    """在指定范围内找出所有素数"""
    # 使用列表推导式
    primes = [num for num in range(start, end + 1) if is_prime(num)]
    return primes

def find_primes_filter(start, end):
    """使用filter函数找出素数"""
    return list(filter(is_prime, range(start, end + 1)))

if __name__ == '__main__':
    start, end = 101, 200
    
    # 使用列表推导式方法
    primes = find_primes(start, end)
    print(f"在{start}-{end}之间的素数个数为：{len(primes)}")
    print(f"素数列表：{primes}")
    
    # 使用filter方法
    primes_filter = find_primes_filter(start, end)
    print("\n使用filter方法得到相同结果：")
    print(f"素数个数：{len(primes_filter)}")
    print(f"素数列表：{primes_filter}") 