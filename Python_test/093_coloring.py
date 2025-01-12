#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现图着色问题的解决方案。

程序分析：
1. 实现贪心算法
2. 实现近似算法
3. 实现回溯算法
4. 优化求解过程
"""

from typing import List, Dict, Set, Optional
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
    
    def greedy_coloring(self) -> Dict[int, int]:
        """贪心算法求解图着色"""
        # 按度数降序排序顶点
        vertices = list(range(self.V))
        vertices.sort(key=lambda v: len(self.graph[v]), reverse=True)
        
        # 为每个顶点分配可用的最小颜色
        colors = {}  # 顶点到颜色的映射
        
        for v in vertices:
            # 获取邻居已使用的颜色
            used_colors = {colors[u] for u in self.graph[v] if u in colors}
            
            # 找到最小的可用颜色
            color = 0
            while color in used_colors:
                color += 1
            
            colors[v] = color
            self.steps.append((v, color, "分配颜色"))
        
        return colors
    
    def dsatur_coloring(self) -> Dict[int, int]:
        """DSATUR算法求解图着色"""
        colors = {}  # 顶点到颜色的映射
        saturation = defaultdict(int)  # 顶点的饱和度
        
        while len(colors) < self.V:
            # 找到饱和度最大且未着色的顶点
            max_sat = -1
            max_deg = -1
            best_vertex = None
            
            for v in range(self.V):
                if v not in colors:
                    if saturation[v] > max_sat or \
                       (saturation[v] == max_sat and len(self.graph[v]) > max_deg):
                        max_sat = saturation[v]
                        max_deg = len(self.graph[v])
                        best_vertex = v
            
            # 获取邻居已使用的颜色
            used_colors = {colors[u] for u in self.graph[best_vertex] if u in colors}
            
            # 找到最小的可用颜色
            color = 0
            while color in used_colors:
                color += 1
            
            # 为顶点着色
            colors[best_vertex] = color
            self.steps.append((best_vertex, color, "DSATUR着色"))
            
            # 更新邻居的饱和度
            for u in self.graph[best_vertex]:
                if u not in colors:
                    neighbor_colors = {colors[w] for w in self.graph[u] if w in colors}
                    saturation[u] = len(neighbor_colors)
        
        return colors
    
    def backtrack_coloring(self, max_time: float = 5.0) -> Optional[Dict[int, int]]:
        """回溯算法求解图着色（带时间限制）"""
        start_time = time.time()
        min_colors = self.V  # 当前最优解使用的颜色数
        best_coloring = None  # 当前最优解
        
        def is_safe(vertex: int, color: int, colors: Dict[int, int]) -> bool:
            """检查是否可以为顶点分配指定颜色"""
            return all(colors.get(u, -1) != color for u in self.graph[vertex])
        
        def backtrack_util(vertex: int, colors: Dict[int, int], max_color: int):
            nonlocal min_colors, best_coloring
            
            # 检查时间限制
            if time.time() - start_time > max_time:
                return False
            
            # 已经为所有顶点着色
            if vertex == self.V:
                curr_colors = len(set(colors.values()))
                if curr_colors < min_colors:
                    min_colors = curr_colors
                    best_coloring = colors.copy()
                    self.steps.append((curr_colors, "更新最优解"))
                return True
            
            # 尝试每种可能的颜色
            for color in range(max_color + 1):
                if is_safe(vertex, color, colors):
                    colors[vertex] = color
                    # 如果需要新颜色且已超过当前最优解，剪枝
                    if color == max_color and max_color + 1 >= min_colors:
                        colors.pop(vertex)
                        continue
                    
                    # 继续为下一个顶点着色
                    backtrack_util(vertex + 1, colors, max(max_color, color))
                    colors.pop(vertex)
            
            return False
        
        # 使用贪心算法获取初始解
        initial_coloring = self.greedy_coloring()
        min_colors = len(set(initial_coloring.values()))
        best_coloring = initial_coloring
        
        # 开始回溯
        backtrack_util(0, {}, -1)
        return best_coloring
    
    def optimize_coloring(self) -> Dict[int, int]:
        """优化的图着色求解方案"""
        # 预处理：移除孤立顶点
        isolated = set()
        for v in range(self.V):
            if not self.graph[v]:
                isolated.add(v)
                self.steps.append((v, "孤立顶点"))
        
        # 在剩余图上运行DSATUR算法
        remaining_vertices = set(range(self.V)) - isolated
        remaining_graph = Graph(self.V)
        
        for v in remaining_vertices:
            for u in self.graph[v]:
                if u in remaining_vertices:
                    remaining_graph.add_edge(v, u)
        
        colors = remaining_graph.dsatur_coloring()
        
        # 为孤立顶点分配颜色0
        for v in isolated:
            colors[v] = 0
            self.steps.append((v, 0, "孤立顶点着色"))
        
        return colors

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if len(step) == 2:
            val, operation = step
            if operation == "孤立顶点":
                print(f"{operation}：顶点 {val}")
            elif operation == "更新最优解":
                print(f"{operation}：使用 {val} 种颜色")
        elif len(step) == 3:
            if step[2] == "添加边":
                u, v, _ = step
                print(f"添加边：{u} - {v}")
            elif step[2] == "分配颜色":
                vertex, color, _ = step
                print(f"为顶点 {vertex} 分配颜色 {color}")
            elif step[2] == "DSATUR着色":
                vertex, color, _ = step
                print(f"DSATUR为顶点 {vertex} 分配颜色 {color}")
            elif step[2] == "孤立顶点着色":
                vertex, color, _ = step
                print(f"为孤立顶点 {vertex} 分配颜色 {color}")

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
            print("2. DSATUR算法")
            print("3. 回溯算法")
            print("4. 优化算法")
            print("5. 退出")
            
            choice = input("请输入选择（1-5）：")
            
            if choice == '1':
                colors = graph.greedy_coloring()
                print("\n顶点着色：")
                for v in sorted(colors):
                    print(f"顶点 {v}: 颜色 {colors[v]}")
                print(f"使用颜色数：{len(set(colors.values()))}")
            
            elif choice == '2':
                colors = graph.dsatur_coloring()
                print("\n顶点着色：")
                for v in sorted(colors):
                    print(f"顶点 {v}: 颜色 {colors[v]}")
                print(f"使用颜色数：{len(set(colors.values()))}")
            
            elif choice == '3':
                max_time = float(input("请输入最大运行时间（秒）："))
                colors = graph.backtrack_coloring(max_time)
                if colors:
                    print("\n顶点着色：")
                    for v in sorted(colors):
                        print(f"顶点 {v}: 颜色 {colors[v]}")
                    print(f"使用颜色数：{len(set(colors.values()))}")
                else:
                    print("未找到解或超时！")
            
            elif choice == '4':
                colors = graph.optimize_coloring()
                print("\n顶点着色：")
                for v in sorted(colors):
                    print(f"顶点 {v}: 颜色 {colors[v]}")
                print(f"使用颜色数：{len(set(colors.values()))}")
            
            elif choice == '5':
                break
            
            else:
                print("无效的选择！")
            
            # 打印操作过程
            print_operations(graph.steps)
            graph.steps.clear()  # 清空步骤记录
        
    except ValueError as e:
        print(f"错误：{str(e)}") 