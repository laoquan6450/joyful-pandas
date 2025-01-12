#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现稀疏表（Sparse Table）数据结构及其基本操作。

程序分析：
1. 实现稀疏表的基本结构
2. 实现区间最值查询
3. 实现预处理和快速查询
4. 处理RMQ（区间最值查询）问题
"""

import math
from typing import List, Tuple

class SparseTable:
    def __init__(self, arr: List[int]):
        self.arr = arr
        self.n = len(arr)
        self.max_log = int(math.log2(self.n)) + 1
        self.dp = [[0] * self.max_log for _ in range(self.n)]  # dp[i][j] 表示从i开始长度为2^j的区间的最小值
        self.steps = []  # 记录操作步骤
        self._build()
    
    def _build(self):
        """构建稀疏表"""
        # 初始化长度为1的区间
        for i in range(self.n):
            self.dp[i][0] = self.arr[i]
            self.steps.append((i, 0, self.arr[i], "初始化"))
        
        # 动态规划填表
        for j in range(1, self.max_log):
            for i in range(self.n - (1 << j) + 1):
                self.dp[i][j] = min(
                    self.dp[i][j-1],
                    self.dp[i + (1 << (j-1))][j-1]
                )
                self.steps.append((i, j, self.dp[i][j], "填表"))
    
    def query(self, left: int, right: int) -> int:
        """查询区间[left, right]的最小值"""
        # 计算区间长度的log值
        k = int(math.log2(right - left + 1))
        result = min(
            self.dp[left][k],
            self.dp[right - (1 << k) + 1][k]
        )
        self.steps.append((left, right, result, "查询"))
        return result

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, (pos1, pos2, value, operation) in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if operation == "初始化":
            print(f"{operation}：位置 {pos1} 的值为 {value}")
        elif operation == "填表":
            print(f"{operation}：dp[{pos1}][{pos2}] = {value}")
        else:  # 查询
            print(f"{operation}：区间 [{pos1}, {pos2}] 的最小值为 {value}")

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
        
        # 创建稀疏表
        st = SparseTable(numbers)
        
        # 演示区间查询
        while True:
            try:
                print("\n请输入要查询的区间（输入负数退出）：")
                left = int(input("左端点（0-9）："))
                if left < 0:
                    break
                right = int(input("右端点（0-9）："))
                if right < 0:
                    break
                
                if 0 <= left <= right < len(numbers):
                    result = st.query(left, right)
                    print(f"\n区间 [{left}, {right}] 的最小值为：{result}")
                else:
                    print("\n请输入有效的区间范围！")
            except ValueError:
                print("请输入有效的整数！")
        
        # 打印操作过程
        print_operations(st.steps)
        
    except ValueError as e:
        print(f"错误：{str(e)}") 