#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现线性查找算法，在数组中查找指定的数，并与二分查找比较性能。

程序分析：
1. 实现简单的线性查找
2. 实现带哨兵的线性查找优化版本
3. 记录查找过程
4. 与二分查找进行性能对比
"""

import time
from typing import List, Tuple, Any

def linear_search(arr: List[float], target: float) -> Tuple[int, List[Tuple[int, str]]]:
    """简单线性查找实现"""
    steps = []
    
    for i in range(len(arr)):
        steps.append((i, f"检查位置 {i}"))
        if arr[i] == target:
            steps.append((i, "找到目标值"))
            return i, steps
    
    steps.append((-1, "未找到目标值"))
    return -1, steps

def sentinel_linear_search(arr: List[float], target: float) -> Tuple[int, List[Tuple[int, str]]]:
    """带哨兵的线性查找实现"""
    steps = []
    n = len(arr)
    
    # 保存最后一个元素
    last = arr[-1]
    steps.append((-1, "保存最后一个元素"))
    
    # 设置哨兵
    arr[-1] = target
    steps.append((-1, "设置哨兵"))
    
    i = 0
    while arr[i] != target:
        steps.append((i, f"检查位置 {i}"))
        i += 1
    
    # 恢复最后一个元素
    arr[-1] = last
    steps.append((-1, "恢复最后一个元素"))
    
    if i < n - 1 or last == target:
        steps.append((i, "找到目标值"))
        return i, steps
    
    steps.append((-1, "未找到目标值"))
    return -1, steps

def compare_search_methods(arr: List[float], target: float) -> Tuple[float, float, float]:
    """比较不同查找方法的性能"""
    # 测试简单线性查找
    start_time = time.time()
    pos1, _ = linear_search(arr.copy(), target)
    time1 = time.time() - start_time
    
    # 测试带哨兵的线性查找
    start_time = time.time()
    pos2, _ = sentinel_linear_search(arr.copy(), target)
    time2 = time.time() - start_time
    
    # 测试二分查找（假设数组已排序）
    arr_sorted = sorted(arr)
    start_time = time.time()
    pos3 = binary_search(arr_sorted, target)
    time3 = time.time() - start_time
    
    return time1, time2, time3

def binary_search(arr: List[float], target: float) -> int:
    """简化版二分查找（仅用于性能比较）"""
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] > target:
            right = mid - 1
        else:
            left = mid + 1
    return -1

def print_search_process(steps: List[Tuple[int, str]]) -> None:
    """打印查找过程"""
    print("\n查找过程：")
    for i, (pos, message) in enumerate(steps, 1):
        print(f"\n第{i}步：")
        print(message)
        if pos >= 0:
            print(f"当前位置：{pos}")

def get_input_numbers() -> List[float]:
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
    try:
        # 获取输入
        numbers = get_input_numbers()
        print(f"\n输入的数列：{numbers}")
        
        # 获取要查找的数
        target = float(input("\n请输入要查找的数："))
        
        # 使用简单线性查找
        pos1, steps1 = linear_search(numbers, target)
        print("\n简单线性查找结果：")
        print_search_process(steps1)
        if pos1 != -1:
            print(f"\n找到目标值 {target} 在位置 {pos1}")
        else:
            print(f"\n未找到目标值 {target}")
        
        # 使用带哨兵的线性查找
        pos2, steps2 = sentinel_linear_search(numbers.copy(), target)
        print("\n带哨兵的线性查找结果：")
        print_search_process(steps2)
        if pos2 != -1:
            print(f"\n找到目标值 {target} 在位置 {pos2}")
        else:
            print(f"\n未找到目标值 {target}")
        
        # 性能比较
        time1, time2, time3 = compare_search_methods(numbers, target)
        print("\n性能比较：")
        print(f"简单线性查找耗时：{time1:.8f}秒")
        print(f"带哨兵的线性查找耗时：{time2:.8f}秒")
        print(f"二分查找耗时：{time3:.8f}秒")
        
    except ValueError as e:
        print(f"错误：{str(e)}") 