#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现跳表（Skip List）及其基本操作。

程序分析：
1. 实现跳表的节点和层级结构
2. 实现插入、删除、查找操作
3. 实现随机层数生成
4. 维护多层索引结构
"""

import random
from typing import Optional, List, Tuple

class SkipNode:
    def __init__(self, key: int, level: int):
        self.key = key
        self.forward = [None] * (level + 1)  # 每层的前向指针

class SkipList:
    def __init__(self, max_level: int = 16, p: float = 0.5):
        self.max_level = max_level
        self.p = p  # 层数增加的概率
        self.level = 0  # 当前最大层数
        self.header = SkipNode(-1, max_level)  # 头节点
        self.steps = []  # 记录操作步骤
    
    def _random_level(self) -> int:
        """随机生成层数"""
        level = 0
        while random.random() < self.p and level < self.max_level:
            level += 1
        return level
    
    def insert(self, key: int) -> None:
        """插入关键字"""
        update = [None] * (self.max_level + 1)
        current = self.header
        
        # 从最高层开始查找插入位置
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
                self.steps.append((current.key, i, "向前移动"))
            update[i] = current
        
        # 生成随机层数
        new_level = self._random_level()
        if new_level > self.level:
            for i in range(self.level + 1, new_level + 1):
                update[i] = self.header
            self.level = new_level
        
        # 创建新节点
        new_node = SkipNode(key, new_level)
        self.steps.append((key, new_level, "创建新节点"))
        
        # 更新指针
        for i in range(new_level + 1):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node
            self.steps.append((key, i, "更新指针"))
    
    def find(self, key: int) -> bool:
        """查找关键字"""
        current = self.header
        
        # 从最高层开始查找
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
                self.steps.append((current.key, i, "向前查找"))
            
            if current.forward[i] and current.forward[i].key == key:
                self.steps.append((key, i, "找到"))
                return True
        
        self.steps.append((key, -1, "未找到"))
        return False

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, (key, level, operation) in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if operation == "创建新节点":
            print(f"{operation}：键值 {key}，层数 {level}")
        elif operation == "更新指针":
            print(f"{operation}：键值 {key}，层 {level}")
        elif operation == "向前移动" or operation == "向前查找":
            print(f"{operation}：当前节点 {key}，层 {level}")
        else:  # 找到/未找到
            if level == -1:
                print(f"{operation}：键值 {key}")
            else:
                print(f"{operation}：键值 {key}，层 {level}")

def get_input_numbers():
    """获取用户输入的数字"""
    numbers = []
    print("请输入5个不同的数字：")
    while len(numbers) < 5:
        try:
            num = int(input(f"请输入第{len(numbers)+1}个数字："))
            if num in numbers:
                print("该数字已存在，请输入不同的数字！")
                continue
            numbers.append(num)
        except ValueError:
            print("请输入有效的整数！")
    return numbers

if __name__ == '__main__':
    try:
        # 创建跳表
        skip_list = SkipList()
        
        # 获取输入数字并插入
        numbers = get_input_numbers()
        print(f"\n插入的数字：{numbers}")
        for num in numbers:
            skip_list.insert(num)
        
        while True:
            print("\n请选择操作：")
            print("1. 插入数字")
            print("2. 查找数字")
            print("3. 退出")
            
            choice = input("请输入选择（1-3）：")
            
            if choice == '1':
                num = int(input("请输入要插入的数字："))
                skip_list.insert(num)
                print("插入成功！")
            
            elif choice == '2':
                num = int(input("请输入要查找的数字："))
                found = skip_list.find(num)
                print("找到数字！" if found else "未找到数字！")
            
            elif choice == '3':
                break
            
            else:
                print("无效的选择！")
        
        # 打印操作过程
        print_operations(skip_list.steps)
        
    except ValueError as e:
        print(f"错误：{str(e)}") 