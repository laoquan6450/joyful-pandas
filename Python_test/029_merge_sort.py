#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：使用归并排序对输入的10个数进行排序。

程序分析：
1. 把长度为n的输入序列分成两个长度为n/2的子序列
2. 对这两个子序列分别采用归并排序
3. 将两个排序好的子序列合并成一个最终的排序序列
"""

def merge_sort(arr):
    """归并排序实现"""
    arr = arr.copy()  # 不修改原数组
    steps = []  # 记录排序步骤
    
    def merge(arr, left, mid, right):
        """合并两个已排序的子数组"""
        left_arr = arr[left:mid + 1]
        right_arr = arr[mid + 1:right + 1]
        
        i = j = 0
        k = left
        while i < len(left_arr) and j < len(right_arr):
            if left_arr[i] <= right_arr[j]:
                arr[k] = left_arr[i]
                i += 1
            else:
                arr[k] = right_arr[j]
                j += 1
            k += 1
            steps.append((arr.copy(), left, right, "合并"))
        
        while i < len(left_arr):
            arr[k] = left_arr[i]
            i += 1
            k += 1
            steps.append((arr.copy(), left, right, "合并左侧"))
            
        while j < len(right_arr):
            arr[k] = right_arr[j]
            j += 1
            k += 1
            steps.append((arr.copy(), left, right, "合并右侧"))
    
    def sort(arr, left, right):
        """递归排序"""
        if left < right:
            mid = (left + right) // 2
            steps.append((arr.copy(), left, right, "分割"))
            
            sort(arr, left, mid)
            sort(arr, mid + 1, right)
            merge(arr, left, mid, right)
    
    sort(arr, 0, len(arr) - 1)
    return arr, steps

def print_sort_process(steps):
    """打印排序过程"""
    print("\n排序过程：")
    for i, (arr, left, right, action) in enumerate(steps, 1):
        print(f"\n第{i}步：")
        print(f"{action}：范围 [{left}, {right}]")
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
    sorted_numbers, steps = merge_sort(numbers)
    
    # 打印结果
    print(f"\n排序后：{sorted_numbers}")
    
    # 显示排序过程
    print_sort_process(steps) 