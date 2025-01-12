#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现AVL树及其基本操作。

程序分析：
1. 实现AVL树的节点结构
2. 实现插入、删除操作
3. 实现树的平衡调整
4. 实现树的遍历和可视化
"""

class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None
        self.steps = []  # 记录操作步骤
    
    def height(self, node):
        if not node:
            return 0
        return node.height
    
    def balance_factor(self, node):
        if not node:
            return 0
        return self.height(node.left) - self.height(node.right)
    
    def update_height(self, node):
        if not node:
            return
        node.height = max(self.height(node.left), self.height(node.right)) + 1
    
    # ... [实现旋转、插入、删除等操作]

# ... [其余代码包括测试和可视化函数] 