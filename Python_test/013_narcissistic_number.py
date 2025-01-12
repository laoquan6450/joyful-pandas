#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：打印出所有的"水仙花数"，所谓"水仙花数"是指一个三位数，其各位数字立方和等于该数本身。
例如：153是一个"水仙花数"，因为153=1的三次方＋5的三次方＋3的三次方。

程序分析：
1. 遍历所有的三位数（100-999）
2. 将每个数分解出个、十、百位
3. 计算每个位数的立方和并判断
"""

def is_narcissistic(num):
    """判断一个数是否为水仙花数"""
    # 获取各个位数
    hundreds = num // 100
    tens = (num % 100) // 10
    ones = num % 10
    
    # 计算立方和
    sum_of_cubes = hundreds**3 + tens**3 + ones**3
    
    return sum_of_cubes == num

def find_narcissistic_numbers():
    """找出所有的水仙花数"""
    return [num for num in range(100, 1000) if is_narcissistic(num)]

if __name__ == '__main__':
    narcissistic_numbers = find_narcissistic_numbers()
    print(f"所有的水仙花数：{narcissistic_numbers}")
    
    # 验证结果
    for num in narcissistic_numbers:
        hundreds = num // 100
        tens = (num % 100) // 10
        ones = num % 10
        print(f"\n验证 {num}:")
        print(f"{hundreds}³ + {tens}³ + {ones}³ = "
              f"{hundreds**3} + {tens**3} + {ones**3} = {num}") 