#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现Wu-Manber多模式串匹配算法。

程序分析：
1. 实现坏字符移动表
2. 实现哈希函数
3. 实现模式串匹配
4. 优化匹配过程
"""

from typing import List, Dict, Set, Tuple
from collections import defaultdict

class WuManber:
    def __init__(self, block_size: int = 2):
        self.block_size = block_size  # 块大小
        self.steps = []  # 记录操作步骤
    
    def _hash(self, block: str) -> int:
        """计算块的哈希值"""
        h = 0
        for c in block:
            h = (h * 256 + ord(c)) % 16384  # 使用较小的质数以提高效率
        self.steps.append((block, h, "计算哈希"))
        return h
    
    def _build_shift_table(self, patterns: List[str], min_len: int) -> Dict[int, int]:
        """构建移动表"""
        shift = defaultdict(lambda: min_len - self.block_size + 1)
        
        # 对每个模式串的每个块计算移动距离
        for pattern in patterns:
            for i in range(len(pattern) - self.block_size):
                block = pattern[i:i + self.block_size]
                block_hash = self._hash(block)
                distance = min_len - i - self.block_size
                if distance > 0:
                    shift[block_hash] = min(shift[block_hash], distance)
                    self.steps.append((block, distance, "设置移动距离"))
        
        return shift
    
    def _build_prefix_table(self, patterns: List[str]) -> Dict[int, List[Tuple[str, str]]]:
        """构建前缀表"""
        prefix = defaultdict(list)
        
        # 对每个模式串的前缀块建立映射
        for pattern in patterns:
            if len(pattern) >= self.block_size:
                block = pattern[:self.block_size]
                block_hash = self._hash(block)
                prefix[block_hash].append((block, pattern))
                self.steps.append((block, pattern, "添加前缀映射"))
        
        return prefix
    
    def search(self, text: str, patterns: List[str]) -> Dict[str, List[int]]:
        """在文本中搜索多个模式串"""
        if not patterns or not text:
            return {}
        
        # 找出最短模式串长度
        min_len = min(len(p) for p in patterns)
        if min_len < self.block_size:
            return {}
        
        # 构建移动表和前缀表
        shift = self._build_shift_table(patterns, min_len)
        prefix = self._build_prefix_table(patterns)
        
        result = defaultdict(list)
        n = len(text)
        pos = min_len - 1
        
        while pos < n:
            # 获取当前位置的块
            if pos - self.block_size + 1 >= 0:
                block = text[pos - self.block_size + 1:pos + 1]
                block_hash = self._hash(block)
                self.steps.append((pos, block, "检查位置"))
                
                # 如果块在前缀表中，检查可能的匹配
                if block_hash in prefix:
                    for prefix_block, pattern in prefix[block_hash]:
                        if block == prefix_block:
                            start = pos - min_len + 1
                            if start >= 0 and start + len(pattern) <= n:
                                if text[start:start + len(pattern)] == pattern:
                                    result[pattern].append(start)
                                    self.steps.append((pattern, start, "找到匹配"))
                
                # 移动位置
                pos += shift[block_hash]
                self.steps.append((shift[block_hash], "移动距离"))
            else:
                pos += 1
        
        return dict(result)
    
    def optimize_search(self, text: str, patterns: List[str]) -> Dict[str, List[int]]:
        """优化的Wu-Manber搜索算法"""
        if not patterns or not text:
            return {}
        
        # 按长度分组模式串
        patterns_by_length = defaultdict(list)
        for pattern in patterns:
            if len(pattern) >= self.block_size:
                patterns_by_length[len(pattern)].append(pattern)
        
        result = {}
        
        # 对每组长度的模式串单独处理
        for length, group in patterns_by_length.items():
            self.steps.append((length, len(group), "分组处理"))
            matches = self.search(text, group)
            result.update(matches)
        
        return result

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if len(step) == 2:
            val, operation = step
            if operation == "移动距离":
                print(f"{operation}：{val}")
        elif len(step) == 3:
            if step[2] == "计算哈希":
                block, hash_val, _ = step
                print(f"计算哈希：块 '{block}' -> {hash_val}")
            elif step[2] == "设置移动距离":
                block, distance, _ = step
                print(f"设置移动距离：块 '{block}' -> {distance}")
            elif step[2] == "添加前缀映射":
                block, pattern, _ = step
                print(f"添加前缀映射：块 '{block}' -> 模式串 '{pattern}'")
            elif step[2] == "检查位置":
                pos, block, _ = step
                print(f"检查位置：{pos} 块 '{block}'")
            elif step[2] == "找到匹配":
                pattern, pos, _ = step
                print(f"找到匹配：模式串 '{pattern}' 位置 {pos}")
            elif step[2] == "分组处理":
                length, count, _ = step
                print(f"分组处理：长度 {length}，{count}个模式串")

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
        # 创建Wu-Manber对象
        wm = WuManber()
        
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
                patterns = get_input_patterns()
                if patterns:
                    results = wm.search(text, patterns)
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
            
            elif choice == '2':
                patterns = get_input_patterns()
                if patterns:
                    results = wm.optimize_search(text, patterns)
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
        print_operations(wm.steps)
        
    except ValueError as e:
        print(f"错误：{str(e)}") 