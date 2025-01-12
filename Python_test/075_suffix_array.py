#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现后缀数组（Suffix Array）及其基本操作。

程序分析：
1. 实现后缀数组的构建
2. 实现高度数组构建
3. 实现字符串匹配功能
4. 支持最长公共子串查找
"""

from typing import List, Tuple
from collections import defaultdict

class SuffixArray:
    def __init__(self, text: str):
        self.text = text + "$"  # 添加终止符
        self.n = len(self.text)
        self.suffix_array = []  # 后缀数组
        self.rank = []         # 名次数组
        self.height = []       # 高度数组
        self.steps = []        # 记录操作步骤
        self._build_suffix_array()
        self._build_height_array()
    
    def _build_suffix_array(self) -> None:
        """构建后缀数组"""
        # 初始化
        suffixes = [(i, self.text[i:]) for i in range(self.n)]
        self.steps.append(("初始化后缀", len(suffixes)))
        
        # 按字典序排序所有后缀
        suffixes.sort(key=lambda x: x[1])
        self.steps.append(("排序后缀", len(suffixes)))
        
        # 提取排序后的位置
        self.suffix_array = [pos for pos, _ in suffixes]
        
        # 计算rank数组
        self.rank = [0] * self.n
        for i, pos in enumerate(self.suffix_array):
            self.rank[pos] = i
            self.steps.append((pos, i, "设置名次"))
    
    def _build_height_array(self) -> None:
        """构建高度数组（LCP）"""
        self.height = [0] * self.n
        h = 0  # height[i]的值不会小于h-1
        
        for i in range(self.n):
            if self.rank[i] > 0:
                j = self.suffix_array[self.rank[i] - 1]
                while i + h < self.n and j + h < self.n and \
                      self.text[i + h] == self.text[j + h]:
                    h += 1
                self.height[self.rank[i]] = h
                self.steps.append((i, h, "设置高度"))
                if h > 0:
                    h -= 1
    
    def search(self, pattern: str) -> List[int]:
        """在文本中搜索模式串，返回所有匹配位置"""
        if not pattern:
            return []
        
        # 二分查找
        left = 0
        right = self.n - 1
        result = []
        
        # 查找左边界
        left_bound = self._binary_search(pattern, True)
        if left_bound == -1:
            return []
        
        # 查找右边界
        right_bound = self._binary_search(pattern, False)
        
        # 收集区间内的所有位置
        for i in range(left_bound, right_bound + 1):
            result.append(self.suffix_array[i])
            self.steps.append((self.suffix_array[i], "找到匹配"))
        
        return sorted(result)
    
    def _binary_search(self, pattern: str, find_left: bool) -> int:
        """二分查找模式串的边界"""
        left = 0
        right = self.n - 1
        result = -1
        
        while left <= right:
            mid = (left + right) // 2
            pos = self.suffix_array[mid]
            current = self.text[pos:pos + len(pattern)]
            
            if current == pattern:
                result = mid
                if find_left:
                    right = mid - 1
                else:
                    left = mid + 1
                self.steps.append((mid, "找到边界"))
            elif current < pattern:
                left = mid + 1
            else:
                right = mid - 1
            
            self.steps.append((mid, "二分查找"))
        
        return result
    
    def find_longest_common_substring(self, other: str) -> str:
        """查找两个字符串的最长公共子串"""
        # 使用特殊字符分隔两个字符串
        combined = self.text[:-1] + "#" + other + "$"
        n1 = len(self.text) - 1
        n2 = len(other)
        
        # 构建组合字符串的后缀数组
        combined_sa = SuffixArray(combined)
        
        # 在height数组中寻找最长的LCP，且两个后缀分别来自两个字符串
        max_len = 0
        result_pos = 0
        
        for i in range(1, len(combined)):
            if combined_sa.height[i] > max_len:
                pos1 = combined_sa.suffix_array[i-1]
                pos2 = combined_sa.suffix_array[i]
                # 确保两个后缀分别来自两个字符串
                if (pos1 < n1 and pos2 > n1) or (pos1 > n1 and pos2 < n1):
                    max_len = combined_sa.height[i]
                    result_pos = min(pos1, pos2)
                    self.steps.append((max_len, "更新最长公共子串"))
        
        return self.text[result_pos:result_pos + max_len]

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if len(step) == 2:
            val, operation = step
            if operation == "初始化后缀":
                print(f"{operation}：共 {val} 个")
            elif operation == "排序后缀":
                print(f"{operation}：共 {val} 个")
            elif operation == "二分查找":
                print(f"{operation}：位置 {val}")
            elif operation == "找到边界":
                print(f"{operation}：位置 {val}")
            elif operation == "找到匹配":
                print(f"{operation}：位置 {val}")
        elif len(step) == 3:
            val1, val2, operation = step
            if operation == "设置名次":
                print(f"{operation}：位置 {val1} 名次 {val2}")
            elif operation == "设置高度":
                print(f"{operation}：位置 {val1} 高度 {val2}")
            elif operation == "更新最长公共子串":
                print(f"{operation}：长度 {val1}")

if __name__ == '__main__':
    try:
        # 获取输入文本
        text = input("请输入文本：").strip()
        if not text:
            raise ValueError("文本不能为空！")
        
        # 创建后缀数组
        sa = SuffixArray(text)
        
        while True:
            print("\n请选择操作：")
            print("1. 搜索模式串")
            print("2. 查找最长公共子串")
            print("3. 退出")
            
            choice = input("请输入选择（1-3）：")
            
            if choice == '1':
                pattern = input("请输入要搜索的模式串：").strip()
                if pattern:
                    positions = sa.search(pattern)
                    if positions:
                        print("\n找到的匹配位置：")
                        for pos in positions:
                            print(f"位置 {pos}")
                    else:
                        print("未找到匹配！")
                else:
                    print("模式串不能为空！")
            
            elif choice == '2':
                other = input("请输入另一个字符串：").strip()
                if other:
                    result = sa.find_longest_common_substring(other)
                    if result:
                        print(f"\n最长公共子串为：'{result}'")
                    else:
                        print("没有找到公共子串！")
                else:
                    print("字符串不能为空！")
            
            elif choice == '3':
                break
            
            else:
                print("无效的选择！")
        
        # 打印操作过程
        print_operations(sa.steps)
        
    except ValueError as e:
        print(f"错误：{str(e)}")