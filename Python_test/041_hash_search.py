#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现哈希查找算法，使用开放地址法处理冲突。

程序分析：
1. 实现一个简单的哈希表
2. 使用线性探测法处理冲突
3. 包含插入和查找操作
4. 与其他查找方法比较性能
"""

class HashTable:
    def __init__(self, size=20):
        self.size = size
        self.table = [None] * size
        self.steps = []  # 记录操作步骤
    
    def hash_function(self, key: float) -> int:
        """简单的哈希函数"""
        return int(key * 13) % self.size
    
    def insert(self, key: float) -> None:
        """插入一个键"""
        index = self.hash_function(key)
        self.steps.append((index, f"计算哈希值：{index}"))
        
        # 线性探测
        while self.table[index] is not None:
            self.steps.append((index, f"位置 {index} 已占用，继续探测"))
            index = (index + 1) % self.size
        
        self.table[index] = key
        self.steps.append((index, f"插入值 {key} 到位置 {index}"))
    
    def search(self, key: float) -> Tuple[int, List[Tuple[int, str]]]:
        """查找一个键"""
        steps = []
        original_index = self.hash_function(key)
        index = original_index
        steps.append((index, f"计算哈希值：{index}"))
        
        while self.table[index] is not None:
            steps.append((index, f"检查位置 {index}"))
            if self.table[index] == key:
                steps.append((index, "找到目标值"))
                return index, steps
            index = (index + 1) % self.size
            if index == original_index:
                break
        
        steps.append((-1, "未找到目标值"))
        return -1, steps

# ... [其余代码与之前类似，包括性能比较和测试函数] 