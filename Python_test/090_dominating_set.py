#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现支配集问题的解决方案。

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
        """获取顶点的邻居（包括顶点自身）"""
        return self.graph[vertex] | {vertex}
    
    def greedy_dominating_set(self) -> Set[int]:
        """贪心算法求解支配集"""
        # 复制图，以便在处理过程中移除顶点
        undominated = set(range(self.V))
        dominating_set = set()
        
        while undominated:
            # 找到能支配最多未支配顶点的顶点
            max_dominated = -1
            best_vertex = None
            
            for v in range(self.V):
                if v not in dominating_set:
                    dominated = len(undominated & self.get_neighbors(v))
                    if dominated > max_dominated:
                        max_dominated = dominated
                        best_vertex = v
            
            if best_vertex is None:
                break
            
            # 将顶点加入支配集
            dominating_set.add(best_vertex)
            # 移除被支配的顶点
            undominated -= self.get_neighbors(best_vertex)
            self.steps.append((best_vertex, max_dominated, "选择顶点"))
        
        return dominating_set
    
    def approximate_dominating_set(self) -> Set[int]:
        """ln(n)-近似算法求解支配集"""
        undominated = set(range(self.V))
        dominating_set = set()
        
        while undominated:
            # 计算每个顶点的性价比（支配数/权重）
            max_ratio = 0
            best_vertex = None
            
            for v in range(self.V):
                if v not in dominating_set:
                    dominated = len(undominated & self.get_neighbors(v))
                    if dominated > 0:
                        ratio = dominated
                        if ratio > max_ratio:
                            max_ratio = ratio
                            best_vertex = v
            
            if best_vertex is None:
                break
            
            dominating_set.add(best_vertex)
            undominated -= self.get_neighbors(best_vertex)
            self.steps.append((best_vertex, max_ratio, "近似选择"))
        
        return dominating_set
    
    def backtrack_dominating_set(self, max_time: float = 5.0) -> Set[int]:
        """回溯算法求解支配集（带时间限制）"""
        start_time = time.time()
        min_dominating = set(range(self.V))  # 初始解
        
        def is_dominating_set(vertices: Set[int]) -> bool:
            """检查是否是有效的支配集"""
            dominated = set()
            for v in vertices:
                dominated |= self.get_neighbors(v)
            return len(dominated) == self.V
        
        def backtrack_util(curr_vertex: int, curr_set: Set[int]):
            nonlocal min_dominating
            
            # 检查时间限制
            if time.time() - start_time > max_time:
                return
            
            # 如果当前集合已经比最优解大，剪枝
            if len(curr_set) >= len(min_dominating):
                return
            
            # 到达最后一个顶点
            if curr_vertex == self.V:
                if is_dominating_set(curr_set):
                    min_dominating = curr_set.copy()
                    self.steps.append((len(min_dominating), "更新最优解"))
                return
            
            # 不选当前顶点
            backtrack_util(curr_vertex + 1, curr_set)
            
            # 选择当前顶点
            curr_set.add(curr_vertex)
            backtrack_util(curr_vertex + 1, curr_set)
            curr_set.remove(curr_vertex)
        
        backtrack_util(0, set())
        return min_dominating
    
    def optimize_dominating_set(self) -> Set[int]:
        """优化的支配集求解方案"""
        # 预处理：找出必须包含的顶点（与孤立顶点相连的唯一顶点）
        must_include = set()
        isolated = set()
        
        for v in range(self.V):
            if not self.graph[v]:
                isolated.add(v)
                self.steps.append((v, "孤立顶点"))
            elif len(self.graph[v]) == 1:
                neighbor = next(iter(self.graph[v]))
                must_include.add(neighbor)
                self.steps.append((neighbor, "必选顶点"))
        
        # 在剩余图上运行贪心算法
        remaining_vertices = set(range(self.V)) - isolated
        remaining_graph = Graph(self.V)
        
        for v in remaining_vertices:
            for u in self.graph[v]:
                if u in remaining_vertices:
                    remaining_graph.add_edge(v, u)
        
        additional_set = remaining_graph.greedy_dominating_set()
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
            elif operation == "必选顶点":
                print(f"{operation}：顶点 {val}")
            elif operation == "更新最优解":
                print(f"{operation}：当前大小 {val}")
        elif len(step) == 3:
            if step[2] == "添加边":
                u, v, _ = step
                print(f"添加边：{u} - {v}")
            elif step[2] == "选择顶点":
                vertex, dominated, _ = step
                print(f"选择顶点：{vertex}，支配 {dominated} 个顶点")
            elif step[2] == "近似选择":
                vertex, ratio, _ = step
                print(f"近似选择：顶点 {vertex}，支配率 {ratio}")

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
                dominating_set = graph.greedy_dominating_set()
                print("\n支配集：", sorted(dominating_set))
                print(f"支配集大小：{len(dominating_set)}")
            
            elif choice == '2':
                dominating_set = graph.approximate_dominating_set()
                print("\n支配集：", sorted(dominating_set))
                print(f"支配集大小：{len(dominating_set)}")
            
            elif choice == '3':
                max_time = float(input("请输入最大运行时间（秒）："))
                dominating_set = graph.backtrack_dominating_set(max_time)
                print("\n支配集：", sorted(dominating_set))
                print(f"支配集大小：{len(dominating_set)}")
            
            elif choice == '4':
                dominating_set = graph.optimize_dominating_set()
                print("\n支配集：", sorted(dominating_set))
                print(f"支配集大小：{len(dominating_set)}")
            
            elif choice == '5':
                break
            
            else:
                print("无效的选择！")
            
            # 打印操作过程
            print_operations(graph.steps)
            graph.steps.clear()  # 清空步骤记录
        
    except ValueError as e:
        print(f"错误：{str(e)}") 