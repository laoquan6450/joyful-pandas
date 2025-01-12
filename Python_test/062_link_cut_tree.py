#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现动态树（Link Cut Tree）及其基本操作。

程序分析：
1. 实现Splay操作
2. 实现Access操作
3. 实现Link和Cut操作
4. 维护路径信息
"""

from typing import Optional, List

class LCTNode:
    def __init__(self, val: int):
        self.val = val          # 节点值
        self.sum = val          # 子树和
        self.left = None        # 左子节点
        self.right = None       # 右子节点
        self.parent = None      # 父节点
        self.reversed = False   # 翻转标记

class LinkCutTree:
    def __init__(self, n: int):
        self.nodes = [LCTNode(0) for _ in range(n)]
        self.steps = []  # 记录操作步骤
    
    def _is_root(self, x: LCTNode) -> bool:
        """判断是否为Splay树的根"""
        return (not x.parent or 
                (x.parent.left != x and x.parent.right != x))
    
    def _push_down(self, x: LCTNode) -> None:
        """下推标记"""
        if x.reversed:
            x.reversed = False
            if x.left:
                x.left.reversed = not x.left.reversed
            if x.right:
                x.right.reversed = not x.right.reversed
            x.left, x.right = x.right, x.left
            self.steps.append((x.val, "下推翻转标记"))
    
    def _update(self, x: LCTNode) -> None:
        """更新节点信息"""
        x.sum = x.val
        if x.left:
            x.sum += x.left.sum
        if x.right:
            x.sum += x.right.sum
        self.steps.append((x.val, x.sum, "更新节点信息"))
    
    def _rotate(self, x: LCTNode) -> None:
        """旋转操作"""
        y = x.parent
        z = y.parent
        
        if z:
            if z.left == y:
                z.left = x
            elif z.right == y:
                z.right = x
        x.parent = z
        
        if y.left == x:
            y.left = x.right
            if x.right:
                x.right.parent = y
            x.right = y
        else:
            y.right = x.left
            if x.left:
                x.left.parent = y
            x.left = y
        
        y.parent = x
        self._update(y)
        self._update(x)
        self.steps.append((x.val, y.val, "旋转"))
    
    def _splay(self, x: LCTNode) -> None:
        """Splay操作"""
        while not self._is_root(x):
            y = x.parent
            if not self._is_root(y):
                self._push_down(y.parent)
            self._push_down(y)
            self._push_down(x)
            
            if not self._is_root(y):
                z = y.parent
                if (z.left == y) == (y.left == x):
                    self._rotate(y)
                else:
                    self._rotate(x)
            self._rotate(x)
            self.steps.append((x.val, "Splay操作"))
    
    def _access(self, x: int) -> None:
        """Access操作"""
        node = self.nodes[x]
        last = None
        
        while node:
            self._splay(node)
            node.right = last
            self._update(node)
            last = node
            node = node.parent
            self.steps.append((x, "Access操作"))
    
    def make_root(self, x: int) -> None:
        """将x变为整棵树的根"""
        self._access(x)
        self._splay(self.nodes[x])
        self.nodes[x].reversed = not self.nodes[x].reversed
        self.steps.append((x, "变为树根"))
    
    def link(self, x: int, y: int) -> None:
        """连接两个节点"""
        self.make_root(x)
        self.nodes[x].parent = self.nodes[y]
        self.steps.append((x, y, "连接节点"))
    
    def cut(self, x: int, y: int) -> None:
        """断开两个节点的连接"""
        self.make_root(x)
        self._access(y)
        self._splay(self.nodes[y])
        if self.nodes[y].left == self.nodes[x]:
            self.nodes[y].left.parent = None
            self.nodes[y].left = None
            self._update(self.nodes[y])
            self.steps.append((x, y, "断开连接"))
    
    def query(self, x: int, y: int) -> int:
        """查询两点间路径上的节点值之和"""
        self.make_root(x)
        self._access(y)
        self._splay(self.nodes[y])
        result = self.nodes[y].sum
        self.steps.append((x, y, result, "查询路径和"))
        return result

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if len(step) == 2:
            x, operation = step
            if operation == "下推翻转标记":
                print(f"{operation}：节点 {x}")
            elif operation == "Splay操作":
                print(f"{operation}：节点 {x}")
            elif operation == "Access操作":
                print(f"{operation}：节点 {x}")
            else:  # 变为树根
                print(f"{operation}：节点 {x}")
        elif len(step) == 3:
            if isinstance(step[1], int):  # 更新节点信息
                x, sum_val, operation = step
                print(f"{operation}：节点 {x}，和为 {sum_val}")
            else:  # 连接/断开节点
                x, y, operation = step
                print(f"{operation}：节点 {x} 和 {y}")
        else:  # 查询路径和
            x, y, result, operation = step
            print(f"{operation}：节点 {x} 到 {y}，结果 {result}")

# ... [其余代码与之前类似，包括输入处理和主函数] 