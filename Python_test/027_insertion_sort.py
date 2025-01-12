#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：使用插入排序对输入的10个数进行排序。

程序分析：
1. 从第一个元素开始，该元素可以认为已经被排序
2. 取出下一个元素，在已经排序的元素序列中从后向前扫描
3. 如果该元素（已排序）大于新元素，将该元素移到下一位置
4. 重复步骤3，直到找到已排序的元素小于或者等于新元素的位置
5. 将新元素插入到该位置后
"""

def insertion_sort(arr):
    """插入排序实现"""
    arr = arr.copy()  # 不修改原数组
    steps = []  # 记录排序步骤
    
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        steps.append((arr.copy(), i, key))  # 记录每次插入后的状态
    
    return arr, steps

def print_sort_process(steps):
    """打印排序过程"""
    print("\n排序过程：")
    for i, (arr, pos, key) in enumerate(steps, 1):
        print(f"\n第{i}步：")
        print(f"插入元素 {key} 到位置 {pos}")
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
    sorted_numbers, steps = insertion_sort(numbers)
    
    # 打印结果
    print(f"\n排序后：{sorted_numbers}")
    
    # 显示排序过程
    print_sort_process(steps) 