#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现二分查找算法，在一个有序数组中查找指定的数。

程序分析：
1. 数组必须是有序的
2. 每次查找将范围缩小一半
3. 实现递归和迭代两种方式
4. 记录并显示查找过程
"""

def binary_search_recursive(arr, target, left=None, right=None, steps=None):
    """递归实现二分查找"""
    if left is None:
        left = 0
        right = len(arr) - 1
        steps = []
    
    if left > right:
        steps.append((left, right, "未找到目标值"))
        return -1, steps
    
    mid = (left + right) // 2
    steps.append((left, mid, right, f"查找范围 [{left}, {right}]，中间位置 {mid}"))
    
    if arr[mid] == target:
        steps.append((mid, mid, "找到目标值"))
        return mid, steps
    elif arr[mid] > target:
        return binary_search_recursive(arr, target, left, mid - 1, steps)
    else:
        return binary_search_recursive(arr, target, mid + 1, right, steps)

def binary_search_iterative(arr, target):
    """迭代实现二分查找"""
    steps = []
    left = 0
    right = len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        steps.append((left, mid, right, f"查找范围 [{left}, {right}]，中间位置 {mid}"))
        
        if arr[mid] == target:
            steps.append((mid, mid, "找到目标值"))
            return mid, steps
        elif arr[mid] > target:
            right = mid - 1
        else:
            left = mid + 1
    
    steps.append((left, right, "未找到目标值"))
    return -1, steps

def print_search_process(arr, steps, method):
    """打印查找过程"""
    print(f"\n{method}查找过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if len(step) == 4:  # 常规查找步骤
            left, mid, right, message = step
            print(message)
            print("当前数组片段：", arr[left:right+1])
        else:  # 结果步骤
            if len(step) == 3:
                left, right, message = step
                print(message)
            else:
                pos, _, message = step
                print(f"{message}，位置：{pos}")

def get_sorted_numbers():
    """获取用户输入的有序数列"""
    numbers = []
    print("请输入10个递增的数字：")
    while len(numbers) < 10:
        try:
            num = float(input(f"请输入第{len(numbers)+1}个数字："))
            if numbers and num <= numbers[-1]:
                print("请输入比前一个数大的数！")
                continue
            numbers.append(num)
        except ValueError:
            print("请输入有效的数字！")
    return numbers

if __name__ == '__main__':
    # 获取有序数列
    numbers = get_sorted_numbers()
    print(f"\n输入的有序数列：{numbers}")
    
    # 获取要查找的数
    try:
        target = float(input("\n请输入要查找的数："))
        
        # 使用递归方法查找
        pos1, steps1 = binary_search_recursive(numbers, target)
        print_search_process(numbers, steps1, "递归")
        if pos1 != -1:
            print(f"\n递归方法：找到目标值 {target} 在位置 {pos1}")
        else:
            print(f"\n递归方法：未找到目标值 {target}")
        
        # 使用迭代方法查找
        pos2, steps2 = binary_search_iterative(numbers, target)
        print_search_process(numbers, steps2, "迭代")
        if pos2 != -1:
            print(f"\n迭代方法：找到目标值 {target} 在位置 {pos2}")
        else:
            print(f"\n迭代方法：未找到目标值 {target}")
            
    except ValueError:
        print("请输入有效的数字！") 