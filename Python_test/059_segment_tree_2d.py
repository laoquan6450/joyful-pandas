#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现二维线段树（2D Segment Tree）及其基本操作。

程序分析：
1. 实现二维线段树的节点结构
2. 实现区域查询和更新操作
3. 实现懒惰传播机制
4. 优化空间使用
"""

from typing import List, Tuple

class Node:
    def __init__(self):
        self.sum = 0      # 区域和
        self.lazy = 0     # 懒惰标记
        self.tl = None    # 左上子节点
        self.tr = None    # 右上子节点
        self.bl = None    # 左下子节点
        self.br = None    # 右下子节点

class SegmentTree2D:
    def __init__(self, matrix: List[List[int]]):
        self.matrix = matrix
        self.n = len(matrix)
        self.m = len(matrix[0]) if matrix else 0
        self.root = Node()
        self.steps = []  # 记录操作步骤
        self._build(self.root, 0, 0, self.n-1, self.m-1)
    
    def _build(self, node: Node, row1: int, col1: int, row2: int, col2: int) -> None:
        """构建二维线段树"""
        if row1 == row2 and col1 == col2:
            node.sum = self.matrix[row1][col1]
            self.steps.append(((row1, col1), node.sum, "创建叶节点"))
            return
        
        # 计算中点
        row_mid = (row1 + row2) // 2
        col_mid = (col1 + col2) // 2
        
        # 创建子节点
        node.tl = Node()
        node.tr = Node()
        node.bl = Node()
        node.br = Node()
        
        # 递归构建子树
        if row1 <= row_mid:
            if col1 <= col_mid:
                self._build(node.tl, row1, col1, row_mid, col_mid)
            if col_mid + 1 <= col2:
                self._build(node.tr, row1, col_mid+1, row_mid, col2)
        if row_mid + 1 <= row2:
            if col1 <= col_mid:
                self._build(node.bl, row_mid+1, col1, row2, col_mid)
            if col_mid + 1 <= col2:
                self._build(node.br, row_mid+1, col_mid+1, row2, col2)
        
        # 更新当前节点的和
        node.sum = (node.tl.sum if node.tl else 0) + \
                  (node.tr.sum if node.tr else 0) + \
                  (node.bl.sum if node.bl else 0) + \
                  (node.br.sum if node.br else 0)
        self.steps.append(((row1, col1, row2, col2), node.sum, "合并节点"))
    
    def _push_down(self, node: Node, row1: int, col1: int, row2: int, col2: int) -> None:
        """下推懒惰标记"""
        if not node or node.lazy == 0:
            return
        
        row_mid = (row1 + row2) // 2
        col_mid = (col1 + col2) // 2
        
        # 更新子节点的懒惰标记和值
        for child in [node.tl, node.tr, node.bl, node.br]:
            if child:
                child.lazy += node.lazy
                area = ((row_mid - row1 + 1) * (col_mid - col1 + 1))
                child.sum += node.lazy * area
                self.steps.append(("下推懒惰标记", node.lazy))
        
        node.lazy = 0
    
    def update_range(self, row1: int, col1: int, row2: int, col2: int, val: int) -> None:
        """更新区域值"""
        self._update(self.root, 0, 0, self.n-1, self.m-1, row1, col1, row2, col2, val)
    
    def _update(self, node: Node, row1: int, col1: int, row2: int, col2: int,
                qrow1: int, qcol1: int, qrow2: int, qcol2: int, val: int) -> None:
        """递归更新区域"""
        if not node or row1 > qrow2 or row2 < qrow1 or col1 > qcol2 or col2 < qcol1:
            return
        
        if qrow1 <= row1 and row2 <= qrow2 and qcol1 <= col1 and col2 <= qcol2:
            area = (row2 - row1 + 1) * (col2 - col1 + 1)
            node.sum += val * area
            node.lazy += val
            self.steps.append(((row1, col1, row2, col2), val, "更新区域"))
            return
        
        self._push_down(node, row1, col1, row2, col2)
        
        row_mid = (row1 + row2) // 2
        col_mid = (col1 + col2) // 2
        
        self._update(node.tl, row1, col1, row_mid, col_mid,
                    qrow1, qcol1, qrow2, qcol2, val)
        self._update(node.tr, row1, col_mid+1, row_mid, col2,
                    qrow1, qcol1, qrow2, qcol2, val)
        self._update(node.bl, row_mid+1, col1, row2, col_mid,
                    qrow1, qcol1, qrow2, qcol2, val)
        self._update(node.br, row_mid+1, col_mid+1, row2, col2,
                    qrow1, qcol1, qrow2, qcol2, val)
        
        node.sum = (node.tl.sum if node.tl else 0) + \
                  (node.tr.sum if node.tr else 0) + \
                  (node.bl.sum if node.bl else 0) + \
                  (node.br.sum if node.br else 0)
    
    def query_range(self, row1: int, col1: int, row2: int, col2: int) -> int:
        """查询区域和"""
        return self._query(self.root, 0, 0, self.n-1, self.m-1, row1, col1, row2, col2)
    
    def _query(self, node: Node, row1: int, col1: int, row2: int, col2: int,
               qrow1: int, qcol1: int, qrow2: int, qcol2: int) -> int:
        """递归查询区域"""
        if not node or row1 > qrow2 or row2 < qrow1 or col1 > qcol2 or col2 < qcol1:
            return 0
        
        if qrow1 <= row1 and row2 <= qrow2 and qcol1 <= col1 and col2 <= qcol2:
            self.steps.append(((row1, col1, row2, col2), node.sum, "查询区域"))
            return node.sum
        
        self._push_down(node, row1, col1, row2, col2)
        
        row_mid = (row1 + row2) // 2
        col_mid = (col1 + col2) // 2
        
        total = 0
        total += self._query(node.tl, row1, col1, row_mid, col_mid,
                           qrow1, qcol1, qrow2, qcol2)
        total += self._query(node.tr, row1, col_mid+1, row_mid, col2,
                           qrow1, qcol1, qrow2, qcol2)
        total += self._query(node.bl, row_mid+1, col1, row2, col_mid,
                           qrow1, qcol1, qrow2, qcol2)
        total += self._query(node.br, row_mid+1, col_mid+1, row2, col2,
                           qrow1, qcol1, qrow2, qcol2)
        return total

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if step[0] == "下推懒惰标记":
            print(f"下推懒惰标记：{step[1]}")
        else:
            coords, val, operation = step
            if operation == "创建叶节点":
                print(f"{operation}：位置 {coords}，值 {val}")
            elif operation == "合并节点":
                print(f"{operation}：区域 {coords}，和为 {val}")
            elif operation == "更新区域":
                print(f"{operation}：区域 {coords}，增加值 {val}")
            else:  # 查询区域
                print(f"{operation}：区域 {coords}，结果 {val}")

def get_input_matrix():
    """获取用户输入的矩阵"""
    try:
        n = int(input("请输入矩阵的行数（1-5）："))
        m = int(input("请输入矩阵的列数（1-5）："))
        if not (1 <= n <= 5 and 1 <= m <= 5):
            raise ValueError("矩阵大小应在1到5之间")
        
        print(f"\n请输入{n}x{m}矩阵的元素：")
        matrix = []
        for i in range(n):
            row = []
            for j in range(m):
                val = int(input(f"请输入位置({i},{j})的值："))
                row.append(val)
            matrix.append(row)
        return matrix
    except ValueError as e:
        raise ValueError("请输入有效的整数！")

if __name__ == '__main__':
    try:
        # 获取输入矩阵
        matrix = get_input_matrix()
        print("\n输入的矩阵：")
        for row in matrix:
            print(row)
        
        # 创建二维线段树
        st2d = SegmentTree2D(matrix)
        
        while True:
            print("\n请选择操作：")
            print("1. 更新区域值")
            print("2. 查询区域和")
            print("3. 退出")
            
            choice = input("请输入选择（1-3）：")
            
            if choice == '1':
                print("\n请输入要更新的区域坐标（从0开始）：")
                row1 = int(input("左上角行号："))
                col1 = int(input("左上角列号："))
                row2 = int(input("右下角行号："))
                col2 = int(input("右下角列号："))
                val = int(input("请输入要增加的值："))
                
                if 0 <= row1 <= row2 < len(matrix) and \
                   0 <= col1 <= col2 < len(matrix[0]):
                    st2d.update_range(row1, col1, row2, col2, val)
                    print("更新成功！")
                else:
                    print("无效的区域范围！")
            
            elif choice == '2':
                print("\n请输入要查询的区域坐标（从0开始）：")
                row1 = int(input("左上角行号："))
                col1 = int(input("左上角列号："))
                row2 = int(input("右下角行号："))
                col2 = int(input("右下角列号："))
                
                if 0 <= row1 <= row2 < len(matrix) and \
                   0 <= col1 <= col2 < len(matrix[0]):
                    result = st2d.query_range(row1, col1, row2, col2)
                    print(f"\n区域和为：{result}")
                else:
                    print("无效的区域范围！")
            
            elif choice == '3':
                break
            
            else:
                print("无效的选择！")
        
        # 打印操作过程
        print_operations(st2d.steps)
        
    except ValueError as e:
        print(f"错误：{str(e)}") 