#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现Rabin-Karp字符串匹配算法。

程序分析：
1. 实现哈希函数
2. 实现滚动哈希
3. 支持多模式串匹配
4. 优化匹配过程
"""

from typing import List, Dict, Set
from collections import defaultdict

class RabinKarp:
    def __init__(self, base: int = 256, prime: int = 101):
        self.base = base      # 进制数（通常使用字符集大小）
        self.prime = prime    # 用于取模的质数
        self.steps = []       # 记录操作步骤
    
    def _hash(self, s: str) -> int:
        """计算字符串的哈希值"""
        h = 0
        for c in s:
            h = (h * self.base + ord(c)) % self.prime
            self.steps.append((c, h, "计算哈希"))
        return h
    
    def _rolling_hash(self, old_hash: int, old_char: str, new_char: str, power: int) -> int:
        """计算滚动哈希值"""
        # 移除最高位，添加新的最低位
        h = (old_hash - ord(old_char) * power) % self.prime
        h = (h * self.base + ord(new_char)) % self.prime
        # 处理负数情况
        if h < 0:
            h += self.prime
        self.steps.append((old_char, new_char, h, "滚动哈希"))
        return h
    
    def search(self, text: str, pattern: str) -> List[int]:
        """在文本中搜索模式串，返回所有匹配位置"""
        if not pattern or not text:
            return []
        
        m = len(pattern)
        n = len(text)
        if m > n:
            return []
        
        # 计算用于移除最高位的幂
        power = pow(self.base, m-1) % self.prime
        
        # 计算模式串的哈希值
        pattern_hash = self._hash(pattern)
        self.steps.append((pattern, pattern_hash, "模式串哈希"))
        
        # 计算文本第一个窗口的哈希值
        text_hash = self._hash(text[:m])
        self.steps.append((text[:m], text_hash, "窗口哈希"))
        
        positions = []
        
        # 检查第一个窗口
        if text_hash == pattern_hash and text[:m] == pattern:
            positions.append(0)
            self.steps.append((0, "找到匹配"))
        
        # 滑动窗口
        for i in range(n - m):
            # 计算下一个窗口的哈希值
            text_hash = self._rolling_hash(text_hash, text[i], text[i+m], power)
            
            # 如果哈希值匹配，进行字符串比较
            if text_hash == pattern_hash and text[i+1:i+m+1] == pattern:
                positions.append(i + 1)
                self.steps.append((i + 1, "找到匹配"))
        
        return positions
    
    def multi_pattern_search(self, text: str, patterns: List[str]) -> Dict[str, List[int]]:
        """多模式串匹配"""
        result = {}
        # 按长度分组模式串
        patterns_by_length = defaultdict(list)
        for pattern in patterns:
            patterns_by_length[len(pattern)].append(pattern)
        
        # 对每组长度的模式串进行匹配
        for length, group in patterns_by_length.items():
            # 计算所有模式串的哈希值
            pattern_hashes = {pattern: self._hash(pattern) for pattern in group}
            self.steps.append((length, len(group), "分组处理"))
            
            # 在文本中搜索
            n = len(text)
            if length > n:
                continue
            
            # 计算用于移除最高位的幂
            power = pow(self.base, length-1) % self.prime
            
            # 计算第一个窗口的哈希值
            text_hash = self._hash(text[:length])
            
            # 检查第一个窗口
            window = text[:length]
            for pattern in group:
                if text_hash == pattern_hashes[pattern] and window == pattern:
                    if pattern not in result:
                        result[pattern] = []
                    result[pattern].append(0)
                    self.steps.append((pattern, 0, "找到多模式匹配"))
            
            # 滑动窗口
            for i in range(n - length):
                text_hash = self._rolling_hash(text_hash, text[i], text[i+length], power)
                window = text[i+1:i+length+1]
                
                for pattern in group:
                    if text_hash == pattern_hashes[pattern] and window == pattern:
                        if pattern not in result:
                            result[pattern] = []
                        result[pattern].append(i + 1)
                        self.steps.append((pattern, i + 1, "找到多模式匹配"))
        
        return result

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if len(step) == 2:
            val, operation = step
            if operation == "找到匹配":
                print(f"{operation}：位置 {val}")
        elif len(step) == 3:
            if step[2] == "计算哈希" or step[2] == "窗口哈希":
                char, hash_val, _ = step
                print(f"{step[2]}：'{char}' -> {hash_val}")
            elif step[2] == "模式串哈希":
                pattern, hash_val, _ = step
                print(f"模式串哈希：'{pattern}' -> {hash_val}")
            elif step[2] == "分组处理":
                length, count, _ = step
                print(f"分组处理：长度 {length}，{count}个模式串")
            elif step[2] == "找到多模式匹配":
                pattern, pos, _ = step
                print(f"找到多模式匹配：'{pattern}' 位置 {pos}")
        elif len(step) == 4:
            old_char, new_char, hash_val, operation = step
            if operation == "滚动哈希":
                print(f"滚动哈希：移除 '{old_char}'，添加 '{new_char}' -> {hash_val}")

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
        # 创建Rabin-Karp对象
        rk = RabinKarp()
        
        # 获取输入文本
        text = input("请输入文本：").strip()
        if not text:
            raise ValueError("文本不能为空！")
        
        while True:
            print("\n请选择操作：")
            print("1. 单模式串匹配")
            print("2. 多模式串匹配")
            print("3. 退出")
            
            choice = input("请输入选择（1-3）：")
            
            if choice == '1':
                pattern = input("请输入要搜索的模式串：").strip()
                if pattern:
                    positions = rk.search(text, pattern)
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
                    results = rk.multi_pattern_search(text, patterns)
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
                break
            
            else:
                print("无效的选择！")
        
        # 打印操作过程
        print_operations(rk.steps)
        
    except ValueError as e:
        print(f"错误：{str(e)}") 