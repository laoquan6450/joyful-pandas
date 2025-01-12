#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现独立集问题的解决方案。

程序分析：
1. 实现贪心算法
2. 实现近似算法
3. 实现回溯算法
4. 优化求解过程
"""

from typing import List, Set, Dict, Tuple
from collections import defaultdict
import time

class Graph:
    def __init__(self, vertices: int):
        self.V = vertices  # 顶点数
        self.graph = defaultdict(set)  # 邻接表
        self.steps = []  # 记录操作步骤
    
    def add_edge(self, u: int, v: int) -> None:
        """添加边"""
        self.graph[u].add(v)
        self.graph[v].add(u)
        self.steps.append((u, v, "添加边"))
    
    def get_neighbors(self, vertex: int) -> Set[int]:
        """获取顶点的邻居"""
        return self.graph[vertex]
    
    def greedy_independent_set(self) -> Set[int]:
        """贪心算法求解独立集"""
        # 复制图，以便在处理过程中移除顶点
        remaining = set(range(self.V))
        independent_set = set()
        
        while remaining:
            # 找到度数最小的顶点
            min_degree = float('inf')
            best_vertex = None
            
            for v in remaining:
                degree = len(self.graph[v] & remaining)
                if degree < min_degree:
                    min_degree = degree
                    best_vertex = v
            
            if best_vertex is None:
                break
            
            # 将顶点加入独立集
            independent_set.add(best_vertex)
            # 移除该顶点及其邻居
            remaining.remove(best_vertex)
            remaining -= self.get_neighbors(best_vertex)
            self.steps.append((best_vertex, min_degree, "选择顶点"))
        
        return independent_set
    
    def approximate_independent_set(self) -> Set[int]:
        """2-近似算法求解独立集"""
        remaining = set(range(self.V))
        independent_set = set()
        
        while remaining:
            # 随机选择一个顶点
            vertex = next(iter(remaining))
            
            # 将顶点加入独立集
            independent_set.add(vertex)
            self.steps.append((vertex, "近似选择"))
            
            # 移除该顶点及其邻居
            remaining.remove(vertex)
            remaining -= self.get_neighbors(vertex)
        
        return independent_set
    
    def backtrack_independent_set(self, max_time: float = 5.0) -> Set[int]:
        """回溯算法求解独立集（带时间限制）"""
        start_time = time.time()
        max_independent = set()  # 初始解
        
        def is_independent_set(vertices: Set[int]) -> bool:
            """检查是否是有效的独立集"""
            for v in vertices:
                if vertices & self.get_neighbors(v):
                    return False
            return True
        
        def backtrack_util(curr_vertex: int, curr_set: Set[int]):
            nonlocal max_independent
            
            # 检查时间限制
            if time.time() - start_time > max_time:
                return
            
            # 到达最后一个顶点
            if curr_vertex == self.V:
                if len(curr_set) > len(max_independent):
                    max_independent = curr_set.copy()
                    self.steps.append((len(max_independent), "更新最优解"))
                return
            
            # 不选当前顶点
            backtrack_util(curr_vertex + 1, curr_set)
            
            # 如果可以选择当前顶点
            if not (curr_set & self.get_neighbors(curr_vertex)):
                curr_set.add(curr_vertex)
                backtrack_util(curr_vertex + 1, curr_set)
                curr_set.remove(curr_vertex)
        
        backtrack_util(0, set())
        return max_independent
    
    def optimize_independent_set(self) -> Set[int]:
        """优化的独立集求解方案"""
        # 预处理：找出孤立顶点（必然在最大独立集中）
        must_include = set()
        
        for v in range(self.V):
            if not self.graph[v]:
                must_include.add(v)
                self.steps.append((v, "孤立顶点"))
        
        # 在剩余图上运行贪心算法
        remaining_vertices = set(range(self.V)) - must_include
        remaining_graph = Graph(self.V)
        
        for v in remaining_vertices:
            for u in self.graph[v]:
                if u in remaining_vertices:
                    remaining_graph.add_edge(v, u)
        
        additional_set = remaining_graph.greedy_independent_set()
        return must_include | additional_set

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if len(step) == 2:
            val, operation = step
            if operation == "孤立顶点":
                print(f"{operation}：顶点 {val}")
            elif operation == "近似选择":
                print(f"{operation}：顶点 {val}")
            elif operation == "更新最优解":
                print(f"{operation}：当前大小 {val}")
        elif len(step) == 3:
            if step[2] == "添加边":
                u, v, _ = step
                print(f"添加边：{u} - {v}")
            elif step[2] == "选择顶点":
                vertex, degree, _ = step
                print(f"选择顶点：{vertex}，度数 {degree}")

if __name__ == '__main__':
    try:
        # 获取输入
        V = int(input("请输入顶点数量："))
        E = int(input("请输入边的数量："))
        
        # 创建图
        graph = Graph(V)
        
        # 输入边
        print("\n请输入边（每行两个顶点编号，用空格分隔）：")
        for _ in range(E):
            u, v = map(int, input().strip().split())
            if 0 <= u < V and 0 <= v < V and u != v:
                graph.add_edge(u, v)
            else:
                print(f"忽略无效边：{u} - {v}")
        
        while True:
            print("\n请选择算法：")
            print("1. 贪心算法")
            print("2. 近似算法")
            print("3. 回溯算法")
            print("4. 优化算法")
            print("5. 退出")
            
            choice = input("请输入选择（1-5）：")
            
            if choice == '1':
                independent_set = graph.greedy_independent_set()
                print("\n独立集：", sorted(independent_set))
                print(f"独立集大小：{len(independent_set)}")
            
            elif choice == '2':
                independent_set = graph.approximate_independent_set()
                print("\n独立集：", sorted(independent_set))
                print(f"独立集大小：{len(independent_set)}")
            
            elif choice == '3':
                max_time = float(input("请输入最大运行时间（秒）："))
                independent_set = graph.backtrack_independent_set(max_time)
                print("\n独立集：", sorted(independent_set))
                print(f"独立集大小：{len(independent_set)}")
            
            elif choice == '4':
                independent_set = graph.optimize_independent_set()
                print("\n独立集：", sorted(independent_set))
                print(f"独立集大小：{len(independent_set)}")
            
            elif choice == '5':
                break
            
            else:
                print("无效的选择！")
            
            # 打印操作过程
            print_operations(graph.steps)
            graph.steps.clear()  # 清空步骤记录
        
    except ValueError as e:
        print(f"错误：{str(e)}") 