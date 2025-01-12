#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现B+树（B+ Tree）及其基本操作。

程序分析：
1. 实现B+树的基本结构
2. 实现节点分裂和合并
3. 实现范围查询功能
4. 维护叶节点链表
"""

from typing import List, Optional, Tuple, Any

class BPlusNode:
    def __init__(self, leaf: bool = True):
        self.keys = []         # 关键字列表
        self.children = []     # 子节点列表
        self.leaf = leaf      # 是否为叶节点
        self.next = None      # 下一个叶节点（仅叶节点有效）
        self.values = []      # 值列表（仅叶节点有效）
    
    def __str__(self):
        return f"Keys: {self.keys}"

class BPlusTree:
    def __init__(self, t: int):
        self.root = BPlusNode()
        self.t = t  # 最小度数
        self.steps = []  # 记录操作步骤
    
    def _split_child(self, parent: BPlusNode, index: int) -> None:
        """分裂子节点"""
        t = self.t
        child = parent.children[index]
        new_node = BPlusNode(child.leaf)
        
        # 将child的后半部分keys移动到new_node
        mid = t - 1
        if child.leaf:
            new_node.keys = child.keys[mid:]
            new_node.values = child.values[mid:]
            child.keys = child.keys[:mid]
            child.values = child.values[:mid]
            parent.keys.insert(index, new_node.keys[0])
        else:
            new_node.keys = child.keys[mid+1:]
            child.keys = child.keys[:mid]
            parent.keys.insert(index, child.keys[mid])
            new_node.children = child.children[mid+1:]
            child.children = child.children[:mid+1]
        
        # 维护叶节点链表
        if child.leaf:
            new_node.next = child.next
            child.next = new_node
        
        parent.children.insert(index + 1, new_node)
        self.steps.append((child.keys[mid], "分裂节点"))
    
    def insert(self, key: int, value: Any) -> None:
        """插入键值对"""
        root = self.root
        if len(root.keys) == 2 * self.t - 1:
            new_root = BPlusNode(False)
            self.root = new_root
            new_root.children.append(root)
            self._split_child(new_root, 0)
            self._insert_nonfull(new_root, key, value)
        else:
            self._insert_nonfull(root, key, value)
    
    def _insert_nonfull(self, node: BPlusNode, key: int, value: Any) -> None:
        """在非满节点中插入键值对"""
        i = len(node.keys) - 1
        
        if node.leaf:
            # 在叶节点中插入键值对
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            node.keys.insert(i, key)
            node.values.insert(i, value)
            self.steps.append((key, "插入键值对"))
        else:
            # 在内部节点中找到合适的子节点
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            
            if len(node.children[i].keys) == 2 * self.t - 1:
                self._split_child(node, i)
                if key >= node.keys[i]:
                    i += 1
            
            self._insert_nonfull(node.children[i], key, value)
    
    def search(self, key: int) -> Optional[Any]:
        """搜索关键字对应的值"""
        node = self._find_leaf(self.root, key)
        if node:
            try:
                i = node.keys.index(key)
                self.steps.append((key, "找到键值对"))
                return node.values[i]
            except ValueError:
                self.steps.append((key, "未找到键值对"))
                return None
        return None
    
    def _find_leaf(self, node: BPlusNode, key: int) -> Optional[BPlusNode]:
        """查找包含关键字的叶节点"""
        if node.leaf:
            return node
        
        i = 0
        while i < len(node.keys) and key >= node.keys[i]:
            i += 1
        
        self.steps.append((key, f"继续搜索子节点 {i}"))
        return self._find_leaf(node.children[i], key)
    
    def range_query(self, start_key: int, end_key: int) -> List[Tuple[int, Any]]:
        """范围查询"""
        result = []
        node = self._find_leaf(self.root, start_key)
        
        while node:
            for i, key in enumerate(node.keys):
                if start_key <= key <= end_key:
                    result.append((key, node.values[i]))
                    self.steps.append((key, "范围查询匹配"))
                elif key > end_key:
                    return result
            node = node.next
        
        return result

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if len(step) == 2:
            val, operation = step
            if operation == "插入键值对":
                print(f"{operation}：键 {val}")
            elif operation == "分裂节点":
                print(f"{operation}：中值 {val}")
            elif operation == "找到键值对":
                print(f"{operation}：键 {val}")
            elif operation == "未找到键值对":
                print(f"{operation}：键 {val}")
            elif operation == "范围查询匹配":
                print(f"{operation}：键 {val}")
            elif operation.startswith("继续搜索"):
                print(f"{operation}")

def get_input_pairs() -> List[Tuple[int, str]]:
    """获取用户输入的键值对"""
    pairs = []
    print("请输入键值对（每行输入'键 值'，输入非数字键结束）：")
    while True:
        try:
            line = input()
            key, value = line.split()
            key = int(key)
            pairs.append((key, value))
        except ValueError:
            break
    return pairs

if __name__ == '__main__':
    try:
        # 创建B+树（最小度数为2）
        bptree = BPlusTree(2)
        
        # 获取输入键值对并插入
        pairs = get_input_pairs()
        if not pairs:
            raise ValueError("至少需要输入一个键值对！")
        
        print("\n插入的键值对：")
        for key, value in pairs:
            print(f"键：{key}，值：{value}")
            bptree.insert(key, value)
        
        while True:
            print("\n请选择操作：")
            print("1. 插入键值对")
            print("2. 查找值")
            print("3. 范围查询")
            print("4. 退出")
            
            choice = input("请输入选择（1-4）：")
            
            if choice == '1':
                try:
                    print("请输入键值对（格式：键 值）：")
                    key, value = input().split()
                    key = int(key)
                    bptree.insert(key, value)
                    print("插入成功！")
                except ValueError:
                    print("请输入有效的键值对！")
            
            elif choice == '2':
                try:
                    key = int(input("请输入要查找的键："))
                    value = bptree.search(key)
                    if value is not None:
                        print(f"找到值：{value}")
                    else:
                        print("未找到该键！")
                except ValueError:
                    print("请输入有效的整数！")
            
            elif choice == '3':
                try:
                    start = int(input("请输入范围起点："))
                    end = int(input("请输入范围终点："))
                    if start > end:
                        print("起点必须小于等于终点！")
                        continue
                    results = bptree.range_query(start, end)
                    if results:
                        print("\n范围查询结果：")
                        for key, value in results:
                            print(f"键：{key}，值：{value}")
                    else:
                        print("\n该范围内没有数据！")
                except ValueError:
                    print("请输入有效的整数！")
            
            elif choice == '4':
                break
            
            else:
                print("无效的选择！")
        
        # 打印操作过程
        print_operations(bptree.steps)
        
    except ValueError as e:
        print(f"错误：{str(e)}") 