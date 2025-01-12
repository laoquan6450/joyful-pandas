#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现二分图问题的解决方案。

程序分析：
1. 实现二分图判定
2. 实现二分图最大匹配
3. 实现带权二分图匹配
4. 优化求解过程
"""

from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict, deque
import time

class BipartiteGraph:
    def __init__(self, vertices: int):
        self.V = vertices  # 顶点数
        self.graph = defaultdict(set)  # 邻接表
        self.weights = {}  # 边的权重
        self.steps = []  # 记录操作步骤
    
    def add_edge(self, u: int, v: int, weight: float = 1.0) -> None:
        """添加边"""
        self.graph[u].add(v)
        self.graph[v].add(u)
        self.weights[(u, v)] = self.weights[(v, u)] = weight
        self.steps.append((u, v, weight, "添加边"))
    
    def is_bipartite(self) -> Tuple[bool, Optional[Dict[int, int]]]:
        """判断是否为二分图，返回(是否二分图, 顶点着色)"""
        colors = {}  # 顶点着色：0和1表示两个部分
        
        def bfs_color(start: int) -> bool:
            """使用BFS对顶点着色"""
            queue = deque([(start, 0)])  # (顶点, 颜色)
            
            while queue:
                vertex, color = queue.popleft()
                if vertex in colors:
                    if colors[vertex] != color:
                        return False
                    continue
                
                colors[vertex] = color
                self.steps.append((vertex, color, "着色"))
                
                for neighbor in self.graph[vertex]:
                    queue.append((neighbor, 1 - color))
            
            return True
        
        # 处理所有连通分量
        for v in range(self.V):
            if v not in colors:
                if not bfs_color(v):
                    return False, None
        
        return True, colors
    
    def maximum_matching(self) -> List[Tuple[int, int]]:
        """匈牙利算法求解二分图最大匹配"""
        # 首先判断是否为二分图
        is_bip, colors = self.is_bipartite()
        if not is_bip:
            return []
        
        # 获取两个部分的顶点
        left = {v for v in range(self.V) if colors[v] == 0}
        matching = {}  # 当前匹配
        
        def augment(v: int, visited: Set[int]) -> bool:
            """寻找增广路径"""
            for u in self.graph[v]:
                if u not in visited:
                    visited.add(u)
                    if u not in matching or augment(matching[u], visited):
                        matching[v] = u
                        matching[u] = v
                        return True
            return False
        
        # 为左部每个顶点寻找增广路径
        for v in left:
            augment(v, {v})
            self.steps.append((v, "尝试增广"))
        
        # 转换为边的列表形式
        edges = []
        used = set()
        for u, v in matching.items():
            if u not in used and v not in used:
                edges.append((min(u, v), max(u, v)))
                used.add(u)
                used.add(v)
                self.steps.append((u, v, "匹配边"))
        
        return edges
    
    def weighted_matching(self) -> List[Tuple[int, int]]:
        """带权二分图最大匹配（匈牙利算法的带权版本）"""
        # 首先判断是否为二分图
        is_bip, colors = self.is_bipartite()
        if not is_bip:
            return []
        
        # 获取两个部分的顶点
        left = {v for v in range(self.V) if colors[v] == 0}
        matching = {}
        
        # 按权重降序排序边
        edges = [(u, v) for u in left for v in self.graph[u]]
        edges.sort(key=lambda e: self.weights[e], reverse=True)
        
        for u, v in edges:
            if u not in matching and v not in matching:
                matching[u] = v
                matching[v] = u
                self.steps.append((u, v, self.weights[(u, v)], "带权匹配"))
        
        # 转换为边的列表形式
        return [(min(u, v), max(u, v)) for u, v in matching.items() if u < v]
    
    def optimize_matching(self) -> List[Tuple[int, int]]:
        """优化的二分图匹配算法"""
        # 预处理：移除孤立顶点
        isolated = set()
        for v in range(self.V):
            if not self.graph[v]:
                isolated.add(v)
                self.steps.append((v, "孤立顶点"))
        
        # 在剩余图上运行匈牙利算法
        remaining_vertices = set(range(self.V)) - isolated
        remaining_graph = BipartiteGraph(self.V)
        
        for v in remaining_vertices:
            for u in self.graph[v]:
                if u in remaining_vertices:
                    remaining_graph.add_edge(v, u, self.weights.get((v, u), 1.0))
        
        return remaining_graph.maximum_matching()

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if len(step) == 2:
            val, operation = step
            if operation == "孤立顶点":
                print(f"{operation}：顶点 {val}")
            elif operation == "尝试增广":
                print(f"尝试为顶点 {val} 寻找增广路径")
        elif len(step) == 3:
            if step[2] == "着色":
                vertex, color, _ = step
                print(f"将顶点 {vertex} 着色为 {color}")
            elif step[2] == "匹配边":
                u, v, _ = step
                print(f"添加匹配边：{u} - {v}")
        elif len(step) == 4:
            if step[3] == "添加边":
                u, v, w, _ = step
                print(f"添加边：{u} - {v}，权重 {w}")
            elif step[3] == "带权匹配":
                u, v, w, _ = step
                print(f"带权匹配：{u} - {v}，权重 {w}")

if __name__ == '__main__':
    try:
        # 获取输入
        V = int(input("请输入顶点数量："))
        E = int(input("请输入边的数量："))
        
        # 创建图
        graph = BipartiteGraph(V)
        
        # 输入边
        print("\n请输入边（每行：起点 终点 权重）：")
        for _ in range(E):
            line = input().strip().split()
            u, v = map(int, line[:2])
            weight = float(line[2]) if len(line) > 2 else 1.0
            
            if 0 <= u < V and 0 <= v < V and u != v:
                graph.add_edge(u, v, weight)
            else:
                print(f"忽略无效边：{u} - {v}")
        
        while True:
            print("\n请选择操作：")
            print("1. 判断二分图")
            print("2. 最大匹配")
            print("3. 带权匹配")
            print("4. 优化算法")
            print("5. 退出")
            
            choice = input("请输入选择（1-5）：")
            
            if choice == '1':
                is_bip, colors = graph.is_bipartite()
                if is_bip:
                    print("\n是二分图！")
                    print("顶点分组：")
                    left = [v for v in range(V) if colors[v] == 0]
                    right = [v for v in range(V) if colors[v] == 1]
                    print(f"左部：{left}")
                    print(f"右部：{right}")
                else:
                    print("\n不是二分图！")
            
            elif choice == '2':
                matching = graph.maximum_matching()
                if matching:
                    print("\n最大匹配：")
                    for u, v in matching:
                        print(f"{u} - {v}")
                    print(f"匹配大小：{len(matching)}")
                else:
                    print("\n图不是二分图或无匹配！")
            
            elif choice == '3':
                matching = graph.weighted_matching()
                if matching:
                    print("\n带权匹配：")
                    total_weight = 0
                    for u, v in matching:
                        weight = graph.weights[(u, v)]
                        total_weight += weight
                        print(f"{u} - {v} (权重: {weight})")
                    print(f"匹配大小：{len(matching)}")
                    print(f"总权重：{total_weight}")
                else:
                    print("\n图不是二分图或无匹配！")
            
            elif choice == '4':
                matching = graph.optimize_matching()
                if matching:
                    print("\n优化匹配：")
                    for u, v in matching:
                        print(f"{u} - {v}")
                    print(f"匹配大小：{len(matching)}")
                else:
                    print("\n图不是二分图或无匹配！")
            
            elif choice == '5':
                break
            
            else:
                print("无效的选择！")
            
            # 打印操作过程
            print_operations(graph.steps)
            graph.steps.clear()  # 清空步骤记录
        
    except ValueError as e:
        print(f"错误：{str(e)}") 