#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现Horspool字符串匹配算法。

程序分析：
1. 实现移动表构建
2. 实现字符串匹配
3. 支持多模式串匹配
4. 优化匹配过程
"""

from typing import List, Dict, Set
from collections import defaultdict

class Horspool:
    def __init__(self):
        self.steps = []  # 记录操作步骤
    
    def _build_shift_table(self, pattern: str) -> Dict[str, int]:
        """构建移动表"""
        m = len(pattern)
        shift_table = defaultdict(lambda: m)  # 默认移动长度为模式串长度
        
        # 计算每个字符的移动距离（除最后一个字符外）
        for i in range(m - 1):
            shift_table[pattern[i]] = m - 1 - i
            self.steps.append((pattern[i], m-1-i, "设置移动距离"))
        
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
            j = m - 1  # 从右向左匹配
            k = i + m - 1
            matched = True
            
            # 尝试匹配
            while j >= 0:
                self.steps.append((k, j, "比较字符"))
                if text[k] != pattern[j]:
                    matched = False
                    break
                j -= 1
                k -= 1
            
            if matched:
                positions.append(i)
                self.steps.append((i, "找到匹配"))
            
            # 根据最右字符计算移动距离
            shift = shift_table[text[i + m - 1]]
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
        """优化的Horspool搜索算法"""
        if not pattern or not text:
            return []
        
        shift_table = self._build_shift_table(pattern)
        positions = []
        n, m = len(text), len(pattern)
        i = 0
        
        # 使用Boyer-Moore-Horspool优化
        while i <= n - m:
            j = m - 1
            k = i + m - 1
            matched = True
            
            # 从右向左匹配，但先检查最后一个字符
            if text[k] != pattern[j]:
                shift = shift_table[text[k]]
                i += shift
                self.steps.append((shift, "快速移动"))
                continue
            
            # 检查其余字符
            j -= 1
            k -= 1
            while j >= 0:
                self.steps.append((k, j, "优化比较"))
                if text[k] != pattern[j]:
                    matched = False
                    break
                j -= 1
                k -= 1
            
            if matched:
                positions.append(i)
                self.steps.append((i, "找到匹配"))
            
            # 使用Horspool移动规则
            shift = shift_table[text[i + m - 1]]
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
            elif operation in ["移动距离", "快速移动", "优化移动"]:
                print(f"{operation}：{val}")
            elif isinstance(val, str):  # 模式串匹配结果
                print(f"{operation}：'{val}' 找到 {step[1]} 处匹配")
        elif len(step) == 3:
            val1, val2, operation = step
            if operation == "设置移动距离":
                print(f"{operation}：字符 '{val1}' 距离 {val2}")
            else:  # 比较字符或优化比较
                print(f"{operation}：文本位置 {val1}，模式串位置 {val2}")

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
        # 创建Horspool对象
        horspool = Horspool()
        
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
                    positions = horspool.search(text, pattern)
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
                    results = horspool.multi_pattern_search(text, patterns)
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
                    positions = horspool.optimize_search(text, pattern)
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
        print_operations(horspool.steps)
        
    except ValueError as e:
        print(f"错误：{str(e)}") 