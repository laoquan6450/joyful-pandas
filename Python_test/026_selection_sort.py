#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：使用选择排序对输入的10个数进行排序。

程序分析：
1. 首先在未排序序列中找到最小（大）元素，存放到排序序列的起始位置
2. 再从剩余未排序元素中继续寻找最小（大）元素，然后放到已排序序列的末尾
3. 重复第二步，直到所有元素均排序完毕
"""

def selection_sort(arr):
    """选择排序实现"""
    arr = arr.copy()  # 不修改原数组
    n = len(arr)
    steps = []  # 记录每步操作
    
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            steps.append((arr.copy(), i, min_idx))  # 记录交换操作
    
    return arr, steps

def print_sort_process(original, steps):
    """打印排序过程"""
    print("\n排序过程：")
    print(f"初始数组：{original}")
    
    for i, (arr, pos1, pos2) in enumerate(steps, 1):
        print(f"\n第{i}步：")
        print(f"交换位置 {pos1} 和位置 {pos2} 的元素")
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
    sorted_numbers, steps = selection_sort(numbers)
    
    # 打印结果
    print(f"\n排序后：{sorted_numbers}")
    
    # 显示排序过程
    print_sort_process(numbers, steps) 