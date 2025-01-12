#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现网络流问题的解决方案。

程序分析：
1. 实现Ford-Fulkerson算法
2. 实现Edmonds-Karp算法
3. 实现最小费用最大流
4. 优化求解过程
"""

from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict, deque
import heapq
import time

class FlowNetwork:
    def __init__(self, vertices: int):
        self.V = vertices  # 顶点数
        self.graph = defaultdict(dict)  # 邻接表存储容量和费用
        self.steps = []  # 记录操作步骤
    
    def add_edge(self, u: int, v: int, capacity: float, cost: float = 0) -> None:
        """添加边"""
        self.graph[u][v] = {"cap": capacity, "flow": 0, "cost": cost}
        self.graph[v][u] = {"cap": 0, "flow": 0, "cost": -cost}  # 反向边
        self.steps.append((u, v, capacity, cost, "添加边"))
    
    def _find_path_dfs(self, source: int, sink: int, visited: Set[int]) -> List[int]:
        """使用DFS寻找增广路径"""
        if source == sink:
            return [sink]
        
        visited.add(source)
        for v in self.graph[source]:
            if v not in visited and self.graph[source][v]["cap"] > self.graph[source][v]["flow"]:
                path = self._find_path_dfs(v, sink, visited)
                if path:
                    return [source] + path
        
        return []
    
    def ford_fulkerson(self, source: int, sink: int) -> float:
        """Ford-Fulkerson算法求解最大流"""
        max_flow = 0
        
        while True:
            # 寻找增广路径
            path = self._find_path_dfs(source, sink, set())
            if not path:
                break
            
            # 找到路径上的最小剩余容量
            flow = float('inf')
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                flow = min(flow, self.graph[u][v]["cap"] - self.graph[u][v]["flow"])
            
            # 更新流量
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                self.graph[u][v]["flow"] += flow
                self.graph[v][u]["flow"] -= flow
            
            max_flow += flow
            self.steps.append((path, flow, "Ford-Fulkerson增广"))
        
        return max_flow
    
    def edmonds_karp(self, source: int, sink: int) -> float:
        """Edmonds-Karp算法求解最大流"""
        max_flow = 0
        
        while True:
            # 使用BFS寻找最短增广路径
            parent = {}
            queue = deque([source])
            parent[source] = None
            
            while queue and sink not in parent:
                u = queue.popleft()
                for v in self.graph[u]:
                    if v not in parent and self.graph[u][v]["cap"] > self.graph[u][v]["flow"]:
                        parent[v] = u
                        queue.append(v)
            
            if sink not in parent:
                break
            
            # 构建路径
            path = []
            curr = sink
            while curr is not None:
                path.append(curr)
                curr = parent[curr]
            path.reverse()
            
            # 找到路径上的最小剩余容量
            flow = float('inf')
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                flow = min(flow, self.graph[u][v]["cap"] - self.graph[u][v]["flow"])
            
            # 更新流量
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                self.graph[u][v]["flow"] += flow
                self.graph[v][u]["flow"] -= flow
            
            max_flow += flow
            self.steps.append((path, flow, "Edmonds-Karp增广"))
        
        return max_flow
    
    def min_cost_max_flow(self, source: int, sink: int) -> Tuple[float, float]:
        """最小费用最大流算法"""
        max_flow = 0
        min_cost = 0
        
        while True:
            # 使用Dijkstra算法找最短路径
            dist = {v: float('inf') for v in range(self.V)}
            parent = {v: None for v in range(self.V)}
            dist[source] = 0
            pq = [(0, source)]
            
            while pq:
                d, u = heapq.heappop(pq)
                if d > dist[u]:
                    continue
                
                for v in self.graph[u]:
                    if self.graph[u][v]["cap"] > self.graph[u][v]["flow"]:
                        new_dist = dist[u] + self.graph[u][v]["cost"]
                        if new_dist < dist[v]:
                            dist[v] = new_dist
                            parent[v] = u
                            heapq.heappush(pq, (new_dist, v))
            
            if dist[sink] == float('inf'):
                break
            
            # 构建路径
            path = []
            curr = sink
            while curr is not None:
                path.append(curr)
                curr = parent[curr]
            path.reverse()
            
            # 找到路径上的最小剩余容量
            flow = float('inf')
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                flow = min(flow, self.graph[u][v]["cap"] - self.graph[u][v]["flow"])
            
            # 更新流量和费用
            path_cost = 0
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                self.graph[u][v]["flow"] += flow
                self.graph[v][u]["flow"] -= flow
                path_cost += flow * self.graph[u][v]["cost"]
            
            max_flow += flow
            min_cost += path_cost
            self.steps.append((path, flow, path_cost, "最小费用流增广"))
        
        return max_flow, min_cost
    
    def optimize_flow(self, source: int, sink: int) -> Tuple[float, float]:
        """优化的网络流算法"""
        # 预处理：移除无效边（容量为0的边）
        removed_edges = []
        for u in list(self.graph.keys()):
            for v in list(self.graph[u].keys()):
                if self.graph[u][v]["cap"] == 0:
                    removed_edges.append((u, v))
                    del self.graph[u][v]
                    if v in self.graph and u in self.graph[v]:
                        del self.graph[v][u]
                    self.steps.append((u, v, "移除无效边"))
        
        # 使用Edmonds-Karp算法求最大流
        max_flow = self.edmonds_karp(source, sink)
        
        # 计算总费用
        total_cost = sum(edge["flow"] * edge["cost"] 
                        for u in self.graph 
                        for v, edge in self.graph[u].items() 
                        if edge["flow"] > 0)
        
        return max_flow, total_cost

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if len(step) == 3:
            if step[2] == "移除无效边":
                u, v, _ = step
                print(f"移除无效边：{u} - {v}")
            else:  # Ford-Fulkerson或Edmonds-Karp增广
                path, flow, _ = step
                print(f"找到增广路径：{' -> '.join(map(str, path))}")
                print(f"增广流量：{flow}")
        elif len(step) == 4:
            if step[3] == "最小费用流增广":
                path, flow, cost, _ = step
                print(f"找到增广路径：{' -> '.join(map(str, path))}")
                print(f"增广流量：{flow}，路径费用：{cost}")
        elif len(step) == 5:
            u, v, cap, cost, _ = step
            print(f"添加边：{u} - {v}，容量 {cap}，费用 {cost}")

if __name__ == '__main__':
    try:
        # 获取输入
        V = int(input("请输入顶点数量："))
        E = int(input("请输入边的数量："))
        source = int(input("请输入源点："))
        sink = int(input("请输入汇点："))
        
        if not (0 <= source < V and 0 <= sink < V):
            raise ValueError("源点或汇点超出范围！")
        
        # 创建网络
        network = FlowNetwork(V)
        
        # 输入边
        print("\n请输入边（每行：起点 终点 容量 费用）：")
        for _ in range(E):
            line = input().strip().split()
            u, v = map(int, line[:2])
            capacity = float(line[2])
            cost = float(line[3]) if len(line) > 3 else 0
            
            if 0 <= u < V and 0 <= v < V and capacity >= 0:
                network.add_edge(u, v, capacity, cost)
            else:
                print(f"忽略无效边：{u} - {v}")
        
        while True:
            print("\n请选择算法：")
            print("1. Ford-Fulkerson算法")
            print("2. Edmonds-Karp算法")
            print("3. 最小费用最大流")
            print("4. 优化算法")
            print("5. 退出")
            
            choice = input("请输入选择（1-5）：")
            
            if choice == '1':
                max_flow = network.ford_fulkerson(source, sink)
                print(f"\n最大流：{max_flow}")
            
            elif choice == '2':
                max_flow = network.edmonds_karp(source, sink)
                print(f"\n最大流：{max_flow}")
            
            elif choice == '3':
                max_flow, min_cost = network.min_cost_max_flow(source, sink)
                print(f"\n最大流：{max_flow}")
                print(f"最小费用：{min_cost}")
            
            elif choice == '4':
                max_flow, total_cost = network.optimize_flow(source, sink)
                print(f"\n最大流：{max_flow}")
                print(f"总费用：{total_cost}")
            
            elif choice == '5':
                break
            
            else:
                print("无效的选择！")
            
            # 打印操作过程
            print_operations(network.steps)
            network.steps.clear()  # 清空步骤记录
        
    except ValueError as e:
        print(f"错误：{str(e)}") 