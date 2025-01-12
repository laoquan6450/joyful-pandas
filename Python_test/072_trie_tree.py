#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现字典树（Trie Tree）及其基本操作。

程序分析：
1. 实现字典树的基本结构
2. 实现字符串的插入和查找
3. 实现前缀匹配功能
4. 支持字符串删除操作
"""

from typing import List, Dict, Optional

class TrieNode:
    def __init__(self):
        self.children: Dict[str, TrieNode] = {}  # 子节点字典
        self.is_end = False    # 是否为单词结尾
        self.count = 0         # 经过该节点的单词数

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
            node.count += 1
            self.steps.append((char, "更新计数"))
        node.is_end = True
        self.steps.append((word, "标记单词结尾"))
    
    def search(self, word: str) -> bool:
        """查找单词"""
        node = self._find_node(word)
        if node and node.is_end:
            self.steps.append((word, "找到单词"))
            return True
        self.steps.append((word, "未找到单词"))
        return False
    
    def starts_with(self, prefix: str) -> bool:
        """查找前缀"""
        node = self._find_node(prefix)
        if node:
            self.steps.append((prefix, "找到前缀"))
            return True
        self.steps.append((prefix, "未找到前缀"))
        return False
    
    def _find_node(self, s: str) -> Optional[TrieNode]:
        """查找字符串对应的节点"""
        node = self.root
        for char in s:
            if char not in node.children:
                return None
            node = node.children[char]
            self.steps.append((char, "访问节点"))
        return node
    
    def delete(self, word: str) -> bool:
        """删除单词"""
        def _delete_helper(node: TrieNode, word: str, depth: int) -> bool:
            if depth == len(word):
                if not node.is_end:
                    return False
                node.is_end = False
                self.steps.append((word, "取消单词标记"))
                return len(node.children) == 0
            
            char = word[depth]
            if char not in node.children:
                return False
            
            should_delete_current = _delete_helper(node.children[char], word, depth + 1)
            
            if should_delete_current:
                self.steps.append((char, "删除节点"))
                del node.children[char]
                return len(node.children) == 0 and not node.is_end
            
            node.children[char].count -= 1
            self.steps.append((char, "更新计数"))
            return False
        
        if _delete_helper(self.root, word, 0):
            self.steps.append((word, "删除成功"))
            return True
        return False
    
    def get_words_with_prefix(self, prefix: str) -> List[str]:
        """获取所有指定前缀的单词"""
        result = []
        node = self._find_node(prefix)
        
        if not node:
            return result
        
        def _collect_words(node: TrieNode, current: str):
            if node.is_end:
                result.append(current)
                self.steps.append((current, "收集单词"))
            
            for char, child in node.children.items():
                _collect_words(child, current + char)
        
        _collect_words(node, prefix)
        return result

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        char, operation = step
        if operation == "创建新节点":
            print(f"{operation}：字符 '{char}'")
        elif operation == "更新计数":
            print(f"{operation}：字符 '{char}'")
        elif operation == "标记单词结尾":
            print(f"{operation}：单词 '{char}'")
        elif operation == "访问节点":
            print(f"{operation}：字符 '{char}'")
        elif operation == "找到单词":
            print(f"{operation}：'{char}'")
        elif operation == "未找到单词":
            print(f"{operation}：'{char}'")
        elif operation == "找到前缀":
            print(f"{operation}：'{char}'")
        elif operation == "未找到前缀":
            print(f"{operation}：'{char}'")
        elif operation == "取消单词标记":
            print(f"{operation}：'{char}'")
        elif operation == "删除节点":
            print(f"{operation}：字符 '{char}'")
        elif operation == "删除成功":
            print(f"{operation}：单词 '{char}'")
        elif operation == "收集单词":
            print(f"{operation}：'{char}'")

def get_input_words() -> List[str]:
    """获取用户输入的单词"""
    words = []
    print("请输入单词（每行一个，输入空行结束）：")
    while True:
        word = input().strip()
        if not word:
            break
        words.append(word)
    return words

if __name__ == '__main__':
    try:
        # 创建字典树
        trie = Trie()
        
        # 获取输入单词并插入
        words = get_input_words()
        if not words:
            raise ValueError("至少需要输入一个单词！")
        
        print("\n插入的单词：")
        for word in words:
            print(word)
            trie.insert(word)
        
        while True:
            print("\n请选择操作：")
            print("1. 插入单词")
            print("2. 查找单词")
            print("3. 查找前缀")
            print("4. 删除单词")
            print("5. 查找所有前缀匹配")
            print("6. 退出")
            
            choice = input("请输入选择（1-6）：")
            
            if choice == '1':
                word = input("请输入要插入的单词：").strip()
                if word:
                    trie.insert(word)
                    print("插入成功！")
                else:
                    print("单词不能为空！")
            
            elif choice == '2':
                word = input("请输入要查找的单词：").strip()
                if word:
                    if trie.search(word):
                        print("找到单词！")
                    else:
                        print("未找到单词！")
                else:
                    print("单词不能为空！")
            
            elif choice == '3':
                prefix = input("请输入要查找的前缀：").strip()
                if prefix:
                    if trie.starts_with(prefix):
                        print("找到前缀！")
                    else:
                        print("未找到前缀！")
                else:
                    print("前缀不能为空！")
            
            elif choice == '4':
                word = input("请输入要删除的单词：").strip()
                if word:
                    if trie.delete(word):
                        print("删除成功！")
                    else:
                        print("未找到单词！")
                else:
                    print("单词不能为空！")
            
            elif choice == '5':
                prefix = input("请输入要查找的前缀：").strip()
                if prefix:
                    matches = trie.get_words_with_prefix(prefix)
                    if matches:
                        print("\n找到的单词：")
                        for word in matches:
                            print(word)
                    else:
                        print("未找到匹配的单词！")
                else:
                    print("前缀不能为空！")
            
            elif choice == '6':
                break
            
            else:
                print("无效的选择！")
        
        # 打印操作过程
        print_operations(trie.steps)
        
    except ValueError as e:
        print(f"错误：{str(e)}") 