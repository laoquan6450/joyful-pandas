#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现指数查找算法，在有序数组中查找指定的数。

程序分析：
1. 指数查找首先找到一个范围，目标值在这个范围内
2. 通过指数增长（1, 2, 4, 8, ...）来快速确定范围
3. 找到范围后使用二分查找在该范围内查找目标值
4. 适用于无界或很大的有序数组
"""

import time
from typing import List, Tuple, Optional

def binary_search(arr: List[float], left: int, right: int, target: float) -> Tuple[int, List[Tuple[int, int, int, str]]]:
    """二分查找实现"""
    steps = []
    right = min(right, len(arr) - 1)
    
    while left <= right:
        mid = (left + right) // 2
        steps.append((mid, left, right, f"二分查找：检查位置 {mid}"))
        
        if arr[mid] == target:
            steps.append((mid, mid, mid, "找到目标值"))
            return mid, steps
        elif arr[mid] < target:
            left = mid + 1
            steps.append((-1, left, right, "向右查找"))
        else:
            right = mid - 1
            steps.append((-1, left, right, "向左查找"))
    
    steps.append((-1, -1, -1, "未找到目标值"))
    return -1, steps

def exponential_search(arr: List[float], target: float) -> Tuple[int, List[Tuple[int, int, int, str]]]:
    """指数查找实现"""
    steps = []
    n = len(arr)
    
    if arr[0] == target:
        steps.append((0, 0, 0, "在首位找到目标值"))
        return 0, steps
    
    # 找到范围
    i = 1
    while i < n and arr[i] <= target:
        steps.append((i, 0, i, f"扩展范围到位置 {i}"))
        i *= 2
    
    # 在确定的范围内使用二分查找
    steps.append((-1, i//2, min(i, n-1), f"确定查找范围 [{i//2}, {min(i, n-1)}]"))
    pos, binary_steps = binary_search(arr, i//2, min(i, n-1), target)
    steps.extend(binary_steps)
    
    return pos, steps

def print_search_process(arr: List[float], steps: List[Tuple[int, int, int, str]]) -> None:
    """打印查找过程"""
    print("\n指数查找过程：")
    for i, (pos, left, right, message) in enumerate(steps, 1):
        print(f"\n第{i}步：")
        print(message)
        if pos >= 0 and pos < len(arr):
            print(f"当前检查位置：{pos}，值：{arr[pos]}")
        if left >= 0 and right >= 0 and left <= right:
            print(f"当前范围：{arr[left:right+1]}")

def get_sorted_numbers() -> List[float]:
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

def compare_search_methods(arr: List[float], target: float) -> None:
    """比较不同查找方法的性能"""
    # 测试指数查找
    start_time = time.time()
    pos1, _ = exponential_search(arr, target)
    time1 = time.time() - start_time
    
    # 测试二分查找
    start_time = time.time()
    pos2, _ = binary_search(arr, 0, len(arr)-1, target)
    time2 = time.time() - start_time
    
    # 测试线性查找
    start_time = time.time()
    pos3 = -1
    for i, num in enumerate(arr):
        if num == target:
            pos3 = i
            break
    time3 = time.time() - start_time
    
    print("\n性能比较：")
    print(f"指数查找耗时：{time1:.8f}秒")
    print(f"二分查找耗时：{time2:.8f}秒")
    print(f"线性查找耗时：{time3:.8f}秒")

if __name__ == '__main__':
    try:
        # 获取有序数列
        numbers = get_sorted_numbers()
        print(f"\n输入的有序数列：{numbers}")
        
        # 获取要查找的数
        target = float(input("\n请输入要查找的数："))
        
        # 使用指数查找
        pos, steps = exponential_search(numbers, target)
        print_search_process(numbers, steps)
        
        if pos != -1:
            print(f"\n找到目标值 {target} 在位置 {pos}")
        else:
            print(f"\n未找到目标值 {target}")
        
        # 性能比较
        compare_search_methods(numbers, target)
        
    except ValueError as e:
        print(f"错误：{str(e)}") 