#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现边覆盖问题的解决方案。

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
        self.edges = set()  # 边集合
        self.steps = []  # 记录操作步骤
    
    def add_edge(self, u: int, v: int) -> None:
        """添加边"""
        if u > v:
            u, v = v, u
        self.graph[u].add(v)
        self.graph[v].add(u)
        self.edges.add((u, v))
        self.steps.append((u, v, "添加边"))
    
    def greedy_edge_cover(self) -> Set[Tuple[int, int]]:
        """贪心算法求解边覆盖"""
        # 复制图，以便在处理过程中移除顶点
        uncovered = set(range(self.V))
        cover = set()
        
        while uncovered:
            # 找到能覆盖最多未覆盖顶点的边
            max_covered = -1
            best_edge = None
            
            for edge in self.edges:
                u, v = edge
                covered = sum(1 for vertex in (u, v) if vertex in uncovered)
                if covered > max_covered:
                    max_covered = covered
                    best_edge = edge
            
            if best_edge is None:
                break
            
            # 将边加入覆盖集
            cover.add(best_edge)
            u, v = best_edge
            uncovered.discard(u)
            uncovered.discard(v)
            self.steps.append((best_edge, max_covered, "选择边"))
        
        return cover
    
    def approximate_edge_cover(self) -> Set[Tuple[int, int]]:
        """2-近似算法求解边覆盖"""
        uncovered = set(range(self.V))
        cover = set()
        
        # 随机选择未覆盖的顶点，选择与其相连的任意边
        while uncovered:
            vertex = next(iter(uncovered))
            
            # 找到与该顶点相连的一条边
            edge = None
            for neighbor in self.graph[vertex]:
                if vertex < neighbor:
                    edge = (vertex, neighbor)
                else:
                    edge = (neighbor, vertex)
                break
            
            if edge is None:
                break
            
            # 将边加入覆盖集
            cover.add(edge)
            u, v = edge
            uncovered.discard(u)
            uncovered.discard(v)
            self.steps.append((edge, "近似选择"))
        
        return cover
    
    def backtrack_edge_cover(self, max_time: float = 5.0) -> Set[Tuple[int, int]]:
        """回溯算法求解边覆盖（带时间限制）"""
        start_time = time.time()
        min_cover = self.edges.copy()  # 初始解
        
        def is_edge_cover(edges: Set[Tuple[int, int]]) -> bool:
            """检查是否是有效的边覆盖"""
            covered = set()
            for edge in edges:
                covered.add(edge[0])
                covered.add(edge[1])
            return len(covered) == self.V
        
        def backtrack_util(curr_edge: int, curr_cover: Set[Tuple[int, int]]):
            nonlocal min_cover
            
            # 检查时间限制
            if time.time() - start_time > max_time:
                return
            
            # 如果当前覆盖已经比最优解大，剪枝
            if len(curr_cover) >= len(min_cover):
                return
            
            # 检查当前选择是否是一个解
            if is_edge_cover(curr_cover):
                min_cover = curr_cover.copy()
                self.steps.append((len(min_cover), "更新最优解"))
                return
            
            # 已经考虑完所有边
            if curr_edge >= len(self.edges):
                return
            
            edges_list = list(self.edges)
            
            # 不选当前边
            backtrack_util(curr_edge + 1, curr_cover)
            
            # 选择当前边
            curr_cover.add(edges_list[curr_edge])
            backtrack_util(curr_edge + 1, curr_cover)
            curr_cover.remove(edges_list[curr_edge])
        
        backtrack_util(0, set())
        return min_cover
    
    def optimize_edge_cover(self) -> Set[Tuple[int, int]]:
        """优化的边覆盖求解方案"""
        # 预处理：找出必须包含的边（连接叶子节点的边）
        must_include = set()
        leaf_vertices = set()
        
        for v in range(self.V):
            if len(self.graph[v]) == 1:
                leaf_vertices.add(v)
                neighbor = next(iter(self.graph[v]))
                edge = (v, neighbor) if v < neighbor else (neighbor, v)
                must_include.add(edge)
                self.steps.append((edge, "必选边"))
        
        # 在剩余图上运行贪心算法
        remaining_vertices = set(range(self.V)) - leaf_vertices
        remaining_graph = Graph(self.V)
        
        for edge in self.edges:
            u, v = edge
            if edge not in must_include and u in remaining_vertices and v in remaining_vertices:
                remaining_graph.add_edge(u, v)
        
        additional_cover = remaining_graph.greedy_edge_cover()
        return must_include | additional_cover

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if len(step) == 2:
            val, operation = step
            if operation == "近似选择":
                print(f"{operation}：边 {val}")
            elif operation == "必选边":
                print(f"{operation}：边 {val}")
            elif operation == "更新最优解":
                print(f"{operation}：当前大小 {val}")
        elif len(step) == 3:
            if step[2] == "添加边":
                u, v, _ = step
                print(f"添加边：{u} - {v}")
            elif step[2] == "选择边":
                edge, covered, _ = step
                print(f"选择边：{edge}，覆盖 {covered} 个顶点")

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
                cover = graph.greedy_edge_cover()
                print("\n边覆盖：", sorted(cover))
                print(f"覆盖大小：{len(cover)}")
            
            elif choice == '2':
                cover = graph.approximate_edge_cover()
                print("\n边覆盖：", sorted(cover))
                print(f"覆盖大小：{len(cover)}")
            
            elif choice == '3':
                max_time = float(input("请输入最大运行时间（秒）："))
                cover = graph.backtrack_edge_cover(max_time)
                print("\n边覆盖：", sorted(cover))
                print(f"覆盖大小：{len(cover)}")
            
            elif choice == '4':
                cover = graph.optimize_edge_cover()
                print("\n边覆盖：", sorted(cover))
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