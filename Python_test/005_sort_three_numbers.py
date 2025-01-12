#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：输入三个整数x,y,z，请把这三个数由小到大输出。

程序分析：可以利用列表的sort方法，也可以使用冒泡排序算法。
"""

def sort_numbers_builtin(x, y, z):
    # 使用内置排序
    numbers = [x, y, z]
    numbers.sort()
    return numbers

def sort_numbers_bubble(x, y, z):
    # 使用冒泡排序
    numbers = [x, y, z]
    for i in range(len(numbers)-1):
        for j in range(len(numbers)-1-i):
            if numbers[j] > numbers[j+1]:
                numbers[j], numbers[j+1] = numbers[j+1], numbers[j]
    return numbers

if __name__ == '__main__':
    try:
        x = int(input('输入第一个数：'))
        y = int(input('输入第二个数：'))
        z = int(input('输入第三个数：'))
        
        # 使用内置方法排序
        result1 = sort_numbers_builtin(x, y, z)
        print(f'使用内置排序结果：{result1}')
        
        # 使用冒泡排序
        result2 = sort_numbers_bubble(x, y, z)
        print(f'使用冒泡排序结果：{result2}')
    except ValueError:
        print('请输入有效的整数！') 



# 使用内置函数sort():

# 输入三个整数 x y z:
x = int(input('输入第一个数：'))
y = int(input('输入第二个数：'))
z = int(input('输入第三个数：'))

# 使用内置函数sort():
numbers = [x, y, z]
numbers.sort()
print(numbers)

