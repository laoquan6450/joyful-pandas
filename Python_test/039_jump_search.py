#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现跳跃查找算法，在有序数组中查找指定的数。

程序分析：
1. 跳跃查找是对线性查找的改进
2. 基本思想是每次跳过固定步长而不是逐个检查
3. 最优步长是 sqrt(n)，其中n是数组长度
4. 找到可能的区间后再进行线性查找
"""

import math
import time
from typing import List, Tuple

def jump_search(arr: List[float], target: float) -> Tuple[int, List[Tuple[int, int, str]]]:
    """跳跃查找实现"""
    steps = []
    n = len(arr)
    
    # 计算最优步长
    step = int(math.sqrt(n))
    steps.append((-1, step, f"设置步长为 {step}"))
    
    # 找到目标值可能在的区块
    prev = 0
    current = step
    while current < n and arr[current] <= target:
        steps.append((current, step, f"跳跃到位置 {current}"))
        prev = current
        current += step
    
    # 确保不越界
    current = min(current, n)
    steps.append((current, step, "确定搜索区间"))
    
    # 在确定的区间内进行线性查找
    steps.append((prev, current, f"在区间 [{prev}, {current}] 中线性查找"))
    for i in range(prev, current):
        steps.append((i, -1, f"检查位置 {i}"))
        if arr[i] == target:
            steps.append((i, -1, "找到目标值"))
            return i, steps
    
    steps.append((-1, -1, "未找到目标值"))
    return -1, steps

def print_search_process(arr: List[float], steps: List[Tuple[int, int, str]]) -> None:
    """打印查找过程"""
    print("\n跳跃查找过程：")
    for i, (pos, step, message) in enumerate(steps, 1):
        print(f"\n第{i}步：")
        print(message)
        if pos >= 0 and pos < len(arr):
            print(f"当前位置：{pos}，值：{arr[pos]}")

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
    # 测试跳跃查找
    start_time = time.time()
    pos1, _ = jump_search(arr, target)
    time1 = time.time() - start_time
    
    # 测试线性查找
    start_time = time.time()
    pos2 = -1
    for i, num in enumerate(arr):
        if num == target:
            pos2 = i
            break
    time2 = time.time() - start_time
    
    # 测试二分查找
    start_time = time.time()
    left, right = 0, len(arr) - 1
    pos3 = -1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            pos3 = mid
            break
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    time3 = time.time() - start_time
    
    print("\n性能比较：")
    print(f"跳跃查找耗时：{time1:.8f}秒")
    print(f"线性查找耗时：{time2:.8f}秒")
    print(f"二分查找耗时：{time3:.8f}秒")

if __name__ == '__main__':
    try:
        # 获取有序数列
        numbers = get_sorted_numbers()
        print(f"\n输入的有序数列：{numbers}")
        
        # 获取要查找的数
        target = float(input("\n请输入要查找的数："))
        
        # 使用跳跃查找
        pos, steps = jump_search(numbers, target)
        print_search_process(numbers, steps)
        
        if pos != -1:
            print(f"\n找到目标值 {target} 在位置 {pos}")
        else:
            print(f"\n未找到目标值 {target}")
        
        # 性能比较
        compare_search_methods(numbers, target)
        
    except ValueError as e:
        print(f"错误：{str(e)}") 