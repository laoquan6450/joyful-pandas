#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现团问题的解决方案。

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
    
    def is_clique(self, vertices: Set[int]) -> bool:
        """检查给定的顶点集是否构成团"""
        for v in vertices:
            if not vertices - {v} <= self.graph[v]:
                return False
        return True
    
    def greedy_clique(self) -> Set[int]:
        """贪心算法求解最大团"""
        # 从度数最大的顶点开始构建团
        clique = set()
        remaining = set(range(self.V))
        
        while remaining:
            # 找到能加入当前团的度数最大的顶点
            max_degree = -1
            best_vertex = None
            
            for v in remaining:
                if clique <= self.get_neighbors(v):  # 如果v与当前团中所有顶点相邻
                    degree = len(self.graph[v])
                    if degree > max_degree:
                        max_degree = degree
                        best_vertex = v
            
            if best_vertex is None:
                break
            
            # 将顶点加入团
            clique.add(best_vertex)
            remaining.remove(best_vertex)
            self.steps.append((best_vertex, max_degree, "选择顶点"))
            
            # 更新剩余顶点集
            remaining &= self.get_neighbors(best_vertex)
        
        return clique
    
    def approximate_clique(self) -> Set[int]:
        """近似算法求解最大团"""
        clique = set()
        vertices = list(range(self.V))
        vertices.sort(key=lambda v: len(self.graph[v]), reverse=True)  # 按度数降序排序
        
        # 从度数最大的顶点开始尝试构建团
        for v in vertices:
            if clique <= self.get_neighbors(v):  # 如果v与当前团中所有顶点相邻
                clique.add(v)
                self.steps.append((v, "近似选择"))
        
        return clique
    
    def backtrack_clique(self, max_time: float = 5.0) -> Set[int]:
        """回溯算法求解最大团（带时间限制）"""
        start_time = time.time()
        max_clique = set()  # 当前找到的最大团
        
        def backtrack_util(curr_vertex: int, curr_clique: Set[int], candidates: Set[int]):
            nonlocal max_clique
            
            # 检查时间限制
            if time.time() - start_time > max_time:
                return
            
            # 更新最优解
            if len(curr_clique) > len(max_clique):
                max_clique = curr_clique.copy()
                self.steps.append((len(max_clique), "更新最优解"))
            
            # 如果没有候选顶点，返回
            if not candidates:
                return
            
            # 遍历候选顶点
            for v in sorted(candidates):  # 按顶点编号排序以保持确定性
                # 如果剩余顶点数量加上当前团大小不可能超过最优解，剪枝
                if len(curr_clique) + len(candidates) <= len(max_clique):
                    break
                
                # 将顶点加入团
                new_clique = curr_clique | {v}
                # 计算新的候选集（与v相邻的顶点）
                new_candidates = candidates & self.get_neighbors(v)
                backtrack_util(v + 1, new_clique, new_candidates)
                candidates.remove(v)
        
        backtrack_util(0, set(), set(range(self.V)))
        return max_clique
    
    def optimize_clique(self) -> Set[int]:
        """优化的最大团求解方案"""
        # 预处理：移除度数太小的顶点
        min_possible_degree = self.V - 2  # 最大团中顶点的最小可能度数
        remaining_vertices = set()
        
        for v in range(self.V):
            if len(self.graph[v]) >= min_possible_degree:
                remaining_vertices.add(v)
            else:
                self.steps.append((v, "移除低度顶点"))
        
        # 在剩余图上运行回溯算法（限时）
        remaining_graph = Graph(self.V)
        for v in remaining_vertices:
            for u in self.graph[v]:
                if u in remaining_vertices:
                    remaining_graph.add_edge(v, u)
        
        return remaining_graph.backtrack_clique(max_time=2.0)

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if len(step) == 2:
            val, operation = step
            if operation == "近似选择":
                print(f"{operation}：顶点 {val}")
            elif operation == "移除低度顶点":
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
                clique = graph.greedy_clique()
                print("\n最大团：", sorted(clique))
                print(f"团大小：{len(clique)}")
            
            elif choice == '2':
                clique = graph.approximate_clique()
                print("\n最大团：", sorted(clique))
                print(f"团大小：{len(clique)}")
            
            elif choice == '3':
                max_time = float(input("请输入最大运行时间（秒）："))
                clique = graph.backtrack_clique(max_time)
                print("\n最大团：", sorted(clique))
                print(f"团大小：{len(clique)}")
            
            elif choice == '4':
                clique = graph.optimize_clique()
                print("\n最大团：", sorted(clique))
                print(f"团大小：{len(clique)}")
            
            elif choice == '5':
                break
            
            else:
                print("无效的选择！")
            
            # 打印操作过程
            print_operations(graph.steps)
            graph.steps.clear()  # 清空步骤记录
        
    except ValueError as e:
        print(f"错误：{str(e)}") 