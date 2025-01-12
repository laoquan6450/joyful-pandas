#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现后缀树（Suffix Tree）及其基本操作。

程序分析：
1. 实现后缀树的基本结构
2. 实现Ukkonen算法构建
3. 实现字符串匹配功能
4. 支持最长公共子串查找
"""

from typing import List, Dict, Optional, Set, Tuple
from collections import defaultdict

class SuffixNode:
    def __init__(self, start: int, end: Optional[int] = None):
        self.start = start      # 边的起始位置
        self.end = end          # 边的结束位置
        self.children = {}      # 子节点字典
        self.suffix_link = None # 后缀链接
        self.id = -1           # 叶节点编号

class SuffixTree:
    def __init__(self, text: str):
        self.text = text + "$"  # 添加终止符
        self.root = SuffixNode(-1, -1)
        self.active_node = self.root
        self.active_edge = -1
        self.active_length = 0
        self.remainder = 0
        self.current_end = [-1]  # 使用列表以便共享引用
        self.current_node = 0
        self.steps = []  # 记录操作步骤
        self._build()
    
    def _edge_length(self, node: SuffixNode) -> int:
        """计算边的长度"""
        if node.end is None:
            return self.current_end[0] - node.start + 1
        return node.end - node.start + 1
    
    def _walk_down(self, node: SuffixNode) -> bool:
        """检查是否需要向下移动活动点"""
        if self.active_length >= self._edge_length(node):
            self.active_edge += self._edge_length(node)
            self.active_length -= self._edge_length(node)
            self.active_node = node
            return True
        return False
    
    def _build(self) -> None:
        """使用Ukkonen算法构建后缀树"""
        self.current_end[0] = -1
        
        for i in range(len(self.text)):
            self.current_end[0] = i
            self.remainder += 1
            last_created_node = None
            
            while self.remainder > 0:
                if self.active_length == 0:
                    self.active_edge = i
                
                if self.text[self.active_edge] not in self.active_node.children:
                    # 创建新叶节点
                    leaf = SuffixNode(i, None)
                    leaf.id = self.current_node
                    self.current_node += 1
                    self.active_node.children[self.text[self.active_edge]] = leaf
                    self.steps.append((i, "创建叶节点"))
                    
                    # 处理后缀链接
                    if last_created_node is not None:
                        last_created_node.suffix_link = self.active_node
                        self.steps.append(("设置后缀链接"))
                    last_created_node = None
                
                else:
                    next_node = self.active_node.children[self.text[self.active_edge]]
                    
                    if self._walk_down(next_node):
                        continue
                    
                    if self.text[next_node.start + self.active_length] == self.text[i]:
                        # 当前字符已存在于树中
                        self.active_length += 1
                        self.steps.append((i, "增加活动长度"))
                        
                        if last_created_node is not None:
                            last_created_node.suffix_link = self.active_node
                            self.steps.append(("设置后缀链接"))
                        break
                    
                    # 需要分裂边
                    split = SuffixNode(next_node.start, next_node.start + self.active_length - 1)
                    self.active_node.children[self.text[self.active_edge]] = split
                    
                    leaf = SuffixNode(i, None)
                    leaf.id = self.current_node
                    self.current_node += 1
                    split.children[self.text[i]] = leaf
                    
                    next_node.start += self.active_length
                    split.children[self.text[next_node.start]] = next_node
                    
                    self.steps.append((i, "分裂边"))
                    
                    if last_created_node is not None:
                        last_created_node.suffix_link = split
                    last_created_node = split
                
                self.remainder -= 1
                if self.active_node == self.root and self.active_length > 0:
                    self.active_length -= 1
                    self.active_edge = i - self.remainder + 1
                else:
                    self.active_node = self.active_node.suffix_link or self.root
    
    def search(self, pattern: str) -> bool:
        """在后缀树中搜索模式串"""
        if not pattern:
            return False
        
        node = self.root
        i = 0
        
        while i < len(pattern):
            if pattern[i] not in node.children:
                self.steps.append((pattern[i], "未找到字符"))
                return False
            
            current = node.children[pattern[i]]
            j = 0
            
            while j < self._edge_length(current) and i < len(pattern):
                if pattern[i] != self.text[current.start + j]:
                    self.steps.append((pattern[i], "字符不匹配"))
                    return False
                i += 1
                j += 1
            
            if j == self._edge_length(current):
                node = current
                self.steps.append((pattern[:i], "匹配边"))
            
        self.steps.append((pattern, "找到模式串"))
        return True
    
    def find_longest_common_substring(self, other: str) -> str:
        """查找最长公共子串"""
        # 构建第二个字符串的后缀树
        other_tree = SuffixTree(other)
        
        def _traverse(node1: SuffixNode, node2: SuffixNode, length: int, max_length: List[int], result: List[str]):
            """遍历两棵树查找最长公共子串"""
            if length > max_length[0]:
                max_length[0] = length
                result[0] = self.text[node1.start:node1.start + length]
                self.steps.append((result[0], "更新最长公共子串"))
            
            for c in node1.children:
                if c in node2.children:
                    child1 = node1.children[c]
                    child2 = node2.children[c]
                    edge_length = min(self._edge_length(child1), self._edge_length(child2))
                    _traverse(child1, child2, length + edge_length, max_length, result)
        
        max_length = [0]
        result = [""]
        _traverse(self.root, other_tree.root, 0, max_length, result)
        return result[0]

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if len(step) == 1:
            print(step[0])
        else:
            val, operation = step
            if operation == "创建叶节点":
                print(f"{operation}：位置 {val}")
            elif operation == "增加活动长度":
                print(f"{operation}：位置 {val}")
            elif operation == "分裂边":
                print(f"{operation}：位置 {val}")
            elif operation == "未找到字符":
                print(f"{operation}：'{val}'")
            elif operation == "字符不匹配":
                print(f"{operation}：'{val}'")
            elif operation == "匹配边":
                print(f"{operation}：'{val}'")
            elif operation == "找到模式串":
                print(f"{operation}：'{val}'")
            elif operation == "更新最长公共子串":
                print(f"{operation}：'{val}'")

if __name__ == '__main__':
    try:
        # 获取输入文本
        text = input("请输入文本：").strip()
        if not text:
            raise ValueError("文本不能为空！")
        
        # 创建后缀树
        suffix_tree = SuffixTree(text)
        
        while True:
            print("\n请选择操作：")
            print("1. 搜索模式串")
            print("2. 查找最长公共子串")
            print("3. 退出")
            
            choice = input("请输入选择（1-3）：")
            
            if choice == '1':
                pattern = input("请输入要搜索的模式串：").strip()
                if pattern:
                    if suffix_tree.search(pattern):
                        print(f"找到模式串 '{pattern}'！")
                    else:
                        print(f"未找到模式串 '{pattern}'！")
                else:
                    print("模式串不能为空！")
            
            elif choice == '2':
                other = input("请输入另一个字符串：").strip()
                if other:
                    result = suffix_tree.find_longest_common_substring(other)
                    if result:
                        print(f"最长公共子串为：'{result}'")
                    else:
                        print("没有找到公共子串！")
                else:
                    print("字符串不能为空！")
            
            elif choice == '3':
                break
            
            else:
                print("无效的选择！")
        
        # 打印操作过程
        print_operations(suffix_tree.steps)
        
    except ValueError as e:
        print(f"错误：{str(e)}") 