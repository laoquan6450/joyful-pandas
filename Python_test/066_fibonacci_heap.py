#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现斐波那契堆（Fibonacci Heap）及其基本操作。

程序分析：
1. 实现斐波那契堆的基本结构
2. 实现合并和插入操作
3. 实现删除最小值操作
4. 实现关键字减值操作
"""

from typing import Optional, List, Dict
from math import log2

class FibNode:
    def __init__(self, key: int):
        self.key = key          # 关键字值
        self.degree = 0         # 子节点数量
        self.marked = False     # 标记状态
        self.parent = None      # 父节点
        self.child = None       # 子节点
        self.left = self        # 左兄弟
        self.right = self       # 右兄弟

class FibonacciHeap:
    def __init__(self):
        self.min = None         # 最小节点
        self.total = 0          # 节点总数
        self.steps = []         # 记录操作步骤
    
    def _add_to_root_list(self, node: FibNode) -> None:
        """将节点添加到根链表"""
        if not self.min:
            self.min = node
        else:
            node.right = self.min.right
            node.left = self.min
            self.min.right.left = node
            self.min.right = node
            if node.key < self.min.key:
                self.min = node
        self.steps.append((node.key, "添加到根链表"))
    
    def insert(self, key: int) -> None:
        """插入新节点"""
        node = FibNode(key)
        self._add_to_root_list(node)
        self.total += 1
        self.steps.append((key, "插入新节点"))
    
    def _consolidate(self) -> None:
        """合并度数相同的树"""
        max_degree = int(log2(self.total)) + 1
        degree_table: Dict[int, FibNode] = {}
        
        # 收集所有根节点
        current = self.min
        root_nodes = []
        if current:
            while True:
                root_nodes.append(current)
                current = current.right
                if current == self.min:
                    break
        
        # 合并相同度数的树
        for node in root_nodes:
            degree = node.degree
            while degree in degree_table:
                other = degree_table[degree]
                if node.key > other.key:
                    node, other = other, node
                
                # 将other作为node的子节点
                other.parent = node
                if not node.child:
                    node.child = other
                    other.right = other
                    other.left = other
                else:
                    other.right = node.child.right
                    other.left = node.child
                    node.child.right.left = other
                    node.child.right = other
                
                node.degree += 1
                degree_table.pop(degree)
                degree += 1
                self.steps.append((node.key, other.key, "合并树"))
            
            degree_table[degree] = node
        
        # 重建根链表
        self.min = None
        for degree, node in degree_table.items():
            node.parent = None
            self._add_to_root_list(node)
    
    def extract_min(self) -> Optional[int]:
        """删除并返回最小值"""
        if not self.min:
            return None
        
        min_key = self.min.key
        
        # 将最小节点的子节点添加到根链表
        if self.min.child:
            current = self.min.child
            while True:
                next_node = current.right
                current.parent = None
                self._add_to_root_list(current)
                current = next_node
                if current == self.min.child:
                    break
        
        # 从根链表中移除最小节点
        if self.min.right == self.min:
            self.min = None
        else:
            self.min.left.right = self.min.right
            self.min.right.left = self.min.left
            self.min = self.min.right
            self._consolidate()
        
        self.total -= 1
        self.steps.append((min_key, "删除最小值"))
        return min_key
    
    def decrease_key(self, node: FibNode, new_key: int) -> None:
        """减小节点的关键字值"""
        if new_key > node.key:
            return
        
        node.key = new_key
        parent = node.parent
        
        if parent and node.key < parent.key:
            self._cut(node, parent)
            self._cascading_cut(parent)
        
        if node.key < self.min.key:
            self.min = node
        
        self.steps.append((node.key, new_key, "减小关键字"))
    
    def _cut(self, node: FibNode, parent: FibNode) -> None:
        """将节点从父节点分离"""
        parent.degree -= 1
        if parent.child == node:
            if node.right == node:
                parent.child = None
            else:
                parent.child = node.right
        
        node.left.right = node.right
        node.right.left = node.left
        node.parent = None
        node.marked = False
        self._add_to_root_list(node)
        self.steps.append((node.key, parent.key, "切断连接"))
    
    def _cascading_cut(self, node: FibNode) -> None:
        """级联切断"""
        parent = node.parent
        if parent:
            if not node.marked:
                node.marked = True
            else:
                self._cut(node, parent)
                self._cascading_cut(parent)

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if len(step) == 2:
            val, operation = step
            if operation == "添加到根链表":
                print(f"{operation}：节点 {val}")
            elif operation == "插入新节点":
                print(f"{operation}：值 {val}")
            else:  # 删除最小值
                print(f"{operation}：{val}")
        else:  # len(step) == 3
            val1, val2, operation = step
            if operation == "合并树":
                print(f"{operation}：节点 {val1} 和 {val2}")
            elif operation == "减小关键字":
                print(f"{operation}：从 {val1} 到 {val2}")
            else:  # 切断连接
                print(f"{operation}：节点 {val1} 与父节点 {val2}")

def get_input_numbers() -> List[int]:
    """获取用户输入的数字"""
    numbers = []
    print("请输入要插入的数字（每行一个，输入非数字结束）：")
    while True:
        try:
            num = int(input())
            numbers.append(num)
        except ValueError:
            break
    return numbers

if __name__ == '__main__':
    try:
        # 创建斐波那契堆
        heap = FibonacciHeap()
        
        # 获取输入数字并插入
        numbers = get_input_numbers()
        if not numbers:
            raise ValueError("至少需要输入一个数字！")
        
        print("\n插入的数字：", numbers)
        for num in numbers:
            heap.insert(num)
        
        while True:
            print("\n请选择操作：")
            print("1. 插入数字")
            print("2. 删除最小值")
            print("3. 退出")
            
            choice = input("请输入选择（1-3）：")
            
            if choice == '1':
                try:
                    num = int(input("请输入要插入的数字："))
                    heap.insert(num)
                    print("插入成功！")
                except ValueError:
                    print("请输入有效的整数！")
            
            elif choice == '2':
                min_val = heap.extract_min()
                if min_val is not None:
                    print(f"删除的最小值为：{min_val}")
                else:
                    print("堆为空！")
            
            elif choice == '3':
                break
            
            else:
                print("无效的选择！")
        
        # 打印操作过程
        print_operations(heap.steps)
        
    except ValueError as e:
        print(f"错误：{str(e)}") 