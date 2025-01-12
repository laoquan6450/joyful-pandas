#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现回文树（Palindromic Tree）及其基本操作。

程序分析：
1. 实现回文树的基本结构
2. 实现回文子串的添加
3. 实现回文子串的查询
4. 支持最长回文子串查找
"""

from typing import List, Dict, Optional

class PalindromeNode:
    def __init__(self, start: int, length: int):
        self.start = start      # 回文串起始位置
        self.length = length    # 回文串长度
        self.next = {}          # 转移边字典
        self.suffix_link = None # 后缀链接
        self.count = 0          # 出现次数
        self.num = 0            # 不同回文后缀数量

class PalindromicTree:
    def __init__(self):
        # 创建两个初始节点：空串和虚拟根
        self.nodes = [PalindromeNode(0, -1), PalindromeNode(0, 0)]
        self.text = ""
        self.last = 1  # 上一个回文串的节点编号
        self.steps = []  # 记录操作步骤
    
    def _get_suffix_link(self, node_idx: int) -> int:
        """获取节点的后缀链接"""
        while True:
            cur_len = len(self.text) - 1
            while cur_len - self.nodes[node_idx].length - 1 >= 0 and \
                  self.text[cur_len - self.nodes[node_idx].length - 1] != self.text[cur_len]:
                node_idx = self.nodes[node_idx].suffix_link
            if cur_len - self.nodes[node_idx].length - 1 < 0:
                return 0
            if self.text[cur_len - self.nodes[node_idx].length - 1] == self.text[cur_len]:
                break
        return node_idx
    
    def add_char(self, c: str) -> None:
        """添加一个字符并更新回文树"""
        self.text += c
        pos = len(self.text) - 1
        cur = self.last
        
        # 查找可以扩展的回文串
        cur = self._get_suffix_link(cur)
        
        # 检查是否已存在该转移
        if c in self.nodes[cur].next:
            self.last = self.nodes[cur].next[c]
            self.nodes[self.last].count += 1
            self.steps.append((c, "更新已有回文串"))
            return
        
        # 创建新节点
        new_node = PalindromeNode(pos - self.nodes[cur].length - 1,
                                 self.nodes[cur].length + 2)
        self.nodes.append(new_node)
        new_idx = len(self.nodes) - 1
        self.nodes[cur].next[c] = new_idx
        
        # 设置后缀链接
        if new_node.length == 1:
            new_node.suffix_link = 1
            new_node.num = 1
        else:
            cur = self._get_suffix_link(self.nodes[cur].suffix_link)
            new_node.suffix_link = self.nodes[cur].next[c]
            new_node.num = self.nodes[new_node.suffix_link].num + 1
        
        new_node.count = 1
        self.last = new_idx
        self.steps.append((c, "创建新回文串"))
    
    def get_palindromes(self) -> List[str]:
        """获取所有回文子串"""
        result = []
        for node in self.nodes[2:]:  # 跳过两个初始节点
            if node.length > 0:
                palindrome = self.text[node.start:node.start + node.length]
                result.append((palindrome, node.count))
                self.steps.append((palindrome, "收集回文串"))
        return result
    
    def find_longest_palindrome(self) -> str:
        """查找最长回文子串"""
        max_len = 0
        result = ""
        
        for node in self.nodes[2:]:  # 跳过两个初始节点
            if node.length > max_len:
                max_len = node.length
                result = self.text[node.start:node.start + node.length]
                self.steps.append((result, "更新最长回文串"))
        
        return result
    
    def count_different_palindromes(self) -> int:
        """统计不同回文子串的数量"""
        count = 0
        for node in self.nodes[2:]:  # 跳过两个初始节点
            if node.length > 0:
                count += 1
        self.steps.append((count, "统计回文串数量"))
        return count

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        val, operation = step
        if operation == "创建新回文串":
            print(f"{operation}：添加字符 '{val}'")
        elif operation == "更新已有回文串":
            print(f"{operation}：字符 '{val}'")
        elif operation == "收集回文串":
            print(f"{operation}：'{val}'")
        elif operation == "更新最长回文串":
            print(f"{operation}：'{val}'")
        elif operation == "统计回文串数量":
            print(f"{operation}：{val}")

if __name__ == '__main__':
    try:
        # 创建回文树
        tree = PalindromicTree()
        
        # 获取输入文本
        text = input("请输入文本：").strip()
        if not text:
            raise ValueError("文本不能为空！")
        
        # 逐个添加字符
        print("\n添加字符：")
        for c in text:
            print(c, end=' ')
            tree.add_char(c)
        print()
        
        while True:
            print("\n请选择操作：")
            print("1. 查看所有回文子串")
            print("2. 查找最长回文子串")
            print("3. 统计不同回文子串数量")
            print("4. 退出")
            
            choice = input("请输入选择（1-4）：")
            
            if choice == '1':
                palindromes = tree.get_palindromes()
                if palindromes:
                    print("\n所有回文子串（及出现次数）：")
                    for palindrome, count in palindromes:
                        print(f"'{palindrome}': {count}次")
                else:
                    print("没有找到回文子串！")
            
            elif choice == '2':
                result = tree.find_longest_palindrome()
                if result:
                    print(f"\n最长回文子串为：'{result}'")
                else:
                    print("没有找到回文子串！")
            
            elif choice == '3':
                count = tree.count_different_palindromes()
                print(f"\n不同回文子串的数量为：{count}")
            
            elif choice == '4':
                break
            
            else:
                print("无效的选择！")
        
        # 打印操作过程
        print_operations(tree.steps)
        
    except ValueError as e:
        print(f"错误：{str(e)}")