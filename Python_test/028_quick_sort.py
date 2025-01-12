#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：使用快速排序对输入的10个数进行排序。

程序分析：
1. 从数列中挑出一个元素，称为"基准"（pivot）
2. 重新排序数列，所有比基准值小的元素摆放在基准前面，所有比基准值大的元素摆在基准后面
3. 递归地把小于基准值元素的子数列和大于基准值元素的子数列排序
"""

def quick_sort(arr, start=None, end=None, steps=None):
    """快速排序实现"""
    if start is None:
        arr = arr.copy()  # 不修改原数组
        start = 0
        end = len(arr) - 1
        steps = []
    
    if start < end:
        pivot_idx = partition(arr, start, end, steps)
        quick_sort(arr, start, pivot_idx - 1, steps)
        quick_sort(arr, pivot_idx + 1, end, steps)
    
    return arr, steps

def partition(arr, start, end, steps):
    """分区操作"""
    pivot = arr[end]
    i = start - 1
    
    for j in range(start, end):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            steps.append((arr.copy(), i, j, "交换"))
    
    arr[i + 1], arr[end] = arr[end], arr[i + 1]
    steps.append((arr.copy(), i + 1, end, "基准值就位"))
    return i + 1

def print_sort_process(steps):
    """打印排序过程"""
    print("\n排序过程：")
    for i, (arr, pos1, pos2, action) in enumerate(steps, 1):
        print(f"\n第{i}步：")
        print(f"{action}：位置 {pos1} 和位置 {pos2}")
        print(f"数组变为：{arr}")

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
    sorted_numbers, steps = quick_sort(numbers)
    
    # 打印结果
    print(f"\n排序后：{sorted_numbers}")
    
    # 显示排序过程
    print_sort_process(steps) 