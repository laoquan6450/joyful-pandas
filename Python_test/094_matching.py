#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现图匹配问题的解决方案。

程序分析：
1. 实现贪心算法
2. 实现匈牙利算法
3. 实现带权匹配
4. 优化求解过程
"""

from typing import List, Dict, Set, Tuple
from collections import defaultdict
import time

class Graph:
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
    
    def greedy_matching(self) -> List[Tuple[int, int]]:
        """贪心算法求解最大匹配"""
        matching = []  # 存储匹配的边
        used = set()  # 已匹配的顶点
        
        # 按权重降序排序边
        edges = [(u, v) for u in range(self.V) for v in self.graph[u] if u < v]
        edges.sort(key=lambda e: self.weights[e], reverse=True)
        
        for u, v in edges:
            if u not in used and v not in used:
                matching.append((u, v))
                used.add(u)
                used.add(v)
                self.steps.append((u, v, "匹配边"))
        
        return matching
    
    def hungarian_matching(self) -> List[Tuple[int, int]]:
        """匈牙利算法求解最大匹配"""
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
        
        # 为每个未匹配的顶点寻找增广路径
        for v in range(self.V):
            if v not in matching:
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
                self.steps.append((u, v, "匈牙利匹配"))
        
        return edges
    
    def weighted_matching(self) -> List[Tuple[int, int]]:
        """带权最大匹配（使用KM算法的简化版本）"""
        matching = []
        vertex_weights = [0] * self.V  # 顶点权重
        
        # 初始化顶点权重为与其相连的最大边权重
        for v in range(self.V):
            vertex_weights[v] = max((self.weights.get((v, u), 0) for u in self.graph[v]), default=0)
        
        used = set()
        for v in range(self.V):
            if v not in used:
                # 找到权重最大的可行边
                max_weight = -float('inf')
                best_match = None
                
                for u in self.graph[v]:
                    if u not in used:
                        weight = self.weights[(v, u)]
                        if weight >= vertex_weights[v] + vertex_weights[u]:
                            if weight > max_weight:
                                max_weight = weight
                                best_match = u
                
                if best_match is not None:
                    matching.append((v, best_match))
                    used.add(v)
                    used.add(best_match)
                    self.steps.append((v, best_match, max_weight, "带权匹配"))
        
        return matching
    
    def optimize_matching(self) -> List[Tuple[int, int]]:
        """优化的匹配算法"""
        # 预处理：移除孤立顶点
        isolated = set()
        for v in range(self.V):
            if not self.graph[v]:
                isolated.add(v)
                self.steps.append((v, "孤立顶点"))
        
        # 在剩余图上运行匈牙利算法
        remaining_vertices = set(range(self.V)) - isolated
        remaining_graph = Graph(self.V)
        
        for v in remaining_vertices:
            for u in self.graph[v]:
                if u in remaining_vertices:
                    remaining_graph.add_edge(v, u, self.weights.get((v, u), 1.0))
        
        return remaining_graph.hungarian_matching()

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
            if step[2] == "匹配边":
                u, v, _ = step
                print(f"添加匹配边：{u} - {v}")
            elif step[2] == "匈牙利匹配":
                u, v, _ = step
                print(f"匈牙利算法匹配：{u} - {v}")
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
        graph = Graph(V)
        
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
            print("\n请选择算法：")
            print("1. 贪心算法")
            print("2. 匈牙利算法")
            print("3. 带权匹配")
            print("4. 优化算法")
            print("5. 退出")
            
            choice = input("请输入选择（1-5）：")
            
            if choice == '1':
                matching = graph.greedy_matching()
                print("\n匹配边：")
                for u, v in matching:
                    print(f"{u} - {v}")
                print(f"匹配大小：{len(matching)}")
            
            elif choice == '2':
                matching = graph.hungarian_matching()
                print("\n匹配边：")
                for u, v in matching:
                    print(f"{u} - {v}")
                print(f"匹配大小：{len(matching)}")
            
            elif choice == '3':
                matching = graph.weighted_matching()
                print("\n匹配边：")
                total_weight = 0
                for u, v in matching:
                    weight = graph.weights[(u, v)]
                    total_weight += weight
                    print(f"{u} - {v} (权重: {weight})")
                print(f"匹配大小：{len(matching)}")
                print(f"总权重：{total_weight}")
            
            elif choice == '4':
                matching = graph.optimize_matching()
                print("\n匹配边：")
                for u, v in matching:
                    print(f"{u} - {v}")
                print(f"匹配大小：{len(matching)}")
            
            elif choice == '5':
                break
            
            else:
                print("无效的选择！")
            
            # 打印操作过程
            print_operations(graph.steps)
            graph.steps.clear()  # 清空步骤记录
        
    except ValueError as e:
        print(f"错误：{str(e)}") 