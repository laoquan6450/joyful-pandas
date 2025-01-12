#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现二维树状数组（2D Fenwick Tree）及其基本操作。

程序分析：
1. 实现二维树状数组的基本结构
2. 实现点更新和区域查询
3. 实现区域更新和点查询
4. 处理二维前缀和问题
"""

class FenwickTree2D:
    def __init__(self, n: int, m: int):
        self.n = n
        self.m = m
        self.tree = [[0] * (m + 1) for _ in range(n + 1)]
        self.steps = []  # 记录操作步骤
    
    def _lowbit(self, x: int) -> int:
        """获取x的最低位1"""
        return x & (-x)
    
    def update(self, x: int, y: int, delta: int) -> None:
        """更新点(x, y)的值"""
        i = x
        while i <= self.n:
            j = y
            while j <= self.m:
                self.tree[i][j] += delta
                self.steps.append((i, j, delta, "更新点"))
                j += self._lowbit(j)
            i += self._lowbit(i)
    
    def query(self, x: int, y: int) -> int:
        """查询(1,1)到(x,y)的矩形区域和"""
        result = 0
        i = x
        while i > 0:
            j = y
            while j > 0:
                result += self.tree[i][j]
                self.steps.append((i, j, result, "累加查询"))
                j -= self._lowbit(j)
            i -= self._lowbit(i)
        return result
    
    def range_query(self, x1: int, y1: int, x2: int, y2: int) -> int:
        """查询(x1,y1)到(x2,y2)的矩形区域和"""
        return (self.query(x2, y2) - self.query(x2, y1-1) - 
                self.query(x1-1, y2) + self.query(x1-1, y1-1))

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, (x, y, value, operation) in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if operation == "更新点":
            print(f"{operation}：位置({x}, {y})增加值 {value}")
        else:  # 查询
            print(f"{operation}：位置({x}, {y})，当前和为 {value}")

def get_input_matrix():
    """获取用户输入的矩阵"""
    print("请输入3x3矩阵的元素：")
    matrix = []
    for i in range(3):
        row = []
        for j in range(3):
            while True:
                try:
                    num = int(input(f"请输入位置({i+1}, {j+1})的值："))
                    row.append(num)
                    break
                except ValueError:
                    print("请输入有效的整数！")
        matrix.append(row)
    return matrix

if __name__ == '__main__':
    try:
        # 创建二维树状数组
        ft2d = FenwickTree2D(3, 3)
        
        # 获取输入矩阵
        matrix = get_input_matrix()
        print("\n输入的矩阵：")
        for row in matrix:
            print(row)
        
        # 初始化树状数组
        for i in range(3):
            for j in range(3):
                if matrix[i][j] != 0:
                    ft2d.update(i+1, j+1, matrix[i][j])
        
        while True:
            print("\n请选择操作：")
            print("1. 更新点值")
            print("2. 查询区域和")
            print("3. 退出")
            
            choice = input("请输入选择（1-3）：")
            
            if choice == '1':
                x = int(input("请输入x坐标（1-3）："))
                y = int(input("请输入y坐标（1-3）："))
                delta = int(input("请输入要增加的值："))
                ft2d.update(x, y, delta)
                print("更新成功！")
            
            elif choice == '2':
                x1 = int(input("请输入左上角x坐标（1-3）："))
                y1 = int(input("请输入左上角y坐标（1-3）："))
                x2 = int(input("请输入右下角x坐标（1-3）："))
                y2 = int(input("请输入右下角y坐标（1-3）："))
                result = ft2d.range_query(x1, y1, x2, y2)
                print(f"区域和为：{result}")
            
            elif choice == '3':
                break
            
            else:
                print("无效的选择！")
        
        # 打印操作过程
        print_operations(ft2d.steps)
        
    except ValueError as e:
        print(f"错误：{str(e)}") 