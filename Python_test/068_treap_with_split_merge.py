#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现带分裂合并操作的Treap树。

程序分析：
1. 实现Treap的基本结构
2. 实现分裂(Split)操作
3. 实现合并(Merge)操作
4. 维护子树信息
"""

import random
from typing import Optional, Tuple, List

class TreapNode:
    def __init__(self, val: int):
        self.val = val          # 节点值
        self.priority = random.random()  # 随机优先级
        self.left = None        # 左子节点
        self.right = None       # 右子节点
        self.size = 1          # 子树大小

class Treap:
    def __init__(self):
        self.root = None
        self.steps = []  # 记录操作步骤
    
    def _get_size(self, node: Optional[TreapNode]) -> int:
        """获取节点的子树大小"""
        return node.size if node else 0
    
    def _update_size(self, node: TreapNode) -> None:
        """更新节点的子树大小"""
        node.size = 1 + self._get_size(node.left) + self._get_size(node.right)
    
    def _merge(self, left: Optional[TreapNode], right: Optional[TreapNode]) -> Optional[TreapNode]:
        """合并两棵树"""
        if not left or not right:
            return left or right
        
        if left.priority > right.priority:
            left.right = self._merge(left.right, right)
            self._update_size(left)
            self.steps.append((left.val, right.val, "合并节点"))
            return left
        else:
            right.left = self._merge(left, right.left)
            self._update_size(right)
            self.steps.append((left.val, right.val, "合并节点"))
            return right
    
    def _split(self, node: Optional[TreapNode], key: int) -> Tuple[Optional[TreapNode], Optional[TreapNode]]:
        """分裂树，返回(左子树, 右子树)"""
        if not node:
            return None, None
        
        if node.val <= key:
            left, right = self._split(node.right, key)
            node.right = left
            self._update_size(node)
            self.steps.append((node.val, key, "分裂右子树"))
            return node, right
        else:
            left, right = self._split(node.left, key)
            node.left = right
            self._update_size(node)
            self.steps.append((node.val, key, "分裂左子树"))
            return left, node
    
    def insert(self, val: int) -> None:
        """插入新值"""
        left, right = self._split(self.root, val)
        new_node = TreapNode(val)
        self.steps.append((val, "创建新节点"))
        self.root = self._merge(self._merge(left, new_node), right)
    
    def delete(self, val: int) -> None:
        """删除值"""
        left, right = self._split(self.root, val)
        left2, _ = self._split(left, val - 1)
        self.root = self._merge(left2, right)
        self.steps.append((val, "删除节点"))
    
    def find_kth(self, k: int) -> Optional[int]:
        """查找第k小的元素"""
        def _find_kth(node: Optional[TreapNode], k: int) -> Optional[TreapNode]:
            if not node:
                return None
            
            left_size = self._get_size(node.left)
            if left_size == k - 1:
                return node
            elif left_size >= k:
                return _find_kth(node.left, k)
            else:
                return _find_kth(node.right, k - left_size - 1)
        
        result = _find_kth(self.root, k)
        if result:
            self.steps.append((k, result.val, "查找第k小"))
            return result.val
        return None

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if len(step) == 2:
            val, operation = step
            if operation == "创建新节点":
                print(f"{operation}：值 {val}")
            else:  # 删除节点
                print(f"{operation}：值 {val}")
        else:  # len(step) == 3
            val1, val2, operation = step
            if operation == "合并节点":
                print(f"{operation}：值 {val1} 和 {val2}")
            elif operation.startswith("分裂"):
                print(f"{operation}：节点 {val1}，键值 {val2}")
            else:  # 查找第k小
                print(f"{operation}：k={val1}，结果={val2}")

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
        # 创建Treap
        treap = Treap()
        
        # 获取输入数字并插入
        numbers = get_input_numbers()
        if not numbers:
            raise ValueError("至少需要输入一个数字！")
        
        print("\n插入的数字：", numbers)
        for num in numbers:
            treap.insert(num)
        
        while True:
            print("\n请选择操作：")
            print("1. 插入数字")
            print("2. 删除数字")
            print("3. 查找第k小")
            print("4. 退出")
            
            choice = input("请输入选择（1-4）：")
            
            if choice == '1':
                try:
                    num = int(input("请输入要插入的数字："))
                    treap.insert(num)
                    print("插入成功！")
                except ValueError:
                    print("请输入有效的整数！")
            
            elif choice == '2':
                try:
                    num = int(input("请输入要删除的数字："))
                    treap.delete(num)
                    print("删除成功！")
                except ValueError:
                    print("请输入有效的整数！")
            
            elif choice == '3':
                try:
                    k = int(input("请输入k："))
                    result = treap.find_kth(k)
                    if result is not None:
                        print(f"第{k}小的数是：{result}")
                    else:
                        print("k值超出范围！")
                except ValueError:
                    print("请输入有效的整数！")
            
            elif choice == '4':
                break
            
            else:
                print("无效的选择！")
        
        # 打印操作过程
        print_operations(treap.steps)
        
    except ValueError as e:
        print(f"错误：{str(e)}") 