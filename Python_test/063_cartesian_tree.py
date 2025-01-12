#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现笛卡尔树（Cartesian Tree）及其基本操作。

程序分析：
1. 实现笛卡尔树的构建
2. 实现区间最值查询
3. 实现树形结构维护
4. 优化构建过程
"""

from typing import List, Optional, Tuple

class CartesianNode:
    def __init__(self, val: int, idx: int):
        self.val = val      # 节点值
        self.idx = idx      # 原数组中的位置
        self.left = None    # 左子节点
        self.right = None   # 右子节点
        self.parent = None  # 父节点

class CartesianTree:
    def __init__(self, arr: List[int]):
        self.arr = arr
        self.n = len(arr)
        self.root = None
        self.nodes = [CartesianNode(val, i) for i, val in enumerate(arr)]
        self.steps = []  # 记录操作步骤
        self._build()
    
    def _build(self) -> None:
        """构建笛卡尔树"""
        stack = []  # 单调栈
        
        for i in range(self.n):
            last = None
            while stack and self.nodes[stack[-1]].val > self.nodes[i].val:
                last = stack.pop()
                self.steps.append((last, i, "弹出栈顶"))
            
            if stack:
                self.nodes[stack[-1]].right = self.nodes[i]
                self.nodes[i].parent = self.nodes[stack[-1]]
                self.steps.append((stack[-1], i, "连接右子节点"))
            
            if last is not None:
                self.nodes[i].left = self.nodes[last]
                self.nodes[last].parent = self.nodes[i]
                self.steps.append((i, last, "连接左子节点"))
            
            stack.append(i)
            self.steps.append((i, "入栈"))
        
        # 找到根节点
        if stack:
            self.root = self.nodes[stack[0]]
            self.steps.append((stack[0], "设置根节点"))
    
    def find_rmq(self, left: int, right: int) -> int:
        """查找区间最小值"""
        if left > right:
            left, right = right, left
        
        # 找到区间内所有节点的最近公共祖先
        lca = self._find_lca(left, right)
        self.steps.append((left, right, lca.idx, "查找LCA"))
        return lca.idx
    
    def _find_lca(self, left: int, right: int) -> CartesianNode:
        """查找两个节点的最近公共祖先"""
        u, v = self.nodes[left], self.nodes[right]
        
        while u.idx != v.idx:
            if u.idx > v.idx:
                if u.parent and u == u.parent.right:
                    u = u.parent
                else:
                    v = v.parent
            else:
                if v.parent and v == v.parent.right:
                    v = v.parent
                else:
                    u = u.parent
            
            if not u.parent and not v.parent:
                break
            
            self.steps.append((u.idx, v.idx, "LCA查找过程"))
        
        return u

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if len(step) == 2:
            if isinstance(step[0], int):
                idx, operation = step
                if operation == "入栈":
                    print(f"{operation}：节点 {idx}")
                else:  # 设置根节点
                    print(f"{operation}：节点 {idx}")
        elif len(step) == 3:
            if isinstance(step[2], str):  # 连接操作
                u, v, operation = step
                print(f"{operation}：节点 {u} 和 {v}")
            else:  # LCA查找结果
                left, right, lca = step
                print(f"找到LCA：区间 [{left}, {right}] 的LCA为 {lca}")
        else:
            u, v, operation = step
            print(f"{operation}：当前节点 {u} 和 {v}")

def get_input_array() -> List[int]:
    """获取用户输入的数组"""
    arr = []
    print("请输入数组元素（每行一个，输入非数字结束）：")
    while True:
        try:
            num = int(input())
            arr.append(num)
        except ValueError:
            break
    return arr

if __name__ == '__main__':
    try:
        # 获取输入数组
        arr = get_input_array()
        if not arr:
            raise ValueError("数组不能为空！")
        
        # 创建笛卡尔树
        ct = CartesianTree(arr)
        print("\n原始数组：", arr)
        
        while True:
            print("\n请选择操作：")
            print("1. 查询区间最小值")
            print("2. 退出")
            
            choice = input("请输入选择（1-2）：")
            
            if choice == '1':
                try:
                    left = int(input(f"请输入左端点（0-{len(arr)-1}）："))
                    right = int(input(f"请输入右端点（0-{len(arr)-1}）："))
                    
                    if 0 <= left < len(arr) and 0 <= right < len(arr):
                        idx = ct.find_rmq(left, right)
                        print(f"\n区间 [{left}, {right}] 的最小值位置为：{idx}，值为：{arr[idx]}")
                    else:
                        print("无效的区间范围！")
                except ValueError:
                    print("请输入有效的整数！")
            
            elif choice == '2':
                break
            
            else:
                print("无效的选择！")
        
        # 打印操作过程
        print_operations(ct.steps)
        
    except ValueError as e:
        print(f"错误：{str(e)}") 