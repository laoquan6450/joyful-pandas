#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现Treap（树堆）及其基本操作。

程序分析：
1. 实现Treap的节点结构
2. 实现旋转、插入、删除操作
3. 维护BST和堆的性质
4. 实现随机优先级
"""

import random
from typing import Optional, Tuple, List

class TreapNode:
    def __init__(self, key: int):
        self.key = key
        self.priority = random.random()  # 随机优先级
        self.left = None
        self.right = None
        self.size = 1  # 子树大小

class Treap:
    def __init__(self):
        self.root = None
        self.steps = []  # 记录操作步骤
    
    def _update_size(self, node: Optional[TreapNode]) -> None:
        """更新节点的子树大小"""
        if node:
            node.size = 1
            if node.left:
                node.size += node.left.size
            if node.right:
                node.size += node.right.size
    
    def _rotate_right(self, node: TreapNode) -> TreapNode:
        """右旋"""
        left_child = node.left
        node.left = left_child.right
        left_child.right = node
        self._update_size(node)
        self._update_size(left_child)
        self.steps.append((node.key, left_child.key, "右旋"))
        return left_child
    
    def _rotate_left(self, node: TreapNode) -> TreapNode:
        """左旋"""
        right_child = node.right
        node.right = right_child.left
        right_child.left = node
        self._update_size(node)
        self._update_size(right_child)
        self.steps.append((node.key, right_child.key, "左旋"))
        return right_child
    
    def _insert(self, node: Optional[TreapNode], key: int) -> TreapNode:
        """插入节点"""
        if not node:
            new_node = TreapNode(key)
            self.steps.append((key, None, "创建新节点"))
            return new_node
        
        if key < node.key:
            node.left = self._insert(node.left, key)
            self.steps.append((key, node.key, "插入到左子树"))
            if node.left.priority > node.priority:
                node = self._rotate_right(node)
        else:
            node.right = self._insert(node.right, key)
            self.steps.append((key, node.key, "插入到右子树"))
            if node.right.priority > node.priority:
                node = self._rotate_left(node)
        
        self._update_size(node)
        return node
    
    def insert(self, key: int) -> None:
        """插入关键字"""
        self.root = self._insert(self.root, key)
    
    def _find(self, node: Optional[TreapNode], key: int) -> bool:
        """查找关键字"""
        if not node:
            self.steps.append((key, None, "未找到"))
            return False
        
        if key == node.key:
            self.steps.append((key, node.key, "找到"))
            return True
        elif key < node.key:
            self.steps.append((key, node.key, "向左查找"))
            return self._find(node.left, key)
        else:
            self.steps.append((key, node.key, "向右查找"))
            return self._find(node.right, key)
    
    def find(self, key: int) -> bool:
        """查找关键字"""
        return self._find(self.root, key)

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, (key1, key2, operation) in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if operation == "创建新节点":
            print(f"{operation}：键值 {key1}")
        elif operation in ["左旋", "右旋"]:
            print(f"{operation}：节点 {key1} 和节点 {key2}")
        elif operation.startswith("插入"):
            print(f"{operation}：键值 {key1} 相对于节点 {key2}")
        else:  # 查找
            if key2 is None:
                print(f"{operation}：键值 {key1}")
            else:
                print(f"{operation}：键值 {key1}，当前节点 {key2}")

def get_input_numbers():
    """获取用户输入的数字"""
    numbers = []
    print("请输入5个不同的数字：")
    while len(numbers) < 5:
        try:
            num = int(input(f"请输入第{len(numbers)+1}个数字："))
            if num in numbers:
                print("该数字已存在，请输入不同的数字！")
                continue
            numbers.append(num)
        except ValueError:
            print("请输入有效的整数！")
    return numbers

if __name__ == '__main__':
    try:
        # 创建Treap
        treap = Treap()
        
        # 获取输入数字并插入
        numbers = get_input_numbers()
        print(f"\n插入的数字：{numbers}")
        for num in numbers:
            treap.insert(num)
        
        while True:
            print("\n请选择操作：")
            print("1. 插入数字")
            print("2. 查找数字")
            print("3. 退出")
            
            choice = input("请输入选择（1-3）：")
            
            if choice == '1':
                num = int(input("请输入要插入的数字："))
                treap.insert(num)
                print("插入成功！")
            
            elif choice == '2':
                num = int(input("请输入要查找的数字："))
                found = treap.find(num)
                print("找到数字！" if found else "未找到数字！")
            
            elif choice == '3':
                break
            
            else:
                print("无效的选择！")
        
        # 打印操作过程
        print_operations(treap.steps)
        
    except ValueError as e:
        print(f"错误：{str(e)}") 