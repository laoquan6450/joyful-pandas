#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：有5个人坐在一起，问第五个人多少岁？他说比第4个人大2岁。
问第4个人岁数，他说比第3个人大2岁。问第三个人，又说比第2人大两岁。
问第2个人，说比第一个人大两岁。最后问第一个人，他说是10岁。
请问第五个人多大？

程序分析：
1. 利用递归的思维解决问题
2. 同时提供迭代的解法
3. 扩展问题规模，使其能处理n个人的情况
"""

def age_recursive(n):
    """递归方式计算第n个人的年龄"""
    if n == 1:
        return 10
    return age_recursive(n - 1) + 2

def age_iterative(n):
    """迭代方式计算第n个人的年龄"""
    age = 10  # 第一个人的年龄
    for i in range(1, n):
        age += 2
    return age

def print_age_calculation(n):
    """打印年龄计算过程"""
    ages = []
    current_age = 10
    for i in range(1, n + 1):
        ages.append(current_age)
        current_age += 2
    
    # 打印计算过程
    for i, age in enumerate(ages, 1):
        print(f"第{i}个人：{age}岁")
        if i < n:
            print(f"第{i+1}个人比第{i}个人大2岁")

if __name__ == '__main__':
    try:
        n = int(input('请输入要计算的人数：'))
        if n <= 0:
            print("人数必须为正整数！")
        else:
            # 使用递归方法
            result1 = age_recursive(n)
            print(f"\n递归方法计算第{n}个人的年龄：{result1}岁")
            
            # 使用迭代方法
            result2 = age_iterative(n)
            print(f"迭代方法计算第{n}个人的年龄：{result2}岁")
            
            # 打印计算过程
            print("\n详细计算过程：")
            print_age_calculation(n)
            
    except ValueError:
        print("请输入有效的整数！") 