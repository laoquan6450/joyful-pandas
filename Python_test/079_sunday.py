#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现Sunday字符串匹配算法。

程序分析：
1. 实现移动表构建
2. 实现字符串匹配
3. 支持多模式串匹配
4. 优化匹配过程
"""

from typing import List, Dict, Set
from collections import defaultdict

class Sunday:
    def __init__(self):
        self.steps = []  # 记录操作步骤
    
    def _build_shift_table(self, pattern: str) -> Dict[str, int]:
        """构建移动表"""
        n = len(pattern)
        shift_table = defaultdict(lambda: n + 1)  # 默认移动长度为模式串长度+1
        
        # 计算每个字符最右出现的位置到末尾的距离
        for i in range(n):
            shift_table[pattern[i]] = n - i
            self.steps.append((pattern[i], n-i, "设置移动距离"))
        
        return shift_table
    
    def search(self, text: str, pattern: str) -> List[int]:
        """在文本中搜索模式串，返回所有匹配位置"""
        if not pattern or not text:
            return []
        
        shift_table = self._build_shift_table(pattern)
        positions = []
        n, m = len(text), len(pattern)
        i = 0  # 文本指针
        
        while i <= n - m:
            # 尝试匹配当前位置
            matched = True
            for j in range(m):
                self.steps.append((i+j, j, "比较字符"))
                if text[i + j] != pattern[j]:
                    matched = False
                    break
            
            if matched:
                positions.append(i)
                self.steps.append((i, "找到匹配"))
            
            # 计算下一个可能的匹配位置
            next_pos = i + m
            if next_pos >= n:
                break
            
            # 根据下一个字符计算移动距离
            shift = shift_table[text[next_pos]]
            i += shift
            self.steps.append((shift, "移动距离"))
        
        return positions
    
    def multi_pattern_search(self, text: str, patterns: List[str]) -> Dict[str, List[int]]:
        """多模式串匹配"""
        result = {}
        for pattern in patterns:
            positions = self.search(text, pattern)
            if positions:
                result[pattern] = positions
                self.steps.append((pattern, len(positions), "模式串匹配结果"))
        return result
    
    def optimize_search(self, text: str, pattern: str) -> List[int]:
        """优化的Sunday搜索算法"""
        if not pattern or not text:
            return []
        
        shift_table = self._build_shift_table(pattern)
        positions = []
        n, m = len(text), len(pattern)
        i = 0
        
        # 使用坏字符规则和好后缀规则的组合
        while i <= n - m:
            j = m - 1
            k = i + m - 1
            
            # 从右向左匹配
            while j >= 0 and text[k] == pattern[j]:
                self.steps.append((k, j, "从右向左比较"))
                j -= 1
                k -= 1
            
            if j < 0:
                positions.append(i)
                self.steps.append((i, "找到匹配"))
                i += 1
            else:
                # 使用Sunday算法的移动规则
                next_pos = i + m
                if next_pos >= n:
                    break
                
                shift = shift_table[text[next_pos]]
                i += shift
                self.steps.append((shift, "优化移动"))
        
        return positions

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if len(step) == 2:
            val, operation = step
            if operation == "找到匹配":
                print(f"{operation}：位置 {val}")
            elif operation == "移动距离" or operation == "优化移动":
                print(f"{operation}：{val}")
            elif isinstance(val, str):  # 模式串匹配结果
                print(f"{operation}：'{val}' 找到 {step[1]} 处匹配")
        elif len(step) == 3:
            char, dist, operation = step
            if operation == "设置移动距离":
                print(f"{operation}：字符 '{char}' 距离 {dist}")
            else:  # 比较字符或从右向左比较
                print(f"{operation}：文本位置 {char}，模式串位置 {dist}")

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
        # 创建Sunday对象
        sunday = Sunday()
        
        # 获取输入文本
        text = input("请输入文本：").strip()
        if not text:
            raise ValueError("文本不能为空！")
        
        while True:
            print("\n请选择操作：")
            print("1. 单模式串匹配")
            print("2. 多模式串匹配")
            print("3. 优化匹配")
            print("4. 退出")
            
            choice = input("请输入选择（1-4）：")
            
            if choice == '1':
                pattern = input("请输入要搜索的模式串：").strip()
                if pattern:
                    positions = sunday.search(text, pattern)
                    if positions:
                        print("\n找到的匹配位置：")
                        for pos in positions:
                            print(f"位置 {pos}")
                    else:
                        print("未找到匹配！")
                else:
                    print("模式串不能为空！")
            
            elif choice == '2':
                patterns = get_input_patterns()
                if patterns:
                    results = sunday.multi_pattern_search(text, patterns)
                    if results:
                        print("\n匹配结果：")
                        for pattern, positions in results.items():
                            print(f"\n模式串 '{pattern}' 的匹配位置：")
                            for pos in positions:
                                print(f"位置 {pos}")
                    else:
                        print("未找到任何匹配！")
                else:
                    print("至少需要输入一个模式串！")
            
            elif choice == '3':
                pattern = input("请输入要搜索的模式串：").strip()
                if pattern:
                    positions = sunday.optimize_search(text, pattern)
                    if positions:
                        print("\n找到的匹配位置：")
                        for pos in positions:
                            print(f"位置 {pos}")
                    else:
                        print("未找到匹配！")
                else:
                    print("模式串不能为空！")
            
            elif choice == '4':
                break
            
            else:
                print("无效的选择！")
        
        # 打印操作过程
        print_operations(sunday.steps)
        
    except ValueError as e:
        print(f"错误：{str(e)}") 