#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现树状数组（Binary Indexed Tree）及其基本操作。

程序分析：
1. 实现树状数组的基本结构
2. 实现单点更新和区间查询
3. 实现区间更新和单点查询
4. 处理前缀和问题
"""

class BinaryIndexedTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [0] * (self.n + 1)
        self.arr = arr.copy()
        self.steps = []  # 记录操作步骤
        self._build()
    
    def _lowbit(self, x):
        """获取x的最低位1"""
        return x & (-x)
    
    def _build(self):
        """构建树状数组"""
        for i in range(self.n):
            self.update(i + 1, self.arr[i])
            self.steps.append((i + 1, self.arr[i], "初始化节点"))
    
    def update(self, index: int, delta: int) -> None:
        """更新单点值"""
        while index <= self.n:
            self.tree[index] += delta
            self.steps.append((index, delta, "更新节点"))
            index += self._lowbit(index)
    
    def query(self, index: int) -> int:
        """查询前缀和"""
        result = 0
        while index > 0:
            result += self.tree[index]
            self.steps.append((index, result, "累加查询"))
            index -= self._lowbit(index)
        return result
    
    def range_query(self, left: int, right: int) -> int:
        """查询区间和"""
        return self.query(right) - self.query(left - 1)

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, (index, value, operation) in enumerate(steps, 1):
        print(f"\n第{i}步：")
        print(f"{operation}：位置 {index}，值 {value}")

def get_input_numbers():
    """获取用户输入的数字"""
    numbers = []
    print("请输入10个数字：")
    while len(numbers) < 10:
        try:
            num = int(input(f"请输入第{len(numbers)+1}个数字："))
            numbers.append(num)
        except ValueError:
            print("请输入有效的整数！")
    return numbers

if __name__ == '__main__':
    try:
        # 获取输入
        numbers = get_input_numbers()
        print(f"\n原始数组：{numbers}")
        
        # 创建树状数组
        bit = BinaryIndexedTree(numbers)
        
        # 演示单点更新
        index = int(input("\n请输入要更新的位置（1-10）："))
        delta = int(input("请输入要增加的值："))
        bit.update(index, delta)
        
        # 演示区间查询
        left = int(input("\n请输入查询区间的左端点（1-10）："))
        right = int(input("请输入查询区间的右端点（1-10）："))
        result = bit.range_query(left, right)
        print(f"\n区间 [{left}, {right}] 的和为：{result}")
        
        # 打印操作过程
        print_operations(bit.steps)
        
    except ValueError as e:
        print(f"错误：{str(e)}") 