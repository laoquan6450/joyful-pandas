#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现Shift-And字符串匹配算法。

程序分析：
1. 实现位向量构建
2. 实现位运算匹配
3. 支持模糊匹配
4. 优化匹配过程
"""

from typing import List, Dict, Set
from collections import defaultdict

class ShiftAnd:
    def __init__(self):
        self.steps = []  # 记录操作步骤
    
    def _build_mask(self, pattern: str) -> Dict[str, int]:
        """构建字符位掩码"""
        m = len(pattern)
        mask = defaultdict(int)
        
        # 为每个字符构建位掩码
        for i in range(m):
            mask[pattern[i]] |= (1 << i)
            self.steps.append((pattern[i], bin(mask[pattern[i]]), "设置位掩码"))
        
        return mask
    
    def search(self, text: str, pattern: str) -> List[int]:
        """在文本中搜索模式串，返回所有匹配位置"""
        if not pattern or not text:
            return []
        
        # 构建位掩码
        mask = self._build_mask(pattern)
        positions = []
        m = len(pattern)
        state = 0
        match_bit = 1 << (m - 1)
        
        # 遍历文本进行匹配
        for i, c in enumerate(text):
            # 状态转移：左移一位并与当前字符的位掩码相与
            state = ((state << 1) | 1) & mask[c]
            self.steps.append((i, bin(state), "状态转移"))
            
            # 检查是否匹配
            if state & match_bit:
                positions.append(i - m + 1)
                self.steps.append((i - m + 1, "找到匹配"))
        
        return positions
    
    def fuzzy_search(self, text: str, pattern: str, k: int) -> List[int]:
        """支持k个错误的模糊匹配"""
        if not pattern or not text or k < 0:
            return []
        
        m = len(pattern)
        mask = self._build_mask(pattern)
        positions = []
        
        # 初始化k+1个状态，每个状态表示对应数量的错误
        states = [0] * (k + 1)
        match_bit = 1 << (m - 1)
        
        for i, c in enumerate(text):
            # 更新每个错误数量的状态
            old_states = states.copy()
            
            # 状态转移
            states[0] = ((old_states[0] << 1) | 1) & mask[c]
            self.steps.append((i, 0, bin(states[0]), "模糊匹配状态"))
            
            for j in range(1, k + 1):
                # 允许j个错误的状态转移
                substitution = (old_states[j-1] << 1) | 1  # 替换
                deletion = old_states[j] << 1              # 删除
                insertion = old_states[j-1] << 1           # 插入
                
                states[j] = (substitution | deletion | insertion) & mask[c]
                self.steps.append((i, j, bin(states[j]), "错误状态更新"))
            
            # 检查所有状态是否有匹配
            for j in range(k + 1):
                if states[j] & match_bit:
                    positions.append((i - m + 1, j))
                    self.steps.append((i - m + 1, j, "找到模糊匹配"))
        
        return positions
    
    def optimize_search(self, text: str, pattern: str) -> List[int]:
        """优化的Shift-And搜索算法"""
        if not pattern or not text:
            return []
        
        # 使用64位整数优化
        mask = self._build_mask(pattern)
        positions = []
        m = len(pattern)
        state = 0
        match_bit = 1 << (m - 1)
        
        # 预处理文本中的字符位置
        char_positions = defaultdict(list)
        for i, c in enumerate(text):
            char_positions[c].append(i)
            self.steps.append((c, i, "预处理字符位置"))
        
        # 只处理模式串中出现的字符
        pattern_chars = set(pattern)
        for c in pattern_chars:
            for pos in char_positions[c]:
                state = ((state << 1) | 1) & mask[c]
                self.steps.append((pos, bin(state), "优化状态转移"))
                
                if state & match_bit:
                    positions.append(pos - m + 1)
                    self.steps.append((pos - m + 1, "找到优化匹配"))
        
        return sorted(positions)

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if len(step) == 2:
            val, operation = step
            if operation == "找到匹配" or operation == "找到优化匹配":
                print(f"{operation}：位置 {val}")
        elif len(step) == 3:
            if step[2] == "设置位掩码":
                char, bits, _ = step
                print(f"设置位掩码：字符 '{char}' 掩码 {bits}")
            elif step[2] == "状态转移" or step[2] == "优化状态转移":
                pos, bits, _ = step
                print(f"{step[2]}：位置 {pos} 状态 {bits}")
            elif step[2] == "预处理字符位置":
                char, pos, _ = step
                print(f"预处理字符位置：字符 '{char}' 位置 {pos}")
            elif step[2] == "找到模糊匹配":
                pos, errors, _ = step
                print(f"找到模糊匹配：位置 {pos} 错误数 {errors}")
        elif len(step) == 4:
            pos, errors, bits, operation = step
            if operation in ["模糊匹配状态", "错误状态更新"]:
                print(f"{operation}：位置 {pos} 错误数 {errors} 状态 {bits}")

if __name__ == '__main__':
    try:
        # 创建Shift-And对象
        sa = ShiftAnd()
        
        # 获取输入文本
        text = input("请输入文本：").strip()
        if not text:
            raise ValueError("文本不能为空！")
        
        while True:
            print("\n请选择操作：")
            print("1. 精确匹配")
            print("2. 模糊匹配")
            print("3. 优化匹配")
            print("4. 退出")
            
            choice = input("请输入选择（1-4）：")
            
            if choice == '1':
                pattern = input("请输入要搜索的模式串：").strip()
                if pattern:
                    positions = sa.search(text, pattern)
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
                    try:
                        k = int(input("请输入允许的错误数量："))
                        if k < 0:
                            raise ValueError("错误数量必须大于等于0！")
                        positions = sa.fuzzy_search(text, pattern, k)
                        if positions:
                            print("\n找到的模糊匹配：")
                            for pos, errors in positions:
                                print(f"位置 {pos}（{errors}个错误）")
                        else:
                            print("未找到匹配！")
                    except ValueError as e:
                        print(f"错误：{str(e)}")
                else:
                    print("模式串不能为空！")
            
            elif choice == '3':
                pattern = input("请输入要搜索的模式串：").strip()
                if pattern:
                    positions = sa.optimize_search(text, pattern)
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
        print_operations(sa.steps)
        
    except ValueError as e:
        print(f"错误：{str(e)}") 