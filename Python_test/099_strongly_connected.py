#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现强连通分量问题的解决方案。

程序分析：
1. 实现Kosaraju算法
2. 实现Tarjan算法
3. 实现Gabow算法
4. 优化求解过程
"""

from typing import List, Dict, Set, Tuple
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
        self.steps.append((u, v, "添加边"))
    
    def get_transpose(self) -> 'Graph':
        """获取图的转置（反向所有边）"""
        g = Graph(self.V)
        for u in self.graph:
            for v in self.graph[u]:
                g.add_edge(v, u)
        return g
    
    def kosaraju(self) -> List[Set[int]]:
        """Kosaraju算法求解强连通分量"""
        # 第一次DFS，获取结束时间顺序
        visited = set()
        finish_order = []
        
        def dfs1(v: int):
            visited.add(v)
            self.steps.append((v, "访问顶点"))
            for u in self.graph[v]:
                if u not in visited:
                    dfs1(u)
            finish_order.append(v)
        
        for v in range(self.V):
            if v not in visited:
                dfs1(v)
        
        # 获取转置图
        gt = self.get_transpose()
        
        # 第二次DFS，找出强连通分量
        visited.clear()
        scc = []
        
        def dfs2(v: int, component: Set[int]):
            visited.add(v)
            component.add(v)
            self.steps.append((v, "添加到分量"))
            for u in gt.graph[v]:
                if u not in visited:
                    dfs2(u, component)
        
        # 按完成时间逆序遍历
        for v in reversed(finish_order):
            if v not in visited:
                component = set()
                dfs2(v, component)
                scc.append(component)
        
        return scc
    
    def tarjan(self) -> List[Set[int]]:
        """Tarjan算法求解强连通分量"""
        index = 0
        stack = []
        on_stack = set()
        indices = {}
        lowlink = {}
        scc = []
        
        def strongconnect(v: int):
            nonlocal index
            indices[v] = index
            lowlink[v] = index
            index += 1
            stack.append(v)
            on_stack.add(v)
            self.steps.append((v, "访问顶点"))
            
            # 考虑所有邻居
            for w in self.graph[v]:
                if w not in indices:
                    # 邻居未访问
                    strongconnect(w)
                    lowlink[v] = min(lowlink[v], lowlink[w])
                elif w in on_stack:
                    # 邻居在栈中
                    lowlink[v] = min(lowlink[v], indices[w])
            
            # 如果v是强连通分量的根
            if lowlink[v] == indices[v]:
                component = set()
                while True:
                    w = stack.pop()
                    on_stack.remove(w)
                    component.add(w)
                    self.steps.append((w, "添加到分量"))
                    if w == v:
                        break
                scc.append(component)
        
        for v in range(self.V):
            if v not in indices:
                strongconnect(v)
        
        return scc
    
    def gabow(self) -> List[Set[int]]:
        """Gabow算法求解强连通分量"""
        index = 0
        stack1 = []  # 访问栈
        stack2 = []  # 分量栈
        indices = {}
        scc = []
        
        def strongconnect(v: int):
            nonlocal index
            indices[v] = index
            index += 1
            stack1.append(v)
            stack2.append(v)
            self.steps.append((v, "访问顶点"))
            
            # 访问所有邻居
            for w in self.graph[v]:
                if w not in indices:
                    strongconnect(w)
                elif w in set(stack1):
                    # 弹出直到w的所有顶点
                    while indices[stack2[-1]] > indices[w]:
                        stack2.pop()
            
            # 如果v是强连通分量的根
            if stack2[-1] == v:
                component = set()
                stack2.pop()
                while True:
                    w = stack1.pop()
                    component.add(w)
                    self.steps.append((w, "添加到分量"))
                    if w == v:
                        break
                scc.append(component)
        
        for v in range(self.V):
            if v not in indices:
                strongconnect(v)
        
        return scc
    
    def optimize_scc(self) -> List[Set[int]]:
        """优化的强连通分量算法"""
        # 预处理：移除自环
        self_loops = set()
        for v in range(self.V):
            if v in self.graph[v]:
                self_loops.add(v)
                self.graph[v].remove(v)
                self.steps.append((v, "移除自环"))
        
        # 使用Tarjan算法（通常比其他算法更高效）
        scc = self.tarjan()
        
        # 处理自环
        for v in self_loops:
            # 找到包含v的分量
            for component in scc:
                if v in component:
                    break
            else:
                # 如果v不在任何分量中，创建新分量
                scc.append({v})
                self.steps.append((v, "添加单点分量"))
        
        return scc

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if len(step) == 2:
            vertex, operation = step
            if operation == "访问顶点":
                print(f"访问顶点：{vertex}")
            elif operation == "添加到分量":
                print(f"将顶点 {vertex} 添加到当前分量")
            elif operation == "移除自环":
                print(f"移除顶点 {vertex} 的自环")
            elif operation == "添加单点分量":
                print(f"添加单点分量：{vertex}")
        elif len(step) == 3:
            u, v, operation = step
            if operation == "添加边":
                print(f"添加边：{u} -> {v}")

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
            print("1. Kosaraju算法")
            print("2. Tarjan算法")
            print("3. Gabow算法")
            print("4. 优化算法")
            print("5. 退出")
            
            choice = input("请输入选择（1-5）：")
            
            if choice == '1':
                scc = graph.kosaraju()
            elif choice == '2':
                scc = graph.tarjan()
            elif choice == '3':
                scc = graph.gabow()
            elif choice == '4':
                scc = graph.optimize_scc()
            elif choice == '5':
                break
            else:
                print("无效的选择！")
                continue
            
            print("\n强连通分量：")
            for i, component in enumerate(scc, 1):
                print(f"分量 {i}：{sorted(component)}")
            
            # 打印操作过程
            print_operations(graph.steps)
            graph.steps.clear()  # 清空步骤记录
        
    except ValueError as e:
        print(f"错误：{str(e)}") 