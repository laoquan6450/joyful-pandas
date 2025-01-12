#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：使用基数排序对输入的10个非负整数进行排序。

程序分析：
1. 取得数组中的最大数，并取得位数
2. 从最低位开始，对数组进行排序
3. 将所有数组按照本位数的大小进行排序
4. 重复步骤2-3直到最高位，即可完成排序
"""

def radix_sort(arr):
    """基数排序实现"""
    if not arr:
        return [], []
    
    # 复制原数组，不修改原数据
    arr = arr.copy()
    steps = []  # 记录排序步骤
    
    # 找到最大值，确定位数
    max_num = max(arr)
    exp = 1  # 当前处理的位数（1代表个位，10代表十位，等等）
    
    while max_num // exp > 0:
        steps.append((arr.copy(), exp, "开始处理", f"按{exp}位排序"))
        
        # 使用计数排序对当前位进行排序
        output = [0] * len(arr)
        count = [0] * 10  # 0-9的计数器
        
        # 统计当前位上每个数字出现的次数
        for i in range(len(arr)):
            digit = (arr[i] // exp) % 10
            count[digit] += 1
            steps.append((arr.copy(), digit, i, f"统计{digit}在位置{i}"))
        
        # 计算实际位置
        for i in range(1, 10):
            count[i] += count[i - 1]
            steps.append((arr.copy(), i, count[i], "累加计数"))
        
        # 构建输出数组
        for i in range(len(arr) - 1, -1, -1):
            digit = (arr[i] // exp) % 10
            output[count[digit] - 1] = arr[i]
            count[digit] -= 1
            steps.append((output.copy(), i, count[digit], f"放置元素{arr[i]}"))
        
        # 复制回原数组
        for i in range(len(arr)):
            arr[i] = output[i]
        
        exp *= 10  # 处理下一位
    
    return arr, steps

def print_sort_process(steps):
    """打印排序过程"""
    print("\n排序过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if len(step) == 4:  # 常规步骤
            arr, pos1, pos2, action = step
            print(action)
            print(f"位置信息：{pos1}, {pos2}")
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
    sorted_numbers, steps = radix_sort(numbers)
    
    # 打印结果
    print(f"\n排序后：{sorted_numbers}")
    
    # 显示排序过程
    print_sort_process(steps) 