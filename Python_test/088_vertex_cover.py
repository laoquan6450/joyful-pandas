#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现顶点覆盖问题的解决方案。

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
    
    def greedy_vertex_cover(self) -> Set[int]:
        """贪心算法求解顶点覆盖"""
        # 复制图，以便在处理过程中移除边
        remaining_edges = {u: self.graph[u].copy() for u in self.graph}
        cover = set()
        
        while True:
            # 找到度数最大的顶点
            max_degree = 0
            max_vertex = None
            
            for v in range(self.V):
                if v not in cover:
                    degree = len(remaining_edges[v])
                    if degree > max_degree:
                        max_degree = degree
                        max_vertex = v
            
            if max_vertex is None or max_degree == 0:
                break
            
            # 将该顶点加入覆盖集
            cover.add(max_vertex)
            self.steps.append((max_vertex, max_degree, "选择顶点"))
            
            # 移除与该顶点相关的边
            neighbors = remaining_edges[max_vertex].copy()
            for neighbor in neighbors:
                remaining_edges[max_vertex].remove(neighbor)
                remaining_edges[neighbor].remove(max_vertex)
        
        return cover
    
    def approximate_vertex_cover(self) -> Set[int]:
        """2-近似算法求解顶点覆盖"""
        # 复制图
        remaining_edges = {u: self.graph[u].copy() for u in self.graph}
        cover = set()
        
        # 随机选择未覆盖的边，将其两个端点加入覆盖集
        while True:
            # 找到一条未覆盖的边
            edge = None
            for u in range(self.V):
                if remaining_edges[u]:
                    v = next(iter(remaining_edges[u]))
                    edge = (u, v)
                    break
            
            if edge is None:
                break
            
            # 将边的两个端点加入覆盖集
            u, v = edge
            cover.add(u)
            cover.add(v)
            self.steps.append((u, v, "选择边的端点"))
            
            # 移除与这两个顶点相关的所有边
            for vertex in (u, v):
                neighbors = remaining_edges[vertex].copy()
                for neighbor in neighbors:
                    remaining_edges[vertex].remove(neighbor)
                    remaining_edges[neighbor].remove(vertex)
        
        return cover
    
    def backtrack_vertex_cover(self, max_time: float = 5.0) -> Set[int]:
        """回溯算法求解顶点覆盖（带时间限制）"""
        start_time = time.time()
        min_cover = set(range(self.V))  # 初始解
        
        def is_vertex_cover(vertices: Set[int]) -> bool:
            """检查是否是有效的顶点覆盖"""
            for u in self.graph:
                for v in self.graph[u]:
                    if u not in vertices and v not in vertices:
                        return False
            return True
        
        def backtrack_util(curr_vertex: int, curr_cover: Set[int]):
            nonlocal min_cover
            
            # 检查时间限制
            if time.time() - start_time > max_time:
                return
            
            # 如果当前覆盖已经比最优解大，剪枝
            if len(curr_cover) >= len(min_cover):
                return
            
            # 到达最后一个顶点
            if curr_vertex == self.V:
                if is_vertex_cover(curr_cover):
                    min_cover = curr_cover.copy()
                    self.steps.append((len(min_cover), "更新最优解"))
                return
            
            # 不选当前顶点
            backtrack_util(curr_vertex + 1, curr_cover)
            
            # 选择当前顶点
            curr_cover.add(curr_vertex)
            backtrack_util(curr_vertex + 1, curr_cover)
            curr_cover.remove(curr_vertex)
        
        backtrack_util(0, set())
        return min_cover
    
    def optimize_vertex_cover(self) -> Set[int]:
        """优化的顶点覆盖求解方案"""
        # 预处理：移除孤立顶点
        isolated = set()
        for v in range(self.V):
            if not self.graph[v]:
                isolated.add(v)
                self.steps.append((v, "移除孤立顶点"))
        
        # 预处理：找出必须包含的顶点（与叶子相连的顶点）
        must_include = set()
        leaf_vertices = set()
        
        for v in range(self.V):
            if v not in isolated and len(self.graph[v]) == 1:
                leaf_vertices.add(v)
                neighbor = next(iter(self.graph[v]))
                must_include.add(neighbor)
                self.steps.append((neighbor, "必选顶点"))
        
        # 在剩余图上运行贪心算法
        remaining_vertices = set(range(self.V)) - isolated - leaf_vertices
        remaining_graph = Graph(self.V)
        
        for v in remaining_vertices:
            for u in self.graph[v]:
                if u in remaining_vertices:
                    remaining_graph.add_edge(v, u)
        
        additional_cover = remaining_graph.greedy_vertex_cover()
        return must_include | additional_cover

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if len(step) == 2:
            val, operation = step
            if operation == "移除孤立顶点":
                print(f"{operation}：顶点 {val}")
            elif operation == "必选顶点":
                print(f"{operation}：顶点 {val}")
            elif operation == "更新最优解":
                print(f"{operation}：当前大小 {val}")
        elif len(step) == 3:
            v1, v2, operation = step
            if operation == "添加边":
                print(f"{operation}：{v1} - {v2}")
            elif operation == "选择顶点":
                print(f"{operation}：顶点 {v1}，度数 {v2}")
            elif operation == "选择边的端点":
                print(f"{operation}：顶点 {v1} 和 {v2}")

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
            if 0 <= u < V and 0 <= v < V:
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
                cover = graph.greedy_vertex_cover()
                print("\n顶点覆盖：", sorted(cover))
                print(f"覆盖大小：{len(cover)}")
            
            elif choice == '2':
                cover = graph.approximate_vertex_cover()
                print("\n顶点覆盖：", sorted(cover))
                print(f"覆盖大小：{len(cover)}")
            
            elif choice == '3':
                max_time = float(input("请输入最大运行时间（秒）："))
                cover = graph.backtrack_vertex_cover(max_time)
                print("\n顶点覆盖：", sorted(cover))
                print(f"覆盖大小：{len(cover)}")
            
            elif choice == '4':
                cover = graph.optimize_vertex_cover()
                print("\n顶点覆盖：", sorted(cover))
                print(f"覆盖大小：{len(cover)}")
            
            elif choice == '5':
                break
            
            else:
                print("无效的选择！")
            
            # 打印操作过程
            print_operations(graph.steps)
            graph.steps.clear()  # 清空步骤记录
        
    except ValueError as e:
        print(f"错误：{str(e)}") 