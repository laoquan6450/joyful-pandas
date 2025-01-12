#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现B树及其基本操作。

程序分析：
1. 实现B树的节点结构
2. 实现插入、删除操作
3. 实现节点分裂和合并
4. 维护B树的性质
"""

class BTreeNode:
    def __init__(self, leaf=True):
        self.leaf = leaf
        self.keys = []
        self.children = []
        self.n = 0  # 当前关键字数量

class BTree:
    def __init__(self, t):
        self.root = BTreeNode()
        self.t = t  # 最小度数
        self.steps = []  # 记录操作步骤
    
    def search(self, k):
        """在B树中搜索关键字k"""
        return self._search(self.root, k)
    
    def _search(self, x, k):
        i = 0
        while i < x.n and k > x.keys[i]:
            i += 1
        if i < x.n and k == x.keys[i]:
            self.steps.append((x, i, "找到关键字"))
            return (x, i)
        if x.leaf:
            self.steps.append((x, -1, "未找到关键字"))
            return None
        self.steps.append((x, i, "继续搜索子节点"))
        return self._search(x.children[i], k)

    # ... [实现插入、删除等操作]

# ... [其余代码包括测试和可视化函数] 