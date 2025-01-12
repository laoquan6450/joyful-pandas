#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现替罪羊树（Scapegoat Tree）及其基本操作。

程序分析：
1. 实现替罪羊树的基本结构
2. 实现插入和删除操作
3. 实现树的重建操作
4. 维护平衡因子
"""

from typing import Optional, List
from math import log2

class ScapegoatNode:
    def __init__(self, val: int):
        self.val = val          # 节点值
        self.left = None        # 左子节点
        self.right = None       # 右子节点
        self.size = 1          # 子树大小

class ScapegoatTree:
    def __init__(self, alpha: float = 0.7):
        self.root = None
        self.size = 0           # 当前节点数
        self.max_size = 0       # 历史最大节点数
        self.alpha = alpha      # 平衡因子
        self.steps = []         # 记录操作步骤
    
    def _get_size(self, node: Optional[ScapegoatNode]) -> int:
        """获取节点的子树大小"""
        return node.size if node else 0
    
    def _update_size(self, node: ScapegoatNode) -> None:
        """更新节点的子树大小"""
        node.size = 1 + self._get_size(node.left) + self._get_size(node.right)
    
    def _is_unbalanced(self, node: ScapegoatNode) -> bool:
        """检查节点是否不平衡"""
        left_size = self._get_size(node.left)
        right_size = self._get_size(node.right)
        return max(left_size, right_size) > self.alpha * node.size
    
    def _flatten_to_list(self, node: Optional[ScapegoatNode], nodes: List[ScapegoatNode]) -> None:
        """将子树展平为有序列表"""
        if not node:
            return
        self._flatten_to_list(node.left, nodes)
        nodes.append(node)
        self._flatten_to_list(node.right, nodes)
    
    def _build_balanced_tree(self, nodes: List[ScapegoatNode], start: int, end: int) -> Optional[ScapegoatNode]:
        """从有序列表构建平衡树"""
        if start > end:
            return None
        
        mid = (start + end) // 2
        node = nodes[mid]
        node.left = self._build_balanced_tree(nodes, start, mid - 1)
        node.right = self._build_balanced_tree(nodes, mid + 1, end)
        self._update_size(node)
        self.steps.append((node.val, "重建节点"))
        return node
    
    def _rebuild(self, node: ScapegoatNode) -> ScapegoatNode:
        """重建以node为根的子树"""
        nodes = []
        self._flatten_to_list(node, nodes)
        return self._build_balanced_tree(nodes, 0, len(nodes) - 1)
    
    def insert(self, val: int) -> None:
        """插入新值"""
        def _insert(node: Optional[ScapegoatNode], val: int, depth: int) -> tuple:
            if not node:
                self.steps.append((val, "创建新节点"))
                return ScapegoatNode(val), None
            
            if val < node.val:
                new_node, scapegoat = _insert(node.left, val, depth + 1)
                node.left = new_node
            else:
                new_node, scapegoat = _insert(node.right, val, depth + 1)
                node.right = new_node
            
            self._update_size(node)
            
            # 检查是否需要重建
            if not scapegoat and depth > log2(self.size) / log2(1/self.alpha):
                if self._is_unbalanced(node):
                    self.steps.append((node.val, "找到替罪羊节点"))
                    return node, node
            
            return node, scapegoat
        
        self.size += 1
        self.max_size = max(self.max_size, self.size)
        
        if not self.root:
            self.root = ScapegoatNode(val)
            self.steps.append((val, "创建根节点"))
            return
        
        new_root, scapegoat = _insert(self.root, val, 0)
        self.root = new_root
        
        if scapegoat:
            self.root = self._rebuild(self.root)
            self.steps.append(("完成重建"))
    
    def delete(self, val: int) -> None:
        """删除值"""
        def _find_min(node: ScapegoatNode) -> ScapegoatNode:
            current = node
            while current.left:
                current = current.left
            return current
        
        def _delete(node: Optional[ScapegoatNode], val: int) -> Optional[ScapegoatNode]:
            if not node:
                return None
            
            if val < node.val:
                node.left = _delete(node.left, val)
            elif val > node.val:
                node.right = _delete(node.right, val)
            else:
                self.steps.append((val, "删除节点"))
                if not node.left:
                    return node.right
                elif not node.right:
                    return node.left
                else:
                    successor = _find_min(node.right)
                    node.val = successor.val
                    node.right = _delete(node.right, successor.val)
            
            self._update_size(node)
            return node
        
        self.root = _delete(self.root, val)
        self.size -= 1
        
        # 如果树太稀疏，整体重建
        if self.size < self.alpha * self.max_size:
            self.root = self._rebuild(self.root)
            self.max_size = self.size
            self.steps.append(("重建整棵树"))

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if isinstance(step, tuple):
            val, operation = step
            if operation == "创建新节点":
                print(f"{operation}：值 {val}")
            elif operation == "创建根节点":
                print(f"{operation}：值 {val}")
            elif operation == "找到替罪羊节点":
                print(f"{operation}：值 {val}")
            elif operation == "重建节点":
                print(f"{operation}：值 {val}")
            elif operation == "删除节点":
                print(f"{operation}：值 {val}")
        else:
            print(step)

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
        # 创建替罪羊树
        tree = ScapegoatTree()
        
        # 获取输入数字并插入
        numbers = get_input_numbers()
        if not numbers:
            raise ValueError("至少需要输入一个数字！")
        
        print("\n插入的数字：", numbers)
        for num in numbers:
            tree.insert(num)
        
        while True:
            print("\n请选择操作：")
            print("1. 插入数字")
            print("2. 删除数字")
            print("3. 退出")
            
            choice = input("请输入选择（1-3）：")
            
            if choice == '1':
                try:
                    num = int(input("请输入要插入的数字："))
                    tree.insert(num)
                    print("插入成功！")
                except ValueError:
                    print("请输入有效的整数！")
            
            elif choice == '2':
                try:
                    num = int(input("请输入要删除的数字："))
                    tree.delete(num)
                    print("删除成功！")
                except ValueError:
                    print("请输入有效的整数！")
            
            elif choice == '3':
                break
            
            else:
                print("无效的选择！")
        
        # 打印操作过程
        print_operations(tree.steps)
        
    except ValueError as e:
        print(f"错误：{str(e)}") 