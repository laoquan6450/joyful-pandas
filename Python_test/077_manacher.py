#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现Manacher算法及其应用。

程序分析：
1. 实现字符串预处理
2. 实现回文半径数组构建
3. 实现最长回文子串查找
4. 支持所有回文子串统计
"""

from typing import List, Tuple

class Manacher:
    def __init__(self, text: str):
        self.original = text
        self.processed = self._preprocess(text)
        self.n = len(self.processed)
        self.radius = [0] * self.n  # 回文半径数组
        self.steps = []  # 记录操作步骤
        self._build_radius_array()
    
    def _preprocess(self, s: str) -> str:
        """预处理字符串，在字符间插入特殊字符"""
        processed = ['#']
        for c in s:
            processed.extend([c, '#'])
        result = ''.join(processed)
        self.steps.append((result, "预处理字符串"))
        return result
    
    def _build_radius_array(self) -> None:
        """构建回文半径数组"""
        center = 0      # 当前回文串的中心
        right = 0      # 当前回文串的右边界
        
        for i in range(self.n):
            if i < right:
                # 利用对称性进行优化
                mirror = 2 * center - i
                self.radius[i] = min(right - i, self.radius[mirror])
            
            # 尝试扩展回文串
            left = i - (self.radius[i] + 1)
            r = i + (self.radius[i] + 1)
            
            while left >= 0 and r < self.n and self.processed[left] == self.processed[r]:
                self.radius[i] += 1
                left -= 1
                r += 1
            
            # 更新中心和右边界
            if i + self.radius[i] > right:
                center = i
                right = i + self.radius[i]
                self.steps.append((i, self.radius[i], "更新回文中心"))
    
    def find_longest_palindrome(self) -> str:
        """查找最长回文子串"""
        max_len = 0
        center = 0
        
        for i in range(self.n):
            if self.radius[i] > max_len:
                max_len = self.radius[i]
                center = i
                self.steps.append((max_len, "更新最长回文串"))
        
        # 还原原始字符串中的回文子串
        start = (center - max_len) // 2
        length = max_len
        result = self.original[start:start + length]
        return result
    
    def count_all_palindromes(self) -> List[Tuple[str, int]]:
        """统计所有回文子串及其出现次数"""
        palindromes = {}
        
        for i in range(self.n):
            for length in range(self.radius[i] + 1):
                if length == 0:
                    continue
                
                # 计算在原始字符串中的位置和长度
                start = (i - length) // 2
                if length % 2 == 0:
                    actual_len = length // 2
                else:
                    actual_len = (length + 1) // 2
                
                if start >= 0 and start + actual_len <= len(self.original):
                    palindrome = self.original[start:start + actual_len]
                    if palindrome:
                        palindromes[palindrome] = palindromes.get(palindrome, 0) + 1
                        self.steps.append((palindrome, "发现回文串"))
        
        return sorted(palindromes.items(), key=lambda x: (-len(x[0]), x[0]))
    
    def count_palindrome_substrings(self) -> int:
        """计算回文子串的总数"""
        count = 0
        for r in self.radius:
            count += (r + 1) // 2
        self.steps.append((count, "统计回文子串数量"))
        return count

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if len(step) == 2:
            val, operation = step
            if operation == "预处理字符串":
                print(f"{operation}：'{val}'")
            elif operation == "更新最长回文串":
                print(f"{operation}：长度 {val}")
            elif operation == "发现回文串":
                print(f"{operation}：'{val}'")
            elif operation == "统计回文子串数量":
                print(f"{operation}：{val}")
        elif len(step) == 3:
            pos, rad, operation = step
            if operation == "更新回文中心":
                print(f"{operation}：位置 {pos}，半径 {rad}")

if __name__ == '__main__':
    try:
        # 获取输入文本
        text = input("请输入文本：").strip()
        if not text:
            raise ValueError("文本不能为空！")
        
        # 创建Manacher对象
        manacher = Manacher(text)
        
        while True:
            print("\n请选择操作：")
            print("1. 查找最长回文子串")
            print("2. 查看所有回文子串")
            print("3. 统计回文子串数量")
            print("4. 退出")
            
            choice = input("请输入选择（1-4）：")
            
            if choice == '1':
                result = manacher.find_longest_palindrome()
                print(f"\n最长回文子串为：'{result}'")
            
            elif choice == '2':
                palindromes = manacher.count_all_palindromes()
                if palindromes:
                    print("\n所有回文子串（及出现次数）：")
                    for palindrome, count in palindromes:
                        print(f"'{palindrome}': {count}次")
                else:
                    print("没有找到回文子串！")
            
            elif choice == '3':
                count = manacher.count_palindrome_substrings()
                print(f"\n回文子串的总数为：{count}")
            
            elif choice == '4':
                break
            
            else:
                print("无效的选择！")
        
        # 打印操作过程
        print_operations(manacher.steps)
        
    except ValueError as e:
        print(f"错误：{str(e)}") 