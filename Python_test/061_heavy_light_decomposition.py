#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现树链剖分（Heavy Light Decomposition）及其基本操作。

程序分析：
1. 实现树的重链剖分
2. 实现路径查询和更新
3. 实现子树查询和更新
4. 优化查询和更新操作
"""

from typing import List, Dict
from collections import defaultdict

class HLDNode:
    def __init__(self, val: int):
        self.val = val          # 节点值
        self.size = 1          # 子树大小
        self.depth = 0         # 节点深度
        self.parent = -1       # 父节点
        self.heavy = -1        # 重儿子
        self.chain_top = 0     # 所在重链的顶部节点
        self.pos = 0           # 在线段树中的位置

class HeavyLightDecomposition:
    def __init__(self, n: int):
        self.n = n
        self.nodes = [HLDNode(0) for _ in range(n)]
        self.adj = defaultdict(list)  # 邻接表
        self.seg_tree = [0] * (4 * n)  # 线段树
        self.pos_cnt = 0  # 用于DFS序
        self.steps = []  # 记录操作步骤
    
    def add_edge(self, u: int, v: int) -> None:
        """添加边"""
        self.adj[u].append(v)
        self.adj[v].append(u)
        self.steps.append((u, v, "添加边"))
    
    def _dfs_size(self, u: int, parent: int, depth: int) -> int:
        """计算子树大小和重儿子"""
        self.nodes[u].parent = parent
        self.nodes[u].depth = depth
        size = 1
        max_child_size = 0
        
        for v in self.adj[u]:
            if v != parent:
                child_size = self._dfs_size(v, u, depth + 1)
                size += child_size
                if child_size > max_child_size:
                    max_child_size = child_size
                    self.nodes[u].heavy = v
                self.steps.append((u, v, "计算子树"))
        
        self.nodes[u].size = size
        return size
    
    def _dfs_decompose(self, u: int, top: int) -> None:
        """进行重链剖分"""
        self.nodes[u].chain_top = top
        self.nodes[u].pos = self.pos_cnt
        self.pos_cnt += 1
        self.steps.append((u, top, "剖分节点"))
        
        # 优先处理重儿子，保持重链
        if self.nodes[u].heavy != -1:
            self._dfs_decompose(self.nodes[u].heavy, top)
            
        # 处理轻儿子，每个轻儿子都是新链的开始
        for v in self.adj[u]:
            if v != self.nodes[u].parent and v != self.nodes[u].heavy:
                self._dfs_decompose(v, v)
    
    def build(self, root: int) -> None:
        """构建重链剖分"""
        self._dfs_size(root, root, 0)
        self._dfs_decompose(root, root)
        self.steps.append((root, "完成剖分"))
    
    def _update_segment(self, node: int, start: int, end: int, pos: int, val: int) -> None:
        """更新线段树"""
        if start == end:
            self.seg_tree[node] = val
            self.steps.append((pos, val, "更新节点值"))
            return
        
        mid = (start + end) // 2
        if pos <= mid:
            self._update_segment(2*node, start, mid, pos, val)
        else:
            self._update_segment(2*node+1, mid+1, end, pos, val)
        
        self.seg_tree[node] = self.seg_tree[2*node] + self.seg_tree[2*node+1]
    
    def _query_segment(self, node: int, start: int, end: int, l: int, r: int) -> int:
        """查询线段树区间和"""
        if r < start or l > end:
            return 0
        if l <= start and end <= r:
            return self.seg_tree[node]
        
        mid = (start + end) // 2
        return (self._query_segment(2*node, start, mid, l, r) +
                self._query_segment(2*node+1, mid+1, end, l, r))
    
    def update_node(self, u: int, val: int) -> None:
        """更新节点值"""
        pos = self.nodes[u].pos
        self._update_segment(1, 0, self.n-1, pos, val)
    
    def query_path(self, u: int, v: int) -> int:
        """查询路径上的节点值之和"""
        result = 0
        
        # 将两个节点提升到同一条重链上
        while self.nodes[u].chain_top != self.nodes[v].chain_top:
            if self.nodes[self.nodes[u].chain_top].depth < self.nodes[self.nodes[v].chain_top].depth:
                u, v = v, u
            
            top = self.nodes[u].chain_top
            result += self._query_segment(1, 0, self.n-1,
                                       self.nodes[top].pos,
                                       self.nodes[u].pos)
            self.steps.append((u, v, "查询重链"))
            u = self.nodes[top].parent
        
        # 现在u和v在同一条重链上，计算最后一段
        if self.nodes[u].depth > self.nodes[v].depth:
            u, v = v, u
        result += self._query_segment(1, 0, self.n-1,
                                   self.nodes[u].pos,
                                   self.nodes[v].pos)
        self.steps.append((u, v, "查询最终区间"))
        return result

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if len(step) == 2:
            print(f"完成剖分：根节点 {step[0]}")
        else:
            u, v, operation = step
            if operation == "添加边":
                print(f"{operation}：{u} - {v}")
            elif operation == "计算子树":
                print(f"{operation}：父节点 {u}，子节点 {v}")
            elif operation == "剖分节点":
                print(f"{operation}：节点 {u}，链顶 {v}")
            elif operation == "更新节点值":
                print(f"{operation}：位置 {u}，值 {v}")
            elif operation.startswith("查询"):
                print(f"{operation}：节点 {u} 到 {v}")

def get_input_edges(n: int) -> List[tuple]:
    """获取用户输入的边"""
    edges = []
    print(f"\n请输入{n-1}条边（每条边输入两个节点编号，范围0-{n-1}）：")
    while len(edges) < n - 1:
        try:
            u = int(input(f"请输入第{len(edges)+1}条边的起点："))
            v = int(input(f"请输入第{len(edges)+1}条边的终点："))
            if not (0 <= u < n and 0 <= v < n):
                print(f"节点编号必须在0到{n-1}之间！")
                continue
            if (u, v) in edges or (v, u) in edges:
                print("该边已存在！")
                continue
            edges.append((u, v))
        except ValueError:
            print("请输入有效的整数！")
    return edges

def get_input_values(n: int) -> List[int]:
    """获取用户输入的节点值"""
    values = []
    print("\n请输入每个节点的初始值：")
    while len(values) < n:
        try:
            val = int(input(f"请输入节点{len(values)}的值："))
            values.append(val)
        except ValueError:
            print("请输入有效的整数！")
    return values

if __name__ == '__main__':
    try:
        # 获取节点数量
        n = int(input("请输入节点数量（2-10）："))
        if not (2 <= n <= 10):
            raise ValueError("节点数量必须在2到10之间！")
        
        # 创建树链剖分对象
        hld = HeavyLightDecomposition(n)
        
        # 获取边并构建树
        edges = get_input_edges(n)
        for u, v in edges:
            hld.add_edge(u, v)
        
        # 构建树链剖分
        root = 0  # 以0为根节点
        hld.build(root)
        
        # 获取节点初始值并更新
        values = get_input_values(n)
        for i, val in enumerate(values):
            hld.update_node(i, val)
        
        while True:
            print("\n请选择操作：")
            print("1. 更新节点值")
            print("2. 查询路径和")
            print("3. 退出")
            
            choice = input("请输入选择（1-3）：")
            
            if choice == '1':
                try:
                    u = int(input(f"请输入要更新的节点（0-{n-1}）："))
                    if not (0 <= u < n):
                        print("无效的节点编号！")
                        continue
                    val = int(input("请输入新的值："))
                    hld.update_node(u, val)
                    print("更新成功！")
                except ValueError:
                    print("请输入有效的整数！")
            
            elif choice == '2':
                try:
                    u = int(input(f"请输入路径的起点（0-{n-1}）："))
                    v = int(input(f"请输入路径的终点（0-{n-1}）："))
                    if not (0 <= u < n and 0 <= v < n):
                        print("无效的节点编号！")
                        continue
                    result = hld.query_path(u, v)
                    print(f"\n路径 {u} 到 {v} 的节点值之和为：{result}")
                except ValueError:
                    print("请输入有效的整数！")
            
            elif choice == '3':
                break
            
            else:
                print("无效的选择！")
        
        # 打印操作过程
        print_operations(hld.steps)
        
    except ValueError as e:
        print(f"错误：{str(e)}") 