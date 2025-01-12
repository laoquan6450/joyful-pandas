#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现插值查找算法，在有序数组中查找指定的数。

程序分析：
1. 插值查找是二分查找的改进版本
2. 根据要查找的关键字value与查找表中最大最小记录的关键字比较后的查找方法
3. 插值的计算公式：mid = left + (right-left) * (target-arr[left])/(arr[right]-arr[left])
4. 对于分布均匀的数据，性能优于二分查找
"""

import time
from typing import List, Tuple

def interpolation_search(arr: List[float], target: float) -> Tuple[int, List[Tuple[int, int, int, str]]]:
    """插值查找实现"""
    steps = []
    left, right = 0, len(arr) - 1
    
    while left <= right and arr[left] <= target <= arr[right]:
        if arr[left] == arr[right]:
            if arr[left] == target:
                steps.append((left, left, right, "找到目标值"))
                return left, steps
            break
        
        # 计算插值位置
        pos = left + int((right - left) * (target - arr[left]) / (arr[right] - arr[left]))
        steps.append((pos, left, right, f"计算插值位置：{pos}"))
        
        if arr[pos] == target:
            steps.append((pos, pos, pos, "找到目标值"))
            return pos, steps
        elif arr[pos] < target:
            left = pos + 1
            steps.append((pos, left, right, "向右查找"))
        else:
            right = pos - 1
            steps.append((pos, left, right, "向左查找"))
    
    steps.append((-1, left, right, "未找到目标值"))
    return -1, steps

def binary_search(arr: List[float], target: float) -> Tuple[int, List[Tuple[int, int, int, str]]]:
    """二分查找实现（用于比较）"""
    steps = []
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        steps.append((mid, left, right, f"计算中间位置：{mid}"))
        
        if arr[mid] == target:
            steps.append((mid, mid, mid, "找到目标值"))
            return mid, steps
        elif arr[mid] < target:
            left = mid + 1
            steps.append((mid, left, right, "向右查找"))
        else:
            right = mid - 1
            steps.append((mid, left, right, "向左查找"))
    
    steps.append((-1, left, right, "未找到目标值"))
    return -1, steps

def print_search_process(arr: List[float], steps: List[Tuple[int, int, int, str]], method: str) -> None:
    """打印查找过程"""
    print(f"\n{method}查找过程：")
    for i, (pos, left, right, message) in enumerate(steps, 1):
        print(f"\n第{i}步：")
        print(message)
        if left <= right:
            print(f"查找范围：{arr[left:right+1]}")
            if pos >= 0:
                print(f"当前检查位置：{pos}，值：{arr[pos]}")

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

def compare_performance(arr: List[float], target: float) -> Tuple[float, float]:
    """比较插值查找和二分查找的性能"""
    # 测试插值查找
    start_time = time.time()
    interpolation_search(arr, target)
    time1 = time.time() - start_time
    
    # 测试二分查找
    start_time = time.time()
    binary_search(arr, target)
    time2 = time.time() - start_time
    
    return time1, time2

if __name__ == '__main__':
    try:
        # 获取有序数列
        numbers = get_sorted_numbers()
        print(f"\n输入的有序数列：{numbers}")
        
        # 获取要查找的数
        target = float(input("\n请输入要查找的数："))
        
        # 使用插值查找
        pos1, steps1 = interpolation_search(numbers, target)
        print_search_process(numbers, steps1, "插值")
        if pos1 != -1:
            print(f"\n插值查找：找到目标值 {target} 在位置 {pos1}")
        else:
            print(f"\n插值查找：未找到目标值 {target}")
        
        # 使用二分查找
        pos2, steps2 = binary_search(numbers, target)
        print_search_process(numbers, steps2, "二分")
        if pos2 != -1:
            print(f"\n二分查找：找到目标值 {target} 在位置 {pos2}")
        else:
            print(f"\n二分查找：未找到目标值 {target}")
        
        # 性能比较
        time1, time2 = compare_performance(numbers, target)
        print("\n性能比较：")
        print(f"插值查找耗时：{time1:.8f}秒")
        print(f"二分查找耗时：{time2:.8f}秒")
        
    except ValueError as e:
        print(f"错误：{str(e)}") 