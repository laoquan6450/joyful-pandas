#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现线段树及其基本操作。

程序分析：
1. 实现线段树的节点结构
2. 实现区间查询和更新操作
3. 实现懒惰传播
4. 处理区间最值和区间和问题
"""

class SegmentTreeNode:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.sum = 0
        self.min = float('inf')
        self.max = float('-inf')
        self.left = None
        self.right = None
        self.lazy = 0  # 懒惰标记

class SegmentTree:
    def __init__(self, arr):
        self.arr = arr
        self.root = self._build(0, len(arr)-1)
        self.steps = []  # 记录操作步骤
    
    def _build(self, start, end):
        """构建线段树"""
        if start > end:
            return None
            
        node = SegmentTreeNode(start, end)
        if start == end:
            node.sum = self.arr[start]
            node.min = self.arr[start]
            node.max = self.arr[start]
            self.steps.append((start, "创建叶节点"))
            return node
        
        mid = (start + end) // 2
        node.left = self._build(start, mid)
        node.right = self._build(mid+1, end)
        node.sum = node.left.sum + node.right.sum
        node.min = min(node.left.min, node.right.min)
        node.max = max(node.left.max, node.right.max)
        self.steps.append((start, end, "合并节点"))
        return node

    # ... [实现查询和更新操作]

# ... [其余代码包括测试和应用功能] 