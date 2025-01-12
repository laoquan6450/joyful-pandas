#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现伸展树（Splay Tree）及其基本操作。

程序分析：
1. 实现伸展树的节点结构
2. 实现旋转和伸展操作
3. 实现插入、删除、查找操作
4. 维护BST性质和自调整
"""

from typing import Optional, List, Tuple

class SplayNode:
    def __init__(self, key: int):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None

class SplayTree:
    def __init__(self):
        self.root = None
        self.steps = []  # 记录操作步骤
    
    def _rotate_right(self, x: SplayNode) -> None:
        """右旋"""
        y = x.left
        x.left = y.right
        if y.right:
            y.right.parent = x
        y.parent = x.parent
        
        if not x.parent:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
            
        y.right = x
        x.parent = y
        self.steps.append((x.key, y.key, "右旋"))
    
    def _rotate_left(self, x: SplayNode) -> None:
        """左旋"""
        y = x.right
        x.right = y.left
        if y.left:
            y.left.parent = x
        y.parent = x.parent
        
        if not x.parent:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
            
        y.left = x
        x.parent = y
        self.steps.append((x.key, y.key, "左旋"))
    
    def _splay(self, x: SplayNode) -> None:
        """将节点x伸展到根节点"""
        while x.parent:
            if not x.parent.parent:  # Zig
                if x == x.parent.left:
                    self._rotate_right(x.parent)
                else:
                    self._rotate_left(x.parent)
            elif x == x.parent.left and x.parent == x.parent.parent.left:  # Zig-Zig
                self._rotate_right(x.parent.parent)
                self._rotate_right(x.parent)
            elif x == x.parent.right and x.parent == x.parent.parent.right:  # Zig-Zig
                self._rotate_left(x.parent.parent)
                self._rotate_left(x.parent)
            elif x == x.parent.right and x.parent == x.parent.parent.left:  # Zig-Zag
                self._rotate_left(x.parent)
                self._rotate_right(x.parent)
            else:  # Zig-Zag
                self._rotate_right(x.parent)
                self._rotate_left(x.parent)
    
    def insert(self, key: int) -> None:
        """插入关键字"""
        if not self.root:
            self.root = SplayNode(key)
            self.steps.append((key, None, "创建根节点"))
            return
        
        current = self.root
        while True:
            if key < current.key:
                if not current.left:
                    current.left = SplayNode(key)
                    current.left.parent = current
                    self.steps.append((key, current.key, "插入为左子节点"))
                    self._splay(current.left)
                    break
                current = current.left
            else:
                if not current.right:
                    current.right = SplayNode(key)
                    current.right.parent = current
                    self.steps.append((key, current.key, "插入为右子节点"))
                    self._splay(current.right)
                    break
                current = current.right

    def find(self, key: int) -> bool:
        """查找关键字"""
        if not self.root:
            return False
        
        current = self.root
        parent = None
        while current:
            if key == current.key:
                self.steps.append((key, current.key, "找到"))
                self._splay(current)
                return True
            parent = current
            if key < current.key:
                self.steps.append((key, current.key, "向左查找"))
                current = current.left
            else:
                self.steps.append((key, current.key, "向右查找"))
                current = current.right
        
        if parent:
            self._splay(parent)
        return False

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, (key1, key2, operation) in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if operation == "创建根节点":
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
        # 创建伸展树
        splay_tree = SplayTree()
        
        # 获取输入数字并插入
        numbers = get_input_numbers()
        print(f"\n插入的数字：{numbers}")
        for num in numbers:
            splay_tree.insert(num)
        
        while True:
            print("\n请选择操作：")
            print("1. 插入数字")
            print("2. 查找数字")
            print("3. 退出")
            
            choice = input("请输入选择（1-3）：")
            
            if choice == '1':
                num = int(input("请输入要插入的数字："))
                splay_tree.insert(num)
                print("插入成功！")
            
            elif choice == '2':
                num = int(input("请输入要查找的数字："))
                found = splay_tree.find(num)
                print("找到数字！" if found else "未找到数字！")
            
            elif choice == '3':
                break
            
            else:
                print("无效的选择！")
        
        # 打印操作过程
        print_operations(splay_tree.steps)
        
    except ValueError as e:
        print(f"错误：{str(e)}") 