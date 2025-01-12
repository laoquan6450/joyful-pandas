#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现KMP算法及其应用。

程序分析：
1. 实现next数组构建
2. 实现字符串匹配
3. 支持多模式串匹配
4. 实现循环节查找
"""

from typing import List, Dict, Set, Optional

class KMP:
    def __init__(self):
        self.steps = []  # 记录操作步骤
    
    def build_next(self, pattern: str) -> List[int]:
        """构建next数组"""
        n = len(pattern)
        next_array = [0] * n
        next_array[0] = -1
        
        k = -1  # 前缀末尾
        j = 0   # 后缀末尾
        
        while j < n - 1:
            if k == -1 or pattern[k] == pattern[j]:
                k += 1
                j += 1
                next_array[j] = k
                self.steps.append((j, k, "设置next值"))
            else:
                k = next_array[k]
                self.steps.append((k, "回退前缀"))
        
        return next_array
    
    def search(self, text: str, pattern: str) -> List[int]:
        """在文本中搜索模式串，返回所有匹配位置"""
        if not pattern or not text:
            return []
        
        next_array = self.build_next(pattern)
        positions = []
        
        i = 0  # 文本指针
        j = 0  # 模式串指针
        
        while i < len(text):
            if j == -1 or text[i] == pattern[j]:
                i += 1
                j += 1
                self.steps.append((i-1, j-1, "字符匹配"))
            else:
                j = next_array[j]
                self.steps.append((j, "模式串回退"))
            
            if j == len(pattern):
                positions.append(i - j)
                j = next_array[j-1]
                self.steps.append((i-j, "找到匹配"))
        
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
    
    def find_period(self, pattern: str) -> Optional[int]:
        """查找字符串的最小循环节长度"""
        next_array = self.build_next(pattern)
        n = len(pattern)
        
        if n == 0:
            return None
        
        # 如果字符串长度可以被(n - next_array[-1])整除，则存在循环节
        if next_array[-1] > 0 and n % (n - next_array[-1]) == 0:
            period = n - next_array[-1]
            self.steps.append((period, "找到循环节"))
            return period
        
        self.steps.append(("未找到循环节",))
        return None

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if len(step) == 1:
            print(step[0])
        elif len(step) == 2:
            if isinstance(step[0], str):
                pattern, count = step
                print(f"模式串匹配结果：'{pattern}' 找到 {count} 处匹配")
            elif isinstance(step[0], int):
                val, operation = step
                if operation == "回退前缀":
                    print(f"{operation}：位置 {val}")
                else:  # 找到循环节
                    print(f"{operation}：长度 {val}")
        else:  # len(step) == 3
            pos1, pos2, operation = step
            if operation == "设置next值":
                print(f"{operation}：位置 {pos1}，值 {pos2}")
            elif operation == "字符匹配":
                print(f"{operation}：文本位置 {pos1}，模式串位置 {pos2}")
            else:  # 找到匹配
                print(f"{operation}：位置 {pos1}")

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
        # 创建KMP对象
        kmp = KMP()
        
        # 获取输入文本
        text = input("请输入文本：").strip()
        if not text:
            raise ValueError("文本不能为空！")
        
        while True:
            print("\n请选择操作：")
            print("1. 单模式串匹配")
            print("2. 多模式串匹配")
            print("3. 查找循环节")
            print("4. 退出")
            
            choice = input("请输入选择（1-4）：")
            
            if choice == '1':
                pattern = input("请输入要搜索的模式串：").strip()
                if pattern:
                    positions = kmp.search(text, pattern)
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
                    results = kmp.multi_pattern_search(text, patterns)
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
                pattern = input("请输入要查找循环节的字符串：").strip()
                if pattern:
                    period = kmp.find_period(pattern)
                    if period:
                        print(f"\n找到最小循环节，长度为：{period}")
                        print(f"循环节为：'{pattern[:period]}'")
                    else:
                        print("该字符串没有循环节！")
                else:
                    print("字符串不能为空！")
            
            elif choice == '4':
                break
            
            else:
                print("无效的选择！")
        
        # 打印操作过程
        print_operations(kmp.steps)
        
    except ValueError as e:
        print(f"错误：{str(e)}") 