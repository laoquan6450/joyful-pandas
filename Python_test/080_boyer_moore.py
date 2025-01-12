#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现Boyer-Moore字符串匹配算法。

程序分析：
1. 实现坏字符规则
2. 实现好后缀规则
3. 实现字符串匹配
4. 优化匹配过程
"""

from typing import List, Dict, Optional

class BoyerMoore:
    def __init__(self):
        self.steps = []  # 记录操作步骤
    
    def _build_bad_char_table(self, pattern: str) -> Dict[str, int]:
        """构建坏字符规则表"""
        n = len(pattern)
        bad_char = {}
        
        # 记录每个字符最后出现的位置
        for i in range(n):
            bad_char[pattern[i]] = i
            self.steps.append((pattern[i], i, "设置坏字符位置"))
        
        return bad_char
    
    def _build_good_suffix_table(self, pattern: str) -> tuple:
        """构建好后缀规则表"""
        n = len(pattern)
        suffix = [0] * n
        prefix = [False] * n
        
        # 计算后缀数组
        for i in range(n - 1):
            j = i
            k = 0
            while j >= 0 and pattern[j] == pattern[n-1-k]:
                k += 1
                suffix[k] = j
                j -= 1
            if k > 0:
                self.steps.append((k, suffix[k], "设置后缀位置"))
        
        # 计算前缀数组
        for i in range(n):
            j = 0
            while j <= i and pattern[j] == pattern[n-1-i+j]:
                j += 1
            if j == i + 1:
                prefix[i+1] = True
                self.steps.append((i+1, "标记前缀"))
        
        return suffix, prefix
    
    def search(self, text: str, pattern: str) -> List[int]:
        """在文本中搜索模式串，返回所有匹配位置"""
        if not pattern or not text:
            return []
        
        # 构建规则表
        bad_char = self._build_bad_char_table(pattern)
        suffix, prefix = self._build_good_suffix_table(pattern)
        
        positions = []
        n, m = len(text), len(pattern)
        i = 0  # 文本指针
        
        while i <= n - m:
            j = m - 1  # 从右向左匹配
            k = i + m - 1
            
            # 尝试匹配
            while j >= 0 and text[k] == pattern[j]:
                self.steps.append((k, j, "字符匹配"))
                j -= 1
                k -= 1
            
            if j < 0:
                positions.append(i)
                self.steps.append((i, "找到匹配"))
                i += 1
            else:
                # 计算移动距离
                char_shift = j - bad_char.get(text[k], -1)
                suffix_shift = self._get_suffix_shift(j, suffix, prefix, m)
                shift = max(char_shift, suffix_shift)
                i += max(1, shift)
                self.steps.append((shift, "移动距离"))
        
        return positions
    
    def _get_suffix_shift(self, j: int, suffix: List[int], prefix: List[bool], m: int) -> int:
        """计算好后缀规则的移动距离"""
        k = m - 1 - j  # 好后缀长度
        
        if k > 0:
            if suffix[k] > -1:
                return j - suffix[k] + 1
            
            # 查找最长的可匹配前缀
            for r in range(j+2, m):
                if prefix[m-r]:
                    return r
        
        return m
    
    def optimize_search(self, text: str, pattern: str) -> List[int]:
        """优化的Boyer-Moore搜索算法"""
        if not pattern or not text:
            return []
        
        # 构建规则表
        bad_char = self._build_bad_char_table(pattern)
        suffix, prefix = self._build_good_suffix_table(pattern)
        
        positions = []
        n, m = len(text), len(pattern)
        i = 0
        
        # 使用Turbo Boyer-Moore优化
        while i <= n - m:
            j = m - 1
            k = i + m - 1
            last_mismatch = -1
            
            while j >= 0 and text[k] == pattern[j]:
                if last_mismatch >= 0:
                    self.steps.append((k, j, "Turbo匹配"))
                else:
                    self.steps.append((k, j, "常规匹配"))
                j -= 1
                k -= 1
            
            if j < 0:
                positions.append(i)
                self.steps.append((i, "找到匹配"))
                i += 1
            else:
                char_shift = j - bad_char.get(text[k], -1)
                suffix_shift = self._get_suffix_shift(j, suffix, prefix, m)
                shift = max(char_shift, suffix_shift)
                
                if last_mismatch >= 0:
                    shift = max(shift, last_mismatch - j)
                
                i += shift
                last_mismatch = j
                self.steps.append((shift, "Turbo移动"))
        
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
            elif operation == "移动距离" or operation == "Turbo移动":
                print(f"{operation}：{val}")
            elif operation == "标记前缀":
                print(f"{operation}：长度 {val}")
        elif len(step) == 3:
            val1, val2, operation = step
            if operation == "设置坏字符位置":
                print(f"{operation}：字符 '{val1}' 位置 {val2}")
            elif operation == "设置后缀位置":
                print(f"{operation}：长度 {val1} 位置 {val2}")
            elif operation in ["字符匹配", "Turbo匹配", "常规匹配"]:
                print(f"{operation}：文本位置 {val1} 模式串位置 {val2}")

if __name__ == '__main__':
    try:
        # 创建Boyer-Moore对象
        bm = BoyerMoore()
        
        # 获取输入文本
        text = input("请输入文本：").strip()
        if not text:
            raise ValueError("文本不能为空！")
        
        while True:
            print("\n请选择操作：")
            print("1. 常规匹配")
            print("2. 优化匹配")
            print("3. 退出")
            
            choice = input("请输入选择（1-3）：")
            
            if choice == '1':
                pattern = input("请输入要搜索的模式串：").strip()
                if pattern:
                    positions = bm.search(text, pattern)
                    if positions:
                        print("\n找到的匹配位置：")
                        for pos in positions:
                            print(f"位置 {pos}")
                    else:
                        print("未找到匹配！")
                else:
                    print("模式串不能为空！")
            
            elif choice == '2':
                pattern = input("请输入要搜索的模式串：").strip()
                if pattern:
                    positions = bm.optimize_search(text, pattern)
                    if positions:
                        print("\n找到的匹配位置：")
                        for pos in positions:
                            print(f"位置 {pos}")
                    else:
                        print("未找到匹配！")
                else:
                    print("模式串不能为空！")
            
            elif choice == '3':
                break
            
            else:
                print("无效的选择！")
        
        # 打印操作过程
        print_operations(bm.steps)
        
    except ValueError as e:
        print(f"错误：{str(e)}") 