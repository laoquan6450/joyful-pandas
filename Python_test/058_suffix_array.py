#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现后缀数组（Suffix Array）及其基本操作。

程序分析：
1. 实现后缀数组的构建
2. 实现高度数组的构建
3. 实现字符串匹配功能
4. 优化构建过程
"""

from typing import List, Tuple

class SuffixArray:
    def __init__(self, text: str):
        self.text = text + '$'  # 添加终止符
        self.n = len(self.text)
        self.sa = []   # 后缀数组
        self.rank = [] # 名次数组
        self.height = [] # 高度数组
        self.steps = []  # 记录操作步骤
        self._build()
    
    def _build(self) -> None:
        """构建后缀数组"""
        # 初始化后缀数组和名次数组
        suffixes = [(i, self.text[i:]) for i in range(self.n)]
        self.steps.append(("初始化后缀", suffixes))
        
        # 按字典序排序所有后缀
        suffixes.sort(key=lambda x: x[1])
        self.steps.append(("排序后缀", suffixes))
        
        # 提取后缀数组
        self.sa = [pos for pos, _ in suffixes]
        
        # 计算名次数组
        self.rank = [0] * self.n
        for i in range(self.n):
            self.rank[self.sa[i]] = i
        self.steps.append(("计算名次", self.rank))
        
        # 计算高度数组
        self._build_height()
    
    def _build_height(self) -> None:
        """构建高度数组"""
        self.height = [0] * self.n
        h = 0  # 当前LCP长度
        
        for i in range(self.n):
            if self.rank[i] > 0:
                j = self.sa[self.rank[i] - 1]
                while i + h < self.n and j + h < self.n and \
                      self.text[i + h] == self.text[j + h]:
                    h += 1
                self.height[self.rank[i]] = h
                self.steps.append(("计算高度", i, h))
                if h > 0:
                    h -= 1
    
    def find(self, pattern: str) -> List[int]:
        """查找模式串，返回所有匹配位置"""
        left, right = 0, self.n - 1
        results = []
        
        # 二分查找
        while left <= right:
            mid = (left + right) // 2
            suffix = self.text[self.sa[mid]:]
            self.steps.append(("比较", pattern, suffix[:len(pattern)]))
            
            if suffix.startswith(pattern):
                # 找到匹配，扩展范围
                start = mid
                while start > 0 and self.text[self.sa[start-1]:].startswith(pattern):
                    start -= 1
                end = mid
                while end < self.n-1 and self.text[self.sa[end+1]:].startswith(pattern):
                    end += 1
                
                for i in range(start, end + 1):
                    results.append(self.sa[i])
                self.steps.append(("找到匹配", results))
                break
            elif pattern > suffix[:len(pattern)]:
                left = mid + 1
                self.steps.append(("向右查找", left, right))
            else:
                right = mid - 1
                self.steps.append(("向左查找", left, right))
        
        return sorted(results)

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if step[0] == "初始化后缀":
            print("初始化后缀数组：")
            for pos, suffix in step[1][:5]:  # 只显示前5个
                print(f"位置 {pos}: {suffix}")
            if len(step[1]) > 5:
                print("...")
        elif step[0] == "排序后缀":
            print("排序后的后缀：")
            for pos, suffix in step[1][:5]:
                print(f"位置 {pos}: {suffix}")
            if len(step[1]) > 5:
                print("...")
        elif step[0] == "计算名次":
            print("名次数组：", step[1])
        elif step[0] == "计算高度":
            print(f"计算位置 {step[1]} 的高度：{step[2]}")
        elif step[0] == "比较":
            print(f"比较模式串 '{step[1]}' 与后缀 '{step[2]}'")
        elif step[0] == "找到匹配":
            print(f"找到匹配位置：{step[1]}")
        else:  # 向左/右查找
            print(f"{step[0]}：范围 [{step[1]}, {step[2]}]")

def get_input_text():
    """获取用户输入的文本"""
    while True:
        text = input("请输入一个字符串（仅包含小写字母）：").strip().lower()
        if text.isalpha():
            return text
        print("请只输入字母！")

if __name__ == '__main__':
    try:
        # 获取输入文本
        text = get_input_text()
        print(f"\n输入的文本：{text}")
        
        # 构建后缀数组
        sa = SuffixArray(text)
        
        while True:
            print("\n请选择操作：")
            print("1. 查找模式串")
            print("2. 显示后缀数组")
            print("3. 退出")
            
            choice = input("请输入选择（1-3）：")
            
            if choice == '1':
                pattern = input("请输入要查找的模式串：").strip().lower()
                if not pattern.isalpha():
                    print("请只输入字母！")
                    continue
                    
                positions = sa.find(pattern)
                if positions:
                    print(f"\n在以下位置找到模式串 '{pattern}'：")
                    print(positions)
                else:
                    print(f"\n未找到模式串 '{pattern}'")
            
            elif choice == '2':
                print("\n后缀数组：")
                for i, pos in enumerate(sa.sa):
                    print(f"{i}: {sa.text[pos:]}")
            
            elif choice == '3':
                break
            
            else:
                print("无效的选择！")
        
        # 打印操作过程
        print_operations(sa.steps)
        
    except ValueError as e:
        print(f"错误：{str(e)}") 