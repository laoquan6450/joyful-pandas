#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现左偏树（Leftist Heap）及其基本操作。

程序分析：
1. 实现左偏树的基本结构
2. 实现合并操作
3. 实现插入和删除操作
4. 维护左偏性质
"""

from typing import Optional, List

class LeftistNode:
    def __init__(self, val: int):
        self.val = val          # 节点值
        self.left = None        # 左子节点
        self.right = None       # 右子节点
        self.npl = 0           # 零路径长度
        
class LeftistHeap:
    def __init__(self):
        self.root = None
        self.steps = []  # 记录操作步骤
    
    def _get_npl(self, node: Optional[LeftistNode]) -> int:
        """获取节点的零路径长度"""
        return node.npl if node else -1
    
    def _merge(self, h1: Optional[LeftistNode], h2: Optional[LeftistNode]) -> Optional[LeftistNode]:
        """合并两个左偏树"""
        if not h1:
            return h2
        if not h2:
            return h1
        
        # 确保h1的值小于h2
        if h1.val > h2.val:
            h1, h2 = h2, h1
            self.steps.append((h1.val, h2.val, "交换根节点"))
        
        # 递归合并右子树
        h1.right = self._merge(h1.right, h2)
        self.steps.append((h1.val, "合并右子树"))
        
        # 维护左偏性质
        if not h1.left or h1.left.npl < h1.right.npl:
            h1.left, h1.right = h1.right, h1.left
            self.steps.append((h1.val, "交换子树"))
        
        # 更新零路径长度
        h1.npl = self._get_npl(h1.right) + 1
        self.steps.append((h1.val, h1.npl, "更新NPL"))
        
        return h1
    
    def merge(self, other: 'LeftistHeap') -> None:
        """合并两个堆"""
        self.root = self._merge(self.root, other.root)
        other.root = None
    
    def insert(self, val: int) -> None:
        """插入新值"""
        new_node = LeftistNode(val)
        self.steps.append((val, "创建新节点"))
        self.root = self._merge(self.root, new_node)
    
    def delete_min(self) -> Optional[int]:
        """删除并返回最小值"""
        if not self.root:
            return None
        
        min_val = self.root.val
        self.root = self._merge(self.root.left, self.root.right)
        self.steps.append((min_val, "删除最小值"))
        return min_val
    
    def get_min(self) -> Optional[int]:
        """获取最小值"""
        return self.root.val if self.root else None

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if len(step) == 2:
            val, operation = step
            if operation == "创建新节点":
                print(f"{operation}：值 {val}")
            elif operation == "合并右子树":
                print(f"{operation}：当前节点 {val}")
            elif operation == "交换子树":
                print(f"{operation}：当前节点 {val}")
            else:  # 删除最小值
                print(f"{operation}：{val}")
        else:  # len(step) == 3
            if operation := step[2] == "交换根节点":
                val1, val2, _ = step
                print(f"{operation}：值 {val1} 和 {val2}")
            else:  # 更新NPL
                val, npl, _ = step
                print(f"{operation}：节点 {val} 的NPL更新为 {npl}")

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
        # 创建左偏堆
        heap = LeftistHeap()
        
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