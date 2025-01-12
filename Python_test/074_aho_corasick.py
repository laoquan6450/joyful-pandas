#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现AC自动机（Aho-Corasick Automaton）及其基本操作。

程序分析：
1. 实现Trie树基础结构
2. 实现失配指针构建
3. 实现多模式串匹配
4. 支持模式串集合查询
"""

from typing import List, Dict, Set, Optional
from collections import deque

class ACNode:
    def __init__(self):
        self.children: Dict[str, ACNode] = {}  # 子节点字典
        self.fail = None        # 失配指针
        self.is_end = False     # 是否为模式串结尾
        self.pattern = None     # 存储完整的模式串
        self.pattern_set = set()  # 存储以此节点结尾的所有模式串

class AhoCorasick:
    def __init__(self):
        self.root = ACNode()
        self.steps = []  # 记录操作步骤
    
    def add_pattern(self, pattern: str) -> None:
        """添加模式串"""
        node = self.root
        for char in pattern:
            if char not in node.children:
                node.children[char] = ACNode()
                self.steps.append((char, "创建新节点"))
            node = node.children[char]
        node.is_end = True
        node.pattern = pattern
        node.pattern_set.add(pattern)
        self.steps.append((pattern, "标记模式串结尾"))
    
    def build_fail_pointers(self) -> None:
        """构建失配指针"""
        queue = deque()
        
        # 初始化第一层节点的失配指针
        for char, node in self.root.children.items():
            node.fail = self.root
            queue.append(node)
            self.steps.append((char, "设置第一层失配指针"))
        
        # 广度优先搜索构建其他节点的失配指针
        while queue:
            current = queue.popleft()
            
            for char, child in current.children.items():
                queue.append(child)
                fail = current.fail
                
                while fail and char not in fail.children:
                    fail = fail.fail
                
                child.fail = fail.children[char] if fail else self.root
                child.pattern_set.update(child.fail.pattern_set)
                self.steps.append((char, "设置失配指针"))
    
    def search(self, text: str) -> List[tuple]:
        """在文本中搜索所有模式串"""
        result = []
        node = self.root
        
        for i, char in enumerate(text):
            # 沿着失配指针回溯，直到找到匹配或到达根节点
            while node is not self.root and char not in node.children:
                node = node.fail
                self.steps.append((char, "失配回溯"))
            
            # 在当前节点尝试匹配
            if char in node.children:
                node = node.children[char]
                self.steps.append((char, "字符匹配"))
                
                # 检查是否找到完整的模式串
                if node.pattern_set:
                    for pattern in node.pattern_set:
                        result.append((i - len(pattern) + 1, pattern))
                        self.steps.append((pattern, "找到模式串"))
            else:
                node = self.root
        
        return sorted(result)  # 按位置排序
    
    def get_patterns_with_prefix(self, prefix: str) -> Set[str]:
        """获取所有具有指定前缀的模式串"""
        result = set()
        node = self._find_prefix_node(prefix)
        
        if node:
            self._collect_patterns(node, result)
            self.steps.append((prefix, "收集前缀匹配"))
        
        return result
    
    def _find_prefix_node(self, prefix: str) -> Optional[ACNode]:
        """查找前缀对应的节点"""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
            self.steps.append((char, "查找前缀"))
        return node
    
    def _collect_patterns(self, node: ACNode, result: Set[str]) -> None:
        """收集节点下的所有模式串"""
        if node.is_end:
            result.add(node.pattern)
            self.steps.append((node.pattern, "收集模式串"))
        
        for child in node.children.values():
            self._collect_patterns(child, result)

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        char, operation = step
        if operation == "创建新节点":
            print(f"{operation}：字符 '{char}'")
        elif operation == "标记模式串结尾":
            print(f"{operation}：'{char}'")
        elif operation == "设置第一层失配指针":
            print(f"{operation}：字符 '{char}'")
        elif operation == "设置失配指针":
            print(f"{operation}：字符 '{char}'")
        elif operation == "失配回溯":
            print(f"{operation}：字符 '{char}'")
        elif operation == "字符匹配":
            print(f"{operation}：'{char}'")
        elif operation == "找到模式串":
            print(f"{operation}：'{char}'")
        elif operation == "查找前缀":
            print(f"{operation}：字符 '{char}'")
        elif operation == "收集模式串":
            print(f"{operation}：'{char}'")
        elif operation == "收集前缀匹配":
            print(f"{operation}：前缀 '{char}'")

def get_input_patterns() -> List[str]:
    """获取用户输入的模式串"""
    patterns = []
    print("请输入模式串（每行一个，输入空行结束）：")
    while True:
        pattern = input().strip()
        if not pattern:
            break
        patterns.append(pattern)
    return patterns

if __name__ == '__main__':
    try:
        # 创建AC自动机
        ac = AhoCorasick()
        
        # 获取输入模式串并添加
        patterns = get_input_patterns()
        if not patterns:
            raise ValueError("至少需要输入一个模式串！")
        
        print("\n添加的模式串：")
        for pattern in patterns:
            print(pattern)
            ac.add_pattern(pattern)
        
        # 构建失配指针
        ac.build_fail_pointers()
        
        while True:
            print("\n请选择操作：")
            print("1. 添加模式串")
            print("2. 搜索文本")
            print("3. 查找前缀匹配")
            print("4. 退出")
            
            choice = input("请输入选择（1-4）：")
            
            if choice == '1':
                pattern = input("请输入要添加的模式串：").strip()
                if pattern:
                    ac.add_pattern(pattern)
                    ac.build_fail_pointers()  # 重新构建失配指针
                    print("添加成功！")
                else:
                    print("模式串不能为空！")
            
            elif choice == '2':
                text = input("请输入要搜索的文本：").strip()
                if text:
                    matches = ac.search(text)
                    if matches:
                        print("\n找到的匹配：")
                        for pos, pattern in matches:
                            print(f"位置 {pos}：'{pattern}'")
                    else:
                        print("未找到匹配！")
                else:
                    print("文本不能为空！")
            
            elif choice == '3':
                prefix = input("请输入要查找的前缀：").strip()
                if prefix:
                    matches = ac.get_patterns_with_prefix(prefix)
                    if matches:
                        print("\n找到的模式串：")
                        for pattern in sorted(matches):
                            print(pattern)
                    else:
                        print("未找到匹配的模式串！")
                else:
                    print("前缀不能为空！")
            
            elif choice == '4':
                break
            
            else:
                print("无效的选择！")
        
        # 打印操作过程
        print_operations(ac.steps)
        
    except ValueError as e:
        print(f"错误：{str(e)}") 