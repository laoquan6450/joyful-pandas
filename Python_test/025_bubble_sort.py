#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：使用冒泡排序对输入的10个数进行排序。

程序分析：
1. 比较相邻的元素。如果第一个比第二个大，就交换他们两个。
2. 对每一对相邻元素作同样的工作，从开始第一对到结尾的最后一对。
3. 针对所有的元素重复以上的步骤，除了最后一个。
4. 持续每次对越来越少的元素重复上面的步骤，直到没有任何一对数字需要比较。
"""

def bubble_sort(arr):
    """冒泡排序实现"""
    arr = arr.copy()  # 不修改原数组
    n = len(arr)
    steps = []  # 记录每步操作
    
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
                steps.append(arr.copy())  # 记录每次交换后的状态
        if not swapped:
            break
    
    return arr, steps

def print_sort_process(steps):
    """打印排序过程"""
    print("\n排序过程：")
    for i, step in enumerate(steps, 1):
        print(f"第{i}步：{step}")

def get_input_numbers():
    """获取用户输入的数字"""
    numbers = []
    print("请输入10个数字：")
    while len(numbers) < 10:
        try:
            num = float(input(f"请输入第{len(numbers)+1}个数字："))
            numbers.append(num)
        except ValueError:
            print("请输入有效的数字！")
    return numbers

if __name__ == '__main__':
    # 获取输入
    numbers = get_input_numbers()
    print(f"\n原始数组：{numbers}")
    
    # 进行排序
    sorted_numbers, steps = bubble_sort(numbers)
    
    # 打印结果
    print(f"\n排序后：{sorted_numbers}")
    
    # 显示排序过程
    print_sort_process(steps) 