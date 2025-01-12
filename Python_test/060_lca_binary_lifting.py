#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现基于倍增法的最近公共祖先（LCA Binary Lifting）算法。

程序分析：
1. 实现树的基本结构
2. 实现倍增数组的预处理
3. 实现LCA查询功能
4. 优化查询过程
"""

from typing import List, Dict, Set, Optional
from collections import defaultdict

class TreeNode:
    def __init__(self, val: int):
        self.val = val
        self.children = []  # 子节点列表
        self.depth = 0      # 节点深度

class LCAFinder:
    def __init__(self, n: int):
        self.n = n  # 节点数量
        self.log = 20  # 最大倍增层数
        self.nodes = [TreeNode(i) for i in range(n)]  # 节点列表
        self.parent = [[0] * self.log for _ in range(n)]  # 倍增数组
        self.adj = defaultdict(list)  # 邻接表
        self.steps = []  # 记录操作步骤
    
    def add_edge(self, u: int, v: int) -> None:
        """添加边"""
        self.adj[u].append(v)
        self.adj[v].append(u)
        self.steps.append((u, v, "添加边"))
    
    def _dfs(self, node: int, parent: int, depth: int) -> None:
        """DFS构建树结构"""
        self.nodes[node].depth = depth
        self.parent[node][0] = parent
        
        for child in self.adj[node]:
            if child != parent:
                self.nodes[node].children.append(child)
                self._dfs(child, node, depth + 1)
                self.steps.append((node, child, "处理子节点"))
    
    def build(self, root: int) -> None:
        """构建LCA查询所需的数据结构"""
        # DFS构建树结构
        self._dfs(root, root, 0)
        self.steps.append((root, "开始构建倍增数组"))
        
        # 构建倍增数组
        for j in range(1, self.log):
            for i in range(self.n):
                self.parent[i][j] = self.parent[self.parent[i][j-1]][j-1]
                self.steps.append((i, j, "更新倍增数组"))
    
    def get_lca(self, u: int, v: int) -> int:
        """查询两个节点的最近公共祖先"""
        # 确保u的深度不小于v
        if self.nodes[u].depth < self.nodes[v].depth:
            u, v = v, u
        
        # 将u上升到与v同一深度
        diff = self.nodes[u].depth - self.nodes[v].depth
        for i in range(self.log):
            if diff & (1 << i):
                u = self.parent[u][i]
                self.steps.append((u, v, "调整深度"))
        
        if u == v:
            return u
        
        # 同时上升直到找到LCA
        for i in range(self.log-1, -1, -1):
            if self.parent[u][i] != self.parent[v][i]:
                u = self.parent[u][i]
                v = self.parent[v][i]
                self.steps.append((u, v, "同时上升"))
        
        result = self.parent[u][0]
        self.steps.append((result, "找到LCA"))
        return result

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if len(step) == 2:
            if isinstance(step[0], int):
                print(f"找到LCA：节点 {step[0]}")
            else:
                print(f"{step[1]}：根节点 {step[0]}")
        else:
            u, v, operation = step
            if operation == "添加边":
                print(f"{operation}：{u} - {v}")
            elif operation == "处理子节点":
                print(f"{operation}：父节点 {u}，子节点 {v}")
            elif operation == "更新倍增数组":
                print(f"{operation}：节点 {u}，层数 {v}")
            else:  # 调整深度/同时上升
                print(f"{operation}：当前节点 {u} 和 {v}")

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

if __name__ == '__main__':
    try:
        # 获取节点数量
        n = int(input("请输入节点数量（2-10）："))
        if not (2 <= n <= 10):
            raise ValueError("节点数量必须在2到10之间！")
        
        # 创建LCA查询器
        lca = LCAFinder(n)
        
        # 获取边并构建树
        edges = get_input_edges(n)
        for u, v in edges:
            lca.add_edge(u, v)
        
        # 构建LCA查询所需的数据结构
        root = 0  # 以0为根节点
        lca.build(root)
        
        while True:
            print("\n请选择操作：")
            print("1. 查询LCA")
            print("2. 退出")
            
            choice = input("请输入选择（1-2）：")
            
            if choice == '1':
                u = int(input(f"请输入第一个节点（0-{n-1}）："))
                v = int(input(f"请输入第二个节点（0-{n-1}）："))
                
                if 0 <= u < n and 0 <= v < n:
                    result = lca.get_lca(u, v)
                    print(f"\n节点 {u} 和节点 {v} 的最近公共祖先是：{result}")
                else:
                    print("无效的节点编号！")
            
            elif choice == '2':
                break
            
            else:
                print("无效的选择！")
        
        # 打印操作过程
        print_operations(lca.steps)
        
    except ValueError as e:
        print(f"错误：{str(e)}") 