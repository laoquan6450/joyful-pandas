#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现AC自动机（Aho-Corasick Automaton）及其基本操作。

程序分析：
1. 实现Trie树的基本结构
2. 实现失败指针构建
3. 实现多模式串匹配
4. 优化匹配过程
"""

from collections import deque
from typing import List, Dict, Set, Tuple

class ACNode:
    def __init__(self):
        self.children = {}  # 子节点字典
        self.fail = None    # 失败指针
        self.is_end = False # 是否是单词结尾
        self.word = None    # 存储完整单词
        self.length = 0     # 单词长度

class ACAutomaton:
    def __init__(self):
        self.root = ACNode()
        self.steps = []  # 记录操作步骤
    
    def insert(self, word: str) -> None:
        """插入模式串"""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = ACNode()
                self.steps.append((char, "创建新节点"))
            node = node.children[char]
            self.steps.append((char, "移动到下一节点"))
        node.is_end = True
        node.word = word
        node.length = len(word)
        self.steps.append((word, "标记单词结束"))
    
    def build_fail(self) -> None:
        """构建失败指针"""
        queue = deque()
        # 将第一层节点的失败指针指向根节点
        for child in self.root.children.values():
            child.fail = self.root
            queue.append(child)
            self.steps.append(("设置第一层失败指针"))
        
        # BFS构建其他节点的失败指针
        while queue:
            current = queue.popleft()
            for char, child in current.children.items():
                fail = current.fail
                while fail and char not in fail.children:
                    fail = fail.fail
                child.fail = fail.children[char] if fail and char in fail.children else self.root
                queue.append(child)
                self.steps.append((char, "构建失败指针"))
    
    def search(self, text: str) -> List[Tuple[str, int]]:
        """在文本中搜索所有模式串"""
        results = []
        current = self.root
        
        for i, char in enumerate(text):
            while current != self.root and char not in current.children:
                current = current.fail
                self.steps.append((char, i, "跳转失败指针"))
            
            if char in current.children:
                current = current.children[char]
                self.steps.append((char, i, "移动到下一节点"))
            
            temp = current
            while temp != self.root:
                if temp.is_end:
                    pos = i - temp.length + 1
                    results.append((temp.word, pos))
                    self.steps.append((temp.word, pos, "找到匹配"))
                temp = temp.fail
        
        return results

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if len(step) == 2:
            char, operation = step
            if operation == "创建新节点":
                print(f"{operation}：字符 '{char}'")
            elif operation == "移动到下一节点":
                print(f"{operation}：字符 '{char}'")
            elif operation == "标记单词结束":
                print(f"{operation}：单词 '{char}'")
            else:
                print(f"{operation}")
        else:
            char, pos, operation = step
            if operation == "跳转失败指针":
                print(f"{operation}：字符 '{char}' 在位置 {pos}")
            elif operation == "移动到下一节点":
                print(f"{operation}：字符 '{char}' 在位置 {pos}")
            else:  # 找到匹配
                print(f"{operation}：单词 '{char}' 在位置 {pos}")

def get_input_patterns():
    """获取用户输入的模式串"""
    patterns = []
    print("请输入3个不同的模式串（仅包含小写字母）：")
    while len(patterns) < 3:
        try:
            pattern = input(f"请输入第{len(patterns)+1}个模式串：").strip().lower()
            if not pattern.isalpha():
                print("请只输入字母！")
                continue
            if pattern in patterns:
                print("该模式串已存在，请输入不同的模式串！")
                continue
            patterns.append(pattern)
        except ValueError:
            print("输入无效！")
    return patterns

if __name__ == '__main__':
    try:
        # 创建AC自动机
        ac = ACAutomaton()
        
        # 获取输入模式串并构建自动机
        patterns = get_input_patterns()
        print(f"\n模式串：{patterns}")
        for pattern in patterns:
            ac.insert(pattern)
        
        # 构建失败指针
        ac.build_fail()
        
        # 获取待匹配文本
        text = input("\n请输入要匹配的文本：").strip().lower()
        if not text.isalpha():
            raise ValueError("文本只能包含字母！")
        
        # 执行匹配
        matches = ac.search(text)
        
        # 输出结果
        if matches:
            print("\n匹配结果：")
            for pattern, pos in matches:
                print(f"在位置 {pos} 找到模式串 '{pattern}'")
        else:
            print("\n未找到任何匹配！")
        
        # 打印操作过程
        print_operations(ac.steps)
        
    except ValueError as e:
        print(f"错误：{str(e)}") 