#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：使用计数排序对输入的10个非负整数进行排序。

程序分析：
1. 找出待排序的数组中最大和最小的元素
2. 统计数组中每个值为i的元素出现的次数，存入计数数组C的第i项
3. 对所有的计数累加，从而得到小于等于i的元素个数
4. 反向填充目标数组：将每个元素i放在新数组的第C(i)项，每放一个元素就将C(i)减去1
"""

def counting_sort(arr):
    """计数排序实现"""
    if not arr:
        return [], []
    
    # 复制原数组，不修改原数据
    arr = arr.copy()
    steps = []  # 记录排序步骤
    
    # 找出数组中的最大值和最小值
    max_val = max(arr)
    min_val = min(arr)
    
    # 计算计数数组的大小
    range_of_elements = max_val - min_val + 1
    
    # 创建计数数组并统计每个元素出现的次数
    count = [0] * range_of_elements
    for num in arr:
        count[num - min_val] += 1
        steps.append((arr.copy(), count.copy(), f"统计元素 {num} 的出现次数"))
    
    # 修改计数数组，使其包含实际位置信息
    for i in range(1, len(count)):
        count[i] += count[i - 1]
        steps.append((arr.copy(), count.copy(), f"累加位置信息到索引 {i}"))
    
    # 创建输出数组
    output = [0] * len(arr)
    
    # 构建输出数组
    for i in range(len(arr) - 1, -1, -1):
        current = arr[i]
        position = count[current - min_val] - 1
        output[position] = current
        count[current - min_val] -= 1
        steps.append((output.copy(), i, position, f"放置元素 {current}"))
    
    # 将排序后的数组复制回原数组
    for i in range(len(arr)):
        arr[i] = output[i]
    
    return arr, steps

def print_sort_process(steps):
    """打印排序过程"""
    print("\n排序过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if len(step) == 3:  # 统计或累加步骤
            arr, count, action = step
            print(action)
            print(f"当前数组：{arr}")
            print(f"计数数组：{count}")
        else:  # 放置元素步骤
            arr, pos1, pos2, action = step
            print(action)
            print(f"从位置 {pos1} 到位置 {pos2}")
            print(f"数组变为：{arr}")

def get_input_numbers():
    """获取用户输入的非负整数"""
    numbers = []
    print("请输入10个非负整数：")
    while len(numbers) < 10:
        try:
            num = int(input(f"请输入第{len(numbers)+1}个数字："))
            if num < 0:
                print("请输入非负整数！")
                continue
            numbers.append(num)
        except ValueError:
            print("请输入有效的整数！")
    return numbers

if __name__ == '__main__':
    # 获取输入
    numbers = get_input_numbers()
    print(f"\n原始数组：{numbers}")
    
    # 进行排序
    sorted_numbers, steps = counting_sort(numbers)
    
    # 打印结果
    print(f"\n排序后：{sorted_numbers}")
    
    # 显示排序过程
    print_sort_process(steps) 