#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现配对堆（Pairing Heap）及其基本操作。

程序分析：
1. 实现配对堆的基本结构
2. 实现合并操作
3. 实现插入和删除操作
4. 优化配对过程
"""

from typing import Optional, List
from collections import deque

class PairingNode:
    def __init__(self, val: int):
        self.val = val          # 节点值
        self.child = None       # 第一个子节点
        self.sibling = None     # 下一个兄弟节点
        self.prev = None        # 前一个节点（父节点或兄弟节点）

class PairingHeap:
    def __init__(self):
        self.root = None
        self.size = 0
        self.steps = []  # 记录操作步骤
    
    def _link(self, first: PairingNode, second: PairingNode) -> PairingNode:
        """链接两个节点，返回较小值节点"""
        if first.val <= second.val:
            self._add_child(first, second)
            self.steps.append((first.val, second.val, "链接节点"))
            return first
        else:
            self._add_child(second, first)
            self.steps.append((second.val, first.val, "链接节点"))
            return second
    
    def _add_child(self, parent: PairingNode, child: PairingNode) -> None:
        """将child添加为parent的子节点"""
        child.prev = parent
        child.sibling = parent.child
        if parent.child:
            parent.child.prev = child
        parent.child = child
    
    def _merge_pairs(self, first: Optional[PairingNode]) -> Optional[PairingNode]:
        """两两配对合并兄弟节点"""
        if not first or not first.sibling:
            return first
        
        # 保存下一对节点的开始
        next_pair = first.sibling.sibling
        
        # 合并当前一对节点
        result = self._link(first, first.sibling)
        result.sibling = self._merge_pairs(next_pair)
        if result.sibling:
            result.sibling.prev = result
        
        return result
    
    def insert(self, val: int) -> None:
        """插入新值"""
        new_node = PairingNode(val)
        self.steps.append((val, "创建新节点"))
        
        if not self.root:
            self.root = new_node
        else:
            self.root = self._link(self.root, new_node)
        
        self.size += 1
    
    def get_min(self) -> Optional[int]:
        """获取最小值"""
        return self.root.val if self.root else None
    
    def delete_min(self) -> Optional[int]:
        """删除并返回最小值"""
        if not self.root:
            return None
        
        min_val = self.root.val
        old_root = self.root
        self.root = self._merge_pairs(self.root.child)
        if self.root:
            self.root.prev = None
        
        self.size -= 1
        self.steps.append((min_val, "删除最小值"))
        return min_val
    
    def merge(self, other: 'PairingHeap') -> None:
        """合并两个堆"""
        if not other.root:
            return
        if not self.root:
            self.root = other.root
        else:
            self.root = self._link(self.root, other.root)
        
        self.size += other.size
        other.root = None
        other.size = 0

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if len(step) == 2:
            val, operation = step
            if operation == "创建新节点":
                print(f"{operation}：值 {val}")
            else:  # 删除最小值
                print(f"{operation}：{val}")
        else:  # 链接节点
            val1, val2, operation = step
            print(f"{operation}：值 {val1} 和 {val2}")

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
        # 创建配对堆
        heap = PairingHeap()
        
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
            print("3. 查看最小值")
            print("4. 退出")
            
            choice = input("请输入选择（1-4）：")
            
            if choice == '1':
                try:
                    num = int(input("请输入要插入的数字："))
                    heap.insert(num)
                    print("插入成功！")
                except ValueError:
                    print("请输入有效的整数！")
            
            elif choice == '2':
                min_val = heap.delete_min()
                if min_val is not None:
                    print(f"删除的最小值为：{min_val}")
                else:
                    print("堆为空！")
            
            elif choice == '3':
                min_val = heap.get_min()
                if min_val is not None:
                    print(f"当前最小值为：{min_val}")
                else:
                    print("堆为空！")
            
            elif choice == '4':
                break
            
            else:
                print("无效的选择！")
        
        # 打印操作过程
        print_operations(heap.steps)
        
    except ValueError as e:
        print(f"错误：{str(e)}") 