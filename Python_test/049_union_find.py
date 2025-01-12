#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现并查集（Union Find）数据结构及其基本操作。

程序分析：
1. 实现基本的并查集结构
2. 实现路径压缩优化
3. 实现按秩合并优化
4. 处理动态连通性问题
"""

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))  # 初始时每个节点的父节点是自己
        self.rank = [0] * n  # 树的高度
        self.count = n  # 连通分量数量
        self.steps = []  # 记录操作步骤
    
    def find(self, x: int) -> int:
        """查找x的根节点（带路径压缩）"""
        if self.parent[x] != x:
            # 路径压缩：将路径上的所有节点直接连接到根节点
            original_parent = self.parent[x]
            self.parent[x] = self.find(self.parent[x])
            self.steps.append((x, original_parent, self.parent[x], "路径压缩"))
        return self.parent[x]
    
    def union(self, x: int, y: int) -> bool:
        """合并x和y所在的集合（按秩合并）"""
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            self.steps.append((x, y, -1, "已在同一集合"))
            return False
        
        # 按秩合并：将较小的树连接到较大的树上
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
            self.steps.append((root_x, root_y, 1, "合并到右树"))
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
            self.steps.append((root_y, root_x, 2, "合并到左树"))
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
            self.steps.append((root_y, root_x, 3, "合并并增加高度"))
        
        self.count -= 1
        return True
    
    def connected(self, x: int, y: int) -> bool:
        """判断x和y是否连通"""
        return self.find(x) == self.find(y)

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, (x, y, op_type, operation) in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if op_type == -1:
            print(f"{operation}：节点 {x} 和节点 {y}")
        elif op_type == 1:
            print(f"{operation}：将节点 {x} 合并到节点 {y} 的树中")
        elif op_type == 2:
            print(f"{operation}：将节点 {y} 合并到节点 {x} 的树中")
        elif op_type == 3:
            print(f"{operation}：将节点 {x} 合并到节点 {y} 的树中并增加树高")
        else:
            print(f"{operation}：将节点 {x} 的父节点从 {y} 改为 {op_type}")

def test_union_find():
    """测试并查集功能"""
    n = 10  # 节点数量
    uf = UnionFind(n)
    
    # 演示一些合并操作
    pairs = [(1, 2), (3, 4), (5, 6), (1, 6), (7, 8), (8, 9)]
    for x, y in pairs:
        print(f"\n合并节点 {x} 和节点 {y}：")
        if uf.union(x, y):
            print("合并成功")
        else:
            print("已在同一集合中")
    
    # 测试连通性
    test_pairs = [(1, 6), (3, 5), (7, 9)]
    for x, y in test_pairs:
        print(f"\n测试节点 {x} 和节点 {y} 是否连通：", end=' ')
        print("是" if uf.connected(x, y) else "否")
    
    # 打印操作过程
    print_operations(uf.steps)

if __name__ == '__main__':
    test_union_find() 