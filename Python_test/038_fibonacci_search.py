#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现斐波那契查找算法，在有序数组中查找指定的数。

程序分析：
1. 斐波那契查找是利用黄金分割原理的查找算法
2. 需要先生成斐波那契数列
3. 将待查找数组的长度扩展到斐波那契数列项的大小
4. 按照斐波那契数列进行分割查找
"""

import time
from typing import List, Tuple

def generate_fibonacci(max_size: int) -> List[int]:
    """生成斐波那契数列"""
    fib = [0, 1]
    while fib[-1] < max_size:
        fib.append(fib[-1] + fib[-2])
    return fib

def fibonacci_search(arr: List[float], target: float) -> Tuple[int, List[Tuple[int, int, int, str]]]:
    """斐波那契查找实现"""
    steps = []
    n = len(arr)
    
    # 生成斐波那契数列
    fibonacci = generate_fibonacci(n)
    k = 0
    while fibonacci[k] - 1 < n:
        k += 1
    
    # 扩展原数组
    temp = arr.copy() + [arr[-1]] * (fibonacci[k] - 1 - n)
    steps.append((-1, -1, -1, f"扩展数组到长度 {len(temp)}"))
    
    left, right = 0, n - 1
    # 进行斐波那契分割查找
    while left <= right:
        # 计算分割位置
        i = min(left + fibonacci[k-1] - 1, n - 1)
        steps.append((i, left, right, f"斐波那契分割位置：{i}"))
        
        if target < temp[i]:
            right = i - 1
            k -= 1
            steps.append((i, left, right, "向左查找"))
        elif target > temp[i]:
            left = i + 1
            k -= 2
            steps.append((i, left, right, "向右查找"))
        else:
            if i < n:
                steps.append((i, i, i, "找到目标值"))
                return i, steps
            else:
                steps.append((n-1, n-1, n-1, "找到目标值（在扩展部分）"))
                return n - 1, steps
    
    steps.append((-1, left, right, "未找到目标值"))
    return -1, steps

def print_search_process(arr: List[float], steps: List[Tuple[int, int, int, str]]) -> None:
    """打印查找过程"""
    print("\n斐波那契查找过程：")
    for i, (pos, left, right, message) in enumerate(steps, 1):
        print(f"\n第{i}步：")
        print(message)
        if left >= 0 and right >= 0 and left <= right:
            print(f"查找范围：{arr[left:right+1]}")
            if pos >= 0 and pos < len(arr):
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

def compare_with_binary_search(arr: List[float], target: float) -> None:
    """与二分查找进行性能比较"""
    # 测试斐波那契查找
    start_time = time.time()
    pos1, _ = fibonacci_search(arr, target)
    time1 = time.time() - start_time
    
    # 测试二分查找
    start_time = time.time()
    left, right = 0, len(arr) - 1
    pos2 = -1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            pos2 = mid
            break
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    time2 = time.time() - start_time
    
    print("\n性能比较：")
    print(f"斐波那契查找耗时：{time1:.8f}秒")
    print(f"二分查找耗时：{time2:.8f}秒")

if __name__ == '__main__':
    try:
        # 获取有序数列
        numbers = get_sorted_numbers()
        print(f"\n输入的有序数列：{numbers}")
        
        # 获取要查找的数
        target = float(input("\n请输入要查找的数："))
        
        # 使用斐波那契查找
        pos, steps = fibonacci_search(numbers, target)
        print_search_process(numbers, steps)
        
        if pos != -1:
            print(f"\n找到目标值 {target} 在位置 {pos}")
        else:
            print(f"\n未找到目标值 {target}")
        
        # 性能比较
        compare_with_binary_search(numbers, target)
        
    except ValueError as e:
        print(f"错误：{str(e)}") 