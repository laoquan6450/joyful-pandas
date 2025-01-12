#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：使用桶排序对输入的10个浮点数（范围在0到1之间）进行排序。

程序分析：
1. 创建n个桶（这里使用10个）
2. 遍历数组，将每个数放入对应的桶中
3. 对每个桶内的数据进行排序
4. 将所有桶中的数据按顺序合并
"""

def bucket_sort(arr, bucket_size=10):
    """桶排序实现"""
    if not arr:
        return [], []
    
    # 复制原数组，不修改原数据
    arr = arr.copy()
    steps = []  # 记录排序步骤
    
    # 创建桶
    buckets = [[] for _ in range(bucket_size)]
    
    # 将数据分配到桶中
    for num in arr:
        if not 0 <= num <= 1:
            raise ValueError("数值必须在0到1之间")
        
        bucket_index = int(num * bucket_size)
        if bucket_index == bucket_size:  # 处理num = 1的情况
            bucket_index -= 1
            
        buckets[bucket_index].append(num)
        steps.append((buckets.copy(), num, bucket_index, "放入桶中"))
    
    # 对每个桶进行排序
    result = []
    for i, bucket in enumerate(buckets):
        if bucket:
            bucket.sort()
            steps.append((buckets.copy(), i, -1, f"对桶 {i} 排序"))
            result.extend(bucket)
    
    # 将结果复制回原数组
    for i in range(len(arr)):
        arr[i] = result[i]
        steps.append((arr.copy(), i, result[i], "合并结果"))
    
    return arr, steps

def print_sort_process(steps):
    """打印排序过程"""
    print("\n排序过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if isinstance(step[0][0], list):  # 桶操作
            buckets, num, bucket_index, action = step
            print(action)
            if bucket_index != -1:
                print(f"数值 {num} -> 桶 {bucket_index}")
            print("当前桶状态：")
            for j, bucket in enumerate(buckets):
                if bucket:
                    print(f"桶 {j}: {bucket}")
        else:  # 合并操作
            arr, pos, val, action = step
            print(f"{action}: 位置 {pos} = {val}")
            print(f"数组变为：{arr}")

def get_input_numbers():
    """获取用户输入的浮点数"""
    numbers = []
    print("请输入10个0到1之间的浮点数：")
    while len(numbers) < 10:
        try:
            num = float(input(f"请输入第{len(numbers)+1}个数字："))
            if not 0 <= num <= 1:
                print("请输入0到1之间的数！")
                continue
            numbers.append(num)
        except ValueError:
            print("请输入有效的浮点数！")
    return numbers

if __name__ == '__main__':
    try:
        # 获取输入
        numbers = get_input_numbers()
        print(f"\n原始数组：{numbers}")
        
        # 进行排序
        sorted_numbers, steps = bucket_sort(numbers)
        
        # 打印结果
        print(f"\n排序后：{sorted_numbers}")
        
        # 显示排序过程
        print_sort_process(steps)
        
    except ValueError as e:
        print(f"错误：{str(e)}") 