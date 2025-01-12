#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：使用堆排序对输入的10个数进行排序。

程序分析：
1. 创建一个堆 H[0……n-1]
2. 把堆首（最大值）和堆尾互换
3. 把堆的尺寸缩小1，并调用shift_down(0)，目的是把新的数组顶端数据调整到相应位置
4. 重复步骤2，直到堆的尺寸为1
"""

def heap_sort(arr):
    """堆排序实现"""
    arr = arr.copy()  # 不修改原数组
    steps = []  # 记录排序步骤
    
    def heapify(arr, n, i):
        """构建最大堆"""
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        if left < n and arr[left] > arr[largest]:
            largest = left
        
        if right < n and arr[right] > arr[largest]:
            largest = right
        
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            steps.append((arr.copy(), i, largest, "调整堆"))
            heapify(arr, n, largest)
    
    # 构建最大堆
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    
    # 逐个取出堆顶元素
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        steps.append((arr.copy(), 0, i, "交换堆顶"))
        heapify(arr, i, 0)
    
    return arr, steps

def print_sort_process(steps):
    """打印排序过程"""
    print("\n排序过程：")
    for i, (arr, pos1, pos2, action) in enumerate(steps, 1):
        print(f"\n第{i}步：")
        print(f"{action}：位置 {pos1} 和位置 {pos2}")
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
    sorted_numbers, steps = heap_sort(numbers)
    
    # 打印结果
    print(f"\n排序后：{sorted_numbers}")
    
    # 显示排序过程
    print_sort_process(steps) 