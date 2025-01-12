#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现拓扑排序问题的解决方案。

程序分析：
1. 实现Kahn算法
2. 实现DFS算法
3. 实现分层排序
4. 优化求解过程
"""

from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict, deque
import time

class Graph:
    def __init__(self, vertices: int):
        self.V = vertices  # 顶点数
        self.graph = defaultdict(set)  # 邻接表
        self.steps = []  # 记录操作步骤
    
    def add_edge(self, u: int, v: int) -> None:
        """添加边"""
        self.graph[u].add(v)
        self.steps.append((u, v, "添加边"))
    
    def kahn(self) -> Optional[List[int]]:
        """Kahn算法实现拓扑排序"""
        # 计算每个顶点的入度
        in_degree = defaultdict(int)
        for u in range(self.V):
            for v in self.graph[u]:
                in_degree[v] += 1
        
        # 将所有入度为0的顶点加入队列
        queue = deque([u for u in range(self.V) if in_degree[u] == 0])
        result = []
        
        while queue:
            u = queue.popleft()
            result.append(u)
            self.steps.append((u, "访问顶点"))
            
            # 删除从u出发的所有边
            for v in self.graph[u]:
                in_degree[v] -= 1
                self.steps.append((u, v, "删除边"))
                if in_degree[v] == 0:
                    queue.append(v)
        
        # 检查是否存在环
        if len(result) != self.V:
            self.steps.append(("检测到环",))
            return None
        
        return result
    
    def dfs_topological_sort(self) -> Optional[List[int]]:
        """DFS实现拓扑排序"""
        visited = set()
        temp = set()  # 临时标记，用于检测环
        result = []
        
        def dfs(v: int) -> bool:
            if v in temp:  # 检测到环
                self.steps.append(("检测到环",))
                return False
            if v in visited:
                return True
            
            temp.add(v)
            self.steps.append((v, "临时标记"))
            
            # 访问所有邻居
            for u in self.graph[v]:
                if not dfs(u):
                    return False
            
            temp.remove(v)
            visited.add(v)
            result.append(v)
            self.steps.append((v, "永久标记"))
            return True
        
        # 对每个未访问的顶点进行DFS
        for v in range(self.V):
            if v not in visited:
                if not dfs(v):
                    return None
        
        return list(reversed(result))
    
    def layered_topological_sort(self) -> Optional[List[List[int]]]:
        """分层拓扑排序"""
        # 计算每个顶点的入度
        in_degree = defaultdict(int)
        for u in range(self.V):
            for v in self.graph[u]:
                in_degree[v] += 1
        
        # 初始化第一层（入度为0的顶点）
        current_layer = [u for u in range(self.V) if in_degree[u] == 0]
        if not current_layer:
            self.steps.append(("检测到环",))
            return None
        
        layers = []
        visited = set()
        
        while current_layer:
            # 记录当前层
            layers.append(current_layer)
            self.steps.append((current_layer.copy(), "添加层"))
            next_layer = []
            
            # 处理当前层的所有顶点
            for u in current_layer:
                visited.add(u)
                # 更新邻居的入度
                for v in self.graph[u]:
                    in_degree[v] -= 1
                    self.steps.append((u, v, "删除边"))
                    # 如果入度变为0且未访问，加入下一层
                    if in_degree[v] == 0 and v not in visited:
                        next_layer.append(v)
            
            current_layer = sorted(next_layer)  # 保持每层有序
        
        # 检查是否所有顶点都被访问
        if len(visited) != self.V:
            self.steps.append(("检测到环",))
            return None
        
        return layers
    
    def optimize_topological_sort(self) -> Optional[List[int]]:
        """优化的拓扑排序算法"""
        # 预处理：检查是否存在自环
        for v in range(self.V):
            if v in self.graph[v]:
                self.steps.append((v, "检测到自环"))
                return None
        
        # 计算每个顶点的入度和出度
        in_degree = defaultdict(int)
        out_degree = defaultdict(int)
        for u in range(self.V):
            out_degree[u] = len(self.graph[u])
            for v in self.graph[u]:
                in_degree[v] += 1
        
        # 如果图比较稀疏，使用Kahn算法
        if sum(len(edges) for edges in self.graph.values()) < self.V * 2:
            return self.kahn()
        # 如果图比较密集，使用DFS算法
        else:
            return self.dfs_topological_sort()

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if len(step) == 1:
            operation = step[0]
            print(f"{operation}")
        elif len(step) == 2:
            val, operation = step
            if operation == "访问顶点":
                print(f"访问顶点：{val}")
            elif operation == "临时标记":
                print(f"临时标记顶点：{val}")
            elif operation == "永久标记":
                print(f"永久标记顶点：{val}")
            elif operation == "检测到自环":
                print(f"检测到顶点 {val} 存在自环")
            elif operation == "添加层":
                print(f"添加新层：{val}")
        elif len(step) == 3:
            u, v, operation = step
            if operation == "添加边":
                print(f"添加边：{u} -> {v}")
            elif operation == "删除边":
                print(f"删除边：{u} -> {v}")

if __name__ == '__main__':
    try:
        # 获取输入
        V = int(input("请输入顶点数量："))
        E = int(input("请输入边的数量："))
        
        # 创建图
        graph = Graph(V)
        
        # 输入边
        print("\n请输入边（每行：起点 终点）：")
        for _ in range(E):
            u, v = map(int, input().strip().split())
            if 0 <= u < V and 0 <= v < V:
                graph.add_edge(u, v)
            else:
                print(f"忽略无效边：{u} -> {v}")
        
        while True:
            print("\n请选择算法：")
            print("1. Kahn算法")
            print("2. DFS算法")
            print("3. 分层排序")
            print("4. 优化算法")
            print("5. 退出")
            
            choice = input("请输入选择（1-5）：")
            
            if choice == '1':
                result = graph.kahn()
                if result is not None:
                    print("\n拓扑排序结果：")
                    print(" -> ".join(map(str, result)))
                else:
                    print("\n图中存在环，无法进行拓扑排序！")
            
            elif choice == '2':
                result = graph.dfs_topological_sort()
                if result is not None:
                    print("\n拓扑排序结果：")
                    print(" -> ".join(map(str, result)))
                else:
                    print("\n图中存在环，无法进行拓扑排序！")
            
            elif choice == '3':
                layers = graph.layered_topological_sort()
                if layers is not None:
                    print("\n分层拓扑排序结果：")
                    for i, layer in enumerate(layers, 1):
                        print(f"第{i}层：{layer}")
                else:
                    print("\n图中存在环，无法进行拓扑排序！")
            
            elif choice == '4':
                result = graph.optimize_topological_sort()
                if result is not None:
                    print("\n拓扑排序结果：")
                    print(" -> ".join(map(str, result)))
                else:
                    print("\n图中存在环，无法进行拓扑排序！")
            
            elif choice == '5':
                break
            
            else:
                print("无效的选择！")
                continue
            
            # 打印操作过程
            print_operations(graph.steps)
            graph.steps.clear()  # 清空步骤记录
        
    except ValueError as e:
        print(f"错误：{str(e)}") 