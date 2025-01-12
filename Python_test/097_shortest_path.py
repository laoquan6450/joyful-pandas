#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现最短路径问题的解决方案。

程序分析：
1. 实现Dijkstra算法
2. 实现Bellman-Ford算法
3. 实现Floyd-Warshall算法
4. 优化求解过程
"""

from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict
import heapq
import time

class Graph:
    def __init__(self, vertices: int):
        self.V = vertices  # 顶点数
        self.graph = defaultdict(dict)  # 邻接表存储边权重
        self.steps = []  # 记录操作步骤
    
    def add_edge(self, u: int, v: int, weight: float) -> None:
        """添加边"""
        self.graph[u][v] = weight
        self.steps.append((u, v, weight, "添加边"))
    
    def dijkstra(self, source: int) -> Tuple[Dict[int, float], Dict[int, List[int]]]:
        """Dijkstra算法求解单源最短路径"""
        dist = {v: float('inf') for v in range(self.V)}  # 距离
        prev = {v: None for v in range(self.V)}  # 前驱节点
        dist[source] = 0
        
        # 优先队列存储(距离, 顶点)
        pq = [(0, source)]
        visited = set()
        
        while pq:
            d, u = heapq.heappop(pq)
            if u in visited:
                continue
            
            visited.add(u)
            self.steps.append((u, d, "访问顶点"))
            
            for v, weight in self.graph[u].items():
                if v not in visited:
                    new_dist = dist[u] + weight
                    if new_dist < dist[v]:
                        dist[v] = new_dist
                        prev[v] = u
                        heapq.heappush(pq, (new_dist, v))
                        self.steps.append((u, v, new_dist, "更新距离"))
        
        # 构建路径
        paths = {}
        for v in range(self.V):
            if dist[v] != float('inf'):
                path = []
                curr = v
                while curr is not None:
                    path.append(curr)
                    curr = prev[curr]
                path.reverse()
                paths[v] = path
        
        return dist, paths
    
    def bellman_ford(self, source: int) -> Tuple[Optional[Dict[int, float]], Optional[Dict[int, List[int]]]]:
        """Bellman-Ford算法求解单源最短路径（可处理负权边）"""
        dist = {v: float('inf') for v in range(self.V)}
        prev = {v: None for v in range(self.V)}
        dist[source] = 0
        
        # 进行V-1次松弛操作
        for i in range(self.V - 1):
            updated = False
            for u in range(self.V):
                for v, weight in self.graph[u].items():
                    if dist[u] + weight < dist[v]:
                        dist[v] = dist[u] + weight
                        prev[v] = u
                        updated = True
                        self.steps.append((u, v, dist[v], "松弛操作"))
            
            if not updated:
                break
        
        # 检测负权环
        for u in range(self.V):
            for v, weight in self.graph[u].items():
                if dist[u] + weight < dist[v]:
                    self.steps.append((u, v, "检测到负权环"))
                    return None, None
        
        # 构建路径
        paths = {}
        for v in range(self.V):
            if dist[v] != float('inf'):
                path = []
                curr = v
                while curr is not None:
                    path.append(curr)
                    curr = prev[curr]
                path.reverse()
                paths[v] = path
        
        return dist, paths
    
    def floyd_warshall(self) -> Tuple[List[List[float]], List[List[List[int]]]]:
        """Floyd-Warshall算法求解所有点对最短路径"""
        # 初始化距离矩阵和路径矩阵
        dist = [[float('inf')] * self.V for _ in range(self.V)]
        next_vertex = [[None] * self.V for _ in range(self.V)]
        
        # 初始化直接相连的边
        for u in range(self.V):
            dist[u][u] = 0
            for v, weight in self.graph[u].items():
                dist[u][v] = weight
                next_vertex[u][v] = v
        
        # Floyd-Warshall算法核心
        for k in range(self.V):
            for i in range(self.V):
                for j in range(self.V):
                    if dist[i][k] != float('inf') and dist[k][j] != float('inf'):
                        new_dist = dist[i][k] + dist[k][j]
                        if new_dist < dist[i][j]:
                            dist[i][j] = new_dist
                            next_vertex[i][j] = next_vertex[i][k]
                            self.steps.append((i, j, k, new_dist, "更新最短路"))
        
        # 构建所有路径
        paths = [[[] for _ in range(self.V)] for _ in range(self.V)]
        for i in range(self.V):
            for j in range(self.V):
                if dist[i][j] != float('inf'):
                    path = [i]
                    curr = i
                    while curr != j:
                        curr = next_vertex[curr][j]
                        path.append(curr)
                    paths[i][j] = path
        
        return dist, paths
    
    def optimize_shortest_path(self, source: int) -> Tuple[Dict[int, float], Dict[int, List[int]]]:
        """优化的最短路径算法"""
        # 预处理：检测是否存在负权边
        has_negative = False
        for u in range(self.V):
            for v, weight in self.graph[u].items():
                if weight < 0:
                    has_negative = True
                    self.steps.append((u, v, weight, "检测到负权边"))
                    break
            if has_negative:
                break
        
        # 根据图的特性选择合适的算法
        if has_negative:
            dist, paths = self.bellman_ford(source)
            if dist is None:
                print("图中存在负权环！")
                return {}, {}
            return dist, paths
        else:
            return self.dijkstra(source)

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if len(step) == 3:
            if step[2] == "检测到负权环":
                u, v, _ = step
                print(f"检测到负权环：边 {u} -> {v}")
            else:  # 访问顶点
                vertex, dist, _ = step
                print(f"访问顶点 {vertex}，当前距离 {dist}")
        elif len(step) == 4:
            if step[3] == "添加边":
                u, v, w, _ = step
                print(f"添加边：{u} -> {v}，权重 {w}")
            elif step[3] == "更新距离":
                u, v, d, _ = step
                print(f"更新距离：{u} -> {v}，新距离 {d}")
            elif step[3] == "松弛操作":
                u, v, d, _ = step
                print(f"松弛操作：{u} -> {v}，新距离 {d}")
            elif step[3] == "检测到负权边":
                u, v, w, _ = step
                print(f"检测到负权边：{u} -> {v}，权重 {w}")
        elif len(step) == 5:
            i, j, k, d, _ = step
            print(f"通过顶点 {k} 更新 {i} -> {j} 的最短路为 {d}")

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
            u, v, weight = map(float, input().strip().split())
            u, v = int(u), int(v)
            if 0 <= u < V and 0 <= v < V:
                graph.add_edge(u, v, weight)
            else:
                print(f"忽略无效边：{u} -> {v}")
        
        while True:
            print("\n请选择算法：")
            print("1. Dijkstra算法")
            print("2. Bellman-Ford算法")
            print("3. Floyd-Warshall算法")
            print("4. 优化算法")
            print("5. 退出")
            
            choice = input("请输入选择（1-5）：")
            
            if choice in ['1', '2', '4']:
                source = int(input("请输入源点："))
                if not 0 <= source < V:
                    print("无效的源点！")
                    continue
                
                if choice == '1':
                    dist, paths = graph.dijkstra(source)
                elif choice == '2':
                    dist, paths = graph.bellman_ford(source)
                    if dist is None:
                        print("\n图中存在负权环！")
                        continue
                else:  # choice == '4'
                    dist, paths = graph.optimize_shortest_path(source)
                
                print("\n最短路径结果：")
                for v in range(V):
                    if v in paths:
                        print(f"到顶点 {v} 的最短距离：{dist[v]}")
                        print(f"路径：{' -> '.join(map(str, paths[v]))}")
                    else:
                        print(f"顶点 {v} 不可达")
            
            elif choice == '3':
                dist, paths = graph.floyd_warshall()
                print("\n所有点对最短路径：")
                for i in range(V):
                    for j in range(V):
                        if paths[i][j]:
                            print(f"{i} -> {j} 的最短距离：{dist[i][j]}")
                            print(f"路径：{' -> '.join(map(str, paths[i][j]))}")
            
            elif choice == '5':
                break
            
            else:
                print("无效的选择！")
            
            # 打印操作过程
            print_operations(graph.steps)
            graph.steps.clear()  # 清空步骤记录
        
    except ValueError as e:
        print(f"错误：{str(e)}") 