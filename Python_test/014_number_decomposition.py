#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：将一个正整数分解质因数。例如：输入90,打印出90=2*3*3*5。

程序分析：
1. 对于一个正整数，从最小的质数2开始尝试整除
2. 如果能整除，则将商继续分解
3. 如果不能整除，则尝试下一个质数
4. 重复上述过程直到最后的商为1
"""

def prime_factors(n):
    """分解质因数"""
    factors = []
    divisor = 2
    
    while n > 1:
        while n % divisor == 0:
            factors.append(divisor)
            n //= divisor
        divisor += 1
        if divisor * divisor > n:  # 优化：如果除数的平方大于n，则n本身是质数
            if n > 1:
                factors.append(n)
            break
    
    return factors

def format_factors(factors):
    """格式化输出因数分解结果"""
    if not factors:
        return "1"
    return "*".join(map(str, factors))

if __name__ == '__main__':
    try:
        num = int(input("请输入一个正整数："))
        if num <= 0:
            print("请输入正整数！")
        else:
            factors = prime_factors(num)
            result = format_factors(factors)
            print(f"{num} = {result}")
    except ValueError:
        print("请输入有效的整数！") 