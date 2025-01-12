#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：有一个已经排好序的数组。现输入一个数，要求按原来的规律将它插入数组中。

程序分析：
1. 首先判断此数是否大于最后一个数，然后再考虑插入中间的数的情况
2. 需要考虑插入数据的时间复杂度
3. 实现多种插入方法并比较性能
"""

def insert_sorted_simple(arr, num):
    """简单插入方法"""
    arr = arr.copy()  # 不修改原数组
    arr.append(num)
    arr.sort()
    return arr

def insert_sorted_binary(arr, num):
    """二分查找插入位置"""
    def binary_search(arr, num, start, end):
        if start >= end:
            return start if arr[start] > num else start + 1
        mid = (start + end) // 2
        if arr[mid] == num:
            return mid
        elif arr[mid] > num:
            return binary_search(arr, num, start, mid)
        else:
            return binary_search(arr, num, mid + 1, end)
    
    arr = arr.copy()
    if not arr or num <= arr[0]:
        return [num] + arr
    if num >= arr[-1]:
        return arr + [num]
    
    pos = binary_search(arr, num, 0, len(arr)-1)
    return arr[:pos] + [num] + arr[pos:]

def compare_methods(arr, num):
    """比较不同插入方法的结果"""
    import time
    
    # 测试简单插入方法
    start_time = time.time()
    result1 = insert_sorted_simple(arr, num)
    time1 = time.time() - start_time
    
    # 测试二分查找插入方法
    start_time = time.time()
    result2 = insert_sorted_binary(arr, num)
    time2 = time.time() - start_time
    
    return result1, result2, time1, time2

if __name__ == '__main__':
    # 测试数据
    test_array = [1, 4, 6, 9, 13, 16, 19, 28, 40, 100]
    
    try:
        print(f"原始数组：{test_array}")
        num = int(input("请输入要插入的数字："))
        
        result1, result2, time1, time2 = compare_methods(test_array, num)
        
        print("\n简单插入法：")
        print(f"结果：{result1}")
        print(f"耗时：{time1:.8f}秒")
        
        print("\n二分查找插入法：")
        print(f"结果：{result2}")
        print(f"耗时：{time2:.8f}秒")
        
    except ValueError:
        print("请输入有效的数字！") 