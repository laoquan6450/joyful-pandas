#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现后缀树及其基本操作。

程序分析：
1. 实现后缀树的节点结构
2. 实现Ukkonen算法构建后缀树
3. 实现字符串匹配功能
4. 实现最长公共子串查找
"""

class SuffixTreeNode:
    def __init__(self, start=None, end=None):
        self.children = {}
        self.start = start
        self.end = end
        self.suffix_link = None

class SuffixTree:
    def __init__(self, text):
        self.text = text + "$"  # 添加终止符
        self.root = SuffixTreeNode()
        self.steps = []  # 记录构建步骤
        self._build()
    
    def _build(self):
        """使用Ukkonen算法构建后缀树"""
        # ... [实现Ukkonen算法]
        pass

    # ... [实现查找、匹配等操作]

# ... [其余代码包括测试和应用功能] 