#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：使用希尔排序对输入的10个数进行排序。

程序分析：
1. 选择一个增量序列t1，t2，...，tk，其中ti>tj，tk=1
2. 按增量序列个数k，对序列进行k趟排序
3. 每趟排序，根据对应的增量ti，将待排序列分割成若干长度为m的子序列
4. 对各子表进行直接插入排序
"""

def shell_sort(arr):
    """希尔排序实现"""
    arr = arr.copy()  # 不修改原数组
    steps = []  # 记录排序步骤
    n = len(arr)
    
    # 初始增量gap为长度的一半，每次减半
    gap = n // 2
    while gap > 0:
        steps.append((arr.copy(), gap, -1, f"设置增量为{gap}"))
        
        # 对每个子序列进行插入排序
        for i in range(gap, n):
            temp = arr[i]
            j = i
            
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
                steps.append((arr.copy(), j, j+gap, "移动元素"))
            
            arr[j] = temp
            if j != i:
                steps.append((arr.copy(), j, i, "插入元素"))
        
        gap //= 2
    
    return arr, steps

def print_sort_process(steps):
    """打印排序过程"""
    print("\n排序过程：")
    for i, (arr, pos1, pos2, action) in enumerate(steps, 1):
        print(f"\n第{i}步：")
        print(action)
        if pos2 != -1:
            print(f"位置 {pos1} 和位置 {pos2}")
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
    sorted_numbers, steps = shell_sort(numbers)
    
    # 打印结果
    print(f"\n排序后：{sorted_numbers}")
    
    # 显示排序过程
    print_sort_process(steps) 