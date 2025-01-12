#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现红黑树及其基本操作。

程序分析：
1. 实现红黑树的节点结构
2. 实现插入、删除操作
3. 实现颜色调整和旋转
4. 保持红黑树的5个性质
"""

class RBNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None
        self.color = 'RED'  # 新节点默认为红色

class RedBlackTree:
    def __init__(self):
        self.nil = RBNode(None)
        self.nil.color = 'BLACK'
        self.root = self.nil
        self.steps = []  # 记录操作步骤
    
    # ... [实现插入、删除、旋转等操作]

# ... [其余代码包括测试和可视化函数] 