#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现字典树（Trie树）及其基本操作。

程序分析：
1. 实现Trie树的节点结构
2. 实现插入、查找操作
3. 实现前缀匹配功能
4. 实现单词统计功能
"""

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.count = 0  # 记录单词出现次数

class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.steps = []  # 记录操作步骤
    
    def insert(self, word: str) -> None:
        """插入单词"""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
                self.steps.append((char, "创建新节点"))
            node = node.children[char]
            self.steps.append((char, "移动到下一节点"))
        node.is_end = True
        node.count += 1
        self.steps.append((word, f"标记单词结束，出现次数：{node.count}"))

    # ... [实现查找、前缀匹配等操作]

# ... [其余代码包括测试和统计功能] 