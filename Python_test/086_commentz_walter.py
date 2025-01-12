#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现Commentz-Walter多模式串匹配算法。

程序分析：
1. 实现反向Trie树
2. 实现移动函数
3. 实现模式串匹配
4. 优化匹配过程
"""

from typing import List, Dict, Set, Optional
from collections import defaultdict

class TrieNode:
    def __init__(self):
        self.children = {}  # 子节点字典
        self.is_end = False  # 是否为单词结尾
        self.pattern = None  # 存储完整的模式串
        self.suffix_link = None  # 后缀链接

class CommentzWalter:
    def __init__(self):
        self.root = TrieNode()  # 反向Trie树根节点
        self.min_length = float('inf')  # 最短模式串长度
        self.steps = []  # 记录操作步骤
    
    def _build_trie(self, patterns: List[str]) -> None:
        """构建反向Trie树"""
        for pattern in patterns:
            self.min_length = min(self.min_length, len(pattern))
            node = self.root
            # 从后向前插入字符
            for c in reversed(pattern):
                if c not in node.children:
                    node.children[c] = TrieNode()
                    self.steps.append((c, "创建节点"))
                node = node.children[c]
            node.is_end = True
            node.pattern = pattern
            self.steps.append((pattern, "标记模式串"))
    
    def _build_suffix_links(self) -> None:
        """构建后缀链接"""
        queue = []
        # 初始化第一层节点的后缀链接
        for char, node in self.root.children.items():
            node.suffix_link = self.root
            queue.append(node)
            self.steps.append((char, "设置后缀链接"))
        
        # 广度优先搜索构建其他节点的后缀链接
        while queue:
            current = queue.popleft()
            for char, child in current.children.items():
                queue.append(child)
                suffix = current.suffix_link
                
                while suffix and char not in suffix.children:
                    suffix = suffix.suffix_link
                
                child.suffix_link = suffix.children[char] if suffix else self.root
                self.steps.append((char, "更新后缀链接"))
    
    def _build_shift_table(self, patterns: List[str]) -> Dict[str, int]:
        """构建移动表"""
        shift = defaultdict(lambda: self.min_length)
        
        for pattern in patterns:
            n = len(pattern)
            for i, c in enumerate(pattern):
                shift[c] = min(shift[c], n - i - 1)
                self.steps.append((c, shift[c], "设置移动距离"))
        
        return shift
    
    def search(self, text: str, patterns: List[str]) -> Dict[str, List[int]]:
        """在文本中搜索多个模式串"""
        if not patterns or not text:
            return {}
        
        # 构建数据结构
        self._build_trie(patterns)
        self._build_suffix_links()
        shift = self._build_shift_table(patterns)
        
        result = defaultdict(list)
        n = len(text)
        pos = self.min_length - 1
        
        while pos < n:
            # 从当前位置开始反向匹配
            node = self.root
            j = 0
            current_pos = pos
            
            while current_pos >= 0 and node:
                c = text[current_pos]
                self.steps.append((current_pos, c, "检查字符"))
                
                if c in node.children:
                    node = node.children[c]
                    if node.is_end:
                        pattern = node.pattern
                        start = current_pos - len(pattern) + 1
                        if text[start:start + len(pattern)] == pattern:
                            result[pattern].append(start)
                            self.steps.append((pattern, start, "找到匹配"))
                    current_pos -= 1
                    j += 1
                else:
                    break
            
            # 计算移动距离
            if j == 0:
                pos += shift[text[pos]]
                self.steps.append((shift[text[pos]], "移动距离"))
            else:
                pos += max(1, j - shift[text[pos]])
                self.steps.append((max(1, j - shift[text[pos]]), "优化移动"))
        
        return dict(result)

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if len(step) == 2:
            val, operation = step
            if operation == "创建节点":
                print(f"{operation}：字符 '{val}'")
            elif operation == "标记模式串":
                print(f"{operation}：'{val}'")
            elif operation == "设置后缀链接":
                print(f"{operation}：字符 '{val}'")
            elif operation == "更新后缀链接":
                print(f"{operation}：字符 '{val}'")
            elif operation in ["移动距离", "优化移动"]:
                print(f"{operation}：{val}")
        elif len(step) == 3:
            if step[2] == "设置移动距离":
                char, dist, _ = step
                print(f"设置移动距离：字符 '{char}' -> {dist}")
            elif step[2] == "检查字符":
                pos, char, _ = step
                print(f"检查字符：位置 {pos} 字符 '{char}'")
            elif step[2] == "找到匹配":
                pattern, pos, _ = step
                print(f"找到匹配：模式串 '{pattern}' 位置 {pos}")

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
        # 创建Commentz-Walter对象
        cw = CommentzWalter()
        
        # 获取输入文本
        text = input("请输入文本：").strip()
        if not text:
            raise ValueError("文本不能为空！")
        
        # 获取模式串
        patterns = get_input_patterns()
        if not patterns:
            raise ValueError("至少需要输入一个模式串！")
        
        # 执行搜索
        results = cw.search(text, patterns)
        
        # 输出结果
        if results:
            print("\n匹配结果：")
            for pattern, positions in results.items():
                print(f"\n模式串 '{pattern}' 的匹配位置：")
                for pos in positions:
                    print(f"位置 {pos}")
        else:
            print("未找到任何匹配！")
        
        # 打印操作过程
        print_operations(cw.steps)
        
    except ValueError as e:
        print(f"错误：{str(e)}") 