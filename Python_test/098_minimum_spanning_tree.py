#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现最小生成树问题的解决方案。

程序分析：
1. 实现Prim算法
2. 实现Kruskal算法
3. 实现Boruvka算法
4. 优化求解过程
"""

from typing import List, Dict, Set, Tuple
from collections import defaultdict
import heapq

class UnionFind:
    def __init__(self, size: int):
        self.parent = list(range(size))
        self.rank = [0] * size
    
    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x: int, y: int) -> bool:
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True

class Graph:
    def __init__(self, vertices: int):
        self.V = vertices  # 顶点数
        self.graph = defaultdict(dict)  # 邻接表存储边权重
        self.steps = []  # 记录操作步骤
    
    def add_edge(self, u: int, v: int, weight: float) -> None:
        """添加边"""
        self.graph[u][v] = weight
        self.graph[v][u] = weight  # 无向图
        self.steps.append((u, v, weight, "添加边"))
    
    def prim(self) -> List[Tuple[int, int, float]]:
        """Prim算法求解最小生成树"""
        if not self.graph:
            return []
        
        mst = []  # 存储最小生成树的边
        visited = {0}  # 从顶点0开始
        edges = []  # 优先队列存储(权重, 起点, 终点)
        
        # 将起点的所有边加入优先队列
        for v, weight in self.graph[0].items():
            heapq.heappush(edges, (weight, 0, v))
            self.steps.append((0, v, weight, "加入候选"))
        
        while edges and len(visited) < self.V:
            weight, u, v = heapq.heappop(edges)
            
            if v in visited:
                continue
            
            visited.add(v)
            mst.append((u, v, weight))
            self.steps.append((u, v, weight, "选择边"))
            
            # 将新顶点的边加入优先队列
            for next_v, next_weight in self.graph[v].items():
                if next_v not in visited:
                    heapq.heappush(edges, (next_weight, v, next_v))
                    self.steps.append((v, next_v, next_weight, "加入候选"))
        
        return mst if len(visited) == self.V else []
    
    def kruskal(self) -> List[Tuple[int, int, float]]:
        """Kruskal算法求解最小生成树"""
        if not self.graph:
            return []
        
        # 收集所有边并按权重排序
        edges = []
        for u in self.graph:
            for v, weight in self.graph[u].items():
                if u < v:  # 避免重复边
                    edges.append((weight, u, v))
        edges.sort()  # 按权重排序
        
        mst = []
        uf = UnionFind(self.V)
        
        for weight, u, v in edges:
            self.steps.append((u, v, weight, "检查边"))
            if uf.union(u, v):
                mst.append((u, v, weight))
                self.steps.append((u, v, weight, "选择边"))
                if len(mst) == self.V - 1:
                    break
        
        return mst if len(mst) == self.V - 1 else []
    
    def boruvka(self) -> List[Tuple[int, int, float]]:
        """Boruvka算法求解最小生成树"""
        if not self.graph:
            return []
        
        mst = []
        uf = UnionFind(self.V)
        
        while True:
            # 找到每个连通分量的最小权重边
            min_edges = {}  # 组件到其最小边的映射
            
            for u in range(self.V):
                for v, weight in self.graph[u].items():
                    comp_u = uf.find(u)
                    comp_v = uf.find(v)
                    
                    if comp_u != comp_v:
                        if comp_u not in min_edges or weight < min_edges[comp_u][2]:
                            min_edges[comp_u] = (u, v, weight)
                        if comp_v not in min_edges or weight < min_edges[comp_v][2]:
                            min_edges[comp_v] = (u, v, weight)
            
            if not min_edges:  # 没有可以添加的边
                break
            
            # 添加所有最小边到MST
            added = False
            for u, v, weight in min_edges.values():
                if uf.union(u, v):
                    mst.append((u, v, weight))
                    self.steps.append((u, v, weight, "选择边"))
                    added = True
            
            if not added:  # 没有新边被添加
                break
        
        return mst if len(mst) == self.V - 1 else []
    
    def optimize_mst(self) -> List[Tuple[int, int, float]]:
        """优化的最小生成树算法"""
        # 预处理：移除重复边，只保留权重最小的边
        processed_edges = {}
        for u in self.graph:
            for v, weight in self.graph[u].items():
                if u < v:  # 避免重复处理
                    edge = (u, v)
                    if edge not in processed_edges or weight < processed_edges[edge]:
                        processed_edges[edge] = weight
                        self.steps.append((u, v, weight, "预处理边"))
        
        # 创建新图
        optimized_graph = Graph(self.V)
        for (u, v), weight in processed_edges.items():
            optimized_graph.add_edge(u, v, weight)
        
        # 根据边的数量选择合适的算法
        if len(processed_edges) < self.V * 2:  # 稀疏图
            return optimized_graph.kruskal()
        else:  # 稠密图
            return optimized_graph.prim()

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        u, v, weight, operation = step
        if operation == "添加边":
            print(f"添加边：{u} - {v}，权重 {weight}")
        elif operation == "加入候选":
            print(f"将边 {u} - {v} (权重 {weight}) 加入候选集")
        elif operation == "选择边":
            print(f"选择边 {u} - {v} (权重 {weight}) 加入最小生成树")
        elif operation == "检查边":
            print(f"检查边 {u} - {v} (权重 {weight})")
        elif operation == "预处理边":
            print(f"预处理边 {u} - {v} (权重 {weight})")

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
            if 0 <= u < V and 0 <= v < V and u != v:
                graph.add_edge(u, v, weight)
            else:
                print(f"忽略无效边：{u} - {v}")
        
        while True:
            print("\n请选择算法：")
            print("1. Prim算法")
            print("2. Kruskal算法")
            print("3. Boruvka算法")
            print("4. 优化算法")
            print("5. 退出")
            
            choice = input("请输入选择（1-5）：")
            
            if choice == '1':
                mst = graph.prim()
            elif choice == '2':
                mst = graph.kruskal()
            elif choice == '3':
                mst = graph.boruvka()
            elif choice == '4':
                mst = graph.optimize_mst()
            elif choice == '5':
                break
            else:
                print("无效的选择！")
                continue
            
            if mst:
                total_weight = sum(weight for _, _, weight in mst)
                print("\n最小生成树的边：")
                for u, v, weight in mst:
                    print(f"{u} - {v}：权重 {weight}")
                print(f"总权重：{total_weight}")
            else:
                print("\n无法构建最小生成树！")
            
            # 打印操作过程
            print_operations(graph.steps)
            graph.steps.clear()  # 清空步骤记录
        
    except ValueError as e:
        print(f"错误：{str(e)}") 