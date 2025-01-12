#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现B树（B-Tree）及其基本操作。

程序分析：
1. 实现B树的基本结构
2. 实现节点分裂和合并
3. 实现插入和删除操作
4. 维护B树性质
"""

from typing import List, Optional, Tuple

class BTreeNode:
    def __init__(self, leaf: bool = True):
        self.keys = []         # 关键字列表
        self.children = []     # 子节点列表
        self.leaf = leaf      # 是否为叶节点
    
    def __str__(self):
        return f"Keys: {self.keys}"

class BTree:
    def __init__(self, t: int):
        self.root = BTreeNode()
        self.t = t  # 最小度数
        self.steps = []  # 记录操作步骤
    
    def _split_child(self, parent: BTreeNode, index: int) -> None:
        """分裂子节点"""
        t = self.t
        child = parent.children[index]
        new_node = BTreeNode(child.leaf)
        
        # 将child的后半部分keys移动到new_node
        parent.keys.insert(index, child.keys[t-1])
        new_node.keys = child.keys[t:]
        child.keys = child.keys[:t-1]
        
        # 如果不是叶节点，还需要移动children
        if not child.leaf:
            new_node.children = child.children[t:]
            child.children = child.children[:t]
        
        parent.children.insert(index + 1, new_node)
        self.steps.append((child.keys[t-1], "分裂节点"))
    
    def insert(self, key: int) -> None:
        """插入关键字"""
        root = self.root
        if len(root.keys) == 2 * self.t - 1:
            new_root = BTreeNode(False)
            self.root = new_root
            new_root.children.append(root)
            self._split_child(new_root, 0)
            self._insert_nonfull(new_root, key)
        else:
            self._insert_nonfull(root, key)
    
    def _insert_nonfull(self, node: BTreeNode, key: int) -> None:
        """在非满节点中插入关键字"""
        i = len(node.keys) - 1
        
        if node.leaf:
            # 在叶节点中插入关键字
            while i >= 0 and key < node.keys[i]:
                i -= 1
            node.keys.insert(i + 1, key)
            self.steps.append((key, "插入关键字"))
        else:
            # 在内部节点中找到合适的子节点
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            
            if len(node.children[i].keys) == 2 * self.t - 1:
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            
            self._insert_nonfull(node.children[i], key)
    
    def search(self, key: int) -> Tuple[Optional[BTreeNode], Optional[int]]:
        """搜索关键字"""
        return self._search(self.root, key)
    
    def _search(self, node: BTreeNode, key: int) -> Tuple[Optional[BTreeNode], Optional[int]]:
        """在节点中搜索关键字"""
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        
        if i < len(node.keys) and key == node.keys[i]:
            self.steps.append((key, "找到关键字"))
            return node, i
        elif node.leaf:
            self.steps.append((key, "未找到关键字"))
            return None, None
        else:
            self.steps.append((key, f"继续搜索子节点 {i}"))
            return self._search(node.children[i], key)
    
    def delete(self, key: int) -> None:
        """删除关键字"""
        self._delete(self.root, key)
        
        # 如果根节点没有关键字且不是叶节点，更新根节点
        if not self.root.keys and not self.root.leaf:
            self.root = self.root.children[0]
    
    def _delete(self, node: BTreeNode, key: int) -> None:
        """从节点中删除关键字"""
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        
        if node.leaf:
            # 在叶节点中删除关键字
            if i < len(node.keys) and node.keys[i] == key:
                node.keys.pop(i)
                self.steps.append((key, "删除关键字"))
            return
        
        if i < len(node.keys) and node.keys[i] == key:
            # 在内部节点中删除关键字
            if len(node.children[i].keys) >= self.t:
                # 从左子树找前驱
                pred = self._get_predecessor(node.children[i])
                node.keys[i] = pred
                self._delete(node.children[i], pred)
            elif len(node.children[i+1].keys) >= self.t:
                # 从右子树找后继
                succ = self._get_successor(node.children[i+1])
                node.keys[i] = succ
                self._delete(node.children[i+1], succ)
            else:
                # 合并节点
                self._merge_nodes(node, i)
                self._delete(node.children[i], key)
        else:
            # 在子节点中删除关键字
            if len(node.children[i].keys) < self.t:
                self._fill_child(node, i)
            self._delete(node.children[i], key)
    
    def _get_predecessor(self, node: BTreeNode) -> int:
        """获取前驱关键字"""
        while not node.leaf:
            node = node.children[-1]
        return node.keys[-1]
    
    def _get_successor(self, node: BTreeNode) -> int:
        """获取后继关键字"""
        while not node.leaf:
            node = node.children[0]
        return node.keys[0]
    
    def _merge_nodes(self, parent: BTreeNode, index: int) -> None:
        """合并两个子节点"""
        child = parent.children[index]
        sibling = parent.children[index + 1]
        
        # 将父节点的关键字移动到child
        child.keys.append(parent.keys.pop(index))
        
        # 将sibling的所有关键字和子节点移动到child
        child.keys.extend(sibling.keys)
        if not child.leaf:
            child.children.extend(sibling.children)
        
        # 从父节点中移除sibling
        parent.children.pop(index + 1)
        self.steps.append((index, "合并节点"))
    
    def _fill_child(self, parent: BTreeNode, index: int) -> None:
        """确保子节点至少有t个关键字"""
        if index > 0 and len(parent.children[index-1].keys) >= self.t:
            self._borrow_from_prev(parent, index)
        elif index < len(parent.children)-1 and len(parent.children[index+1].keys) >= self.t:
            self._borrow_from_next(parent, index)
        else:
            if index < len(parent.children)-1:
                self._merge_nodes(parent, index)
            else:
                self._merge_nodes(parent, index-1)
    
    def _borrow_from_prev(self, parent: BTreeNode, index: int) -> None:
        """从前一个兄弟节点借关键字"""
        child = parent.children[index]
        sibling = parent.children[index-1]
        
        # 将父节点的关键字移动到child
        child.keys.insert(0, parent.keys[index-1])
        
        # 将sibling的最后一个关键字移动到父节点
        parent.keys[index-1] = sibling.keys.pop()
        
        if not child.leaf:
            child.children.insert(0, sibling.children.pop())
        
        self.steps.append((index, "从前兄弟借关键字"))
    
    def _borrow_from_next(self, parent: BTreeNode, index: int) -> None:
        """从后一个兄弟节点借关键字"""
        child = parent.children[index]
        sibling = parent.children[index+1]
        
        # 将父节点的关键字移动到child
        child.keys.append(parent.keys[index])
        
        # 将sibling的第一个关键字移动到父节点
        parent.keys[index] = sibling.keys.pop(0)
        
        if not child.leaf:
            child.children.append(sibling.children.pop(0))
        
        self.steps.append((index, "从后兄弟借关键字"))

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if len(step) == 2:
            val, operation = step
            if operation == "插入关键字":
                print(f"{operation}：{val}")
            elif operation == "分裂节点":
                print(f"{operation}：中值 {val}")
            elif operation == "删除关键字":
                print(f"{operation}：{val}")
            elif operation == "找到关键字":
                print(f"{operation}：{val}")
            elif operation == "未找到关键字":
                print(f"{operation}：{val}")
            elif operation.startswith("继续搜索"):
                print(f"{operation}")
            else:  # 合并节点相关
                print(f"{operation}：位置 {val}")

def get_input_numbers() -> List[int]:
    """获取用户输入的数字"""
    numbers = []
    print("请输入要插入的数字（每行一个，输入非数字结束）：")
    while True:
        try:
            num = int(input())
            numbers.append(num)
        except ValueError:
            break
    return numbers

if __name__ == '__main__':
    try:
        # 创建B树（最小度数为2）
        btree = BTree(2)
        
        # 获取输入数字并插入
        numbers = get_input_numbers()
        if not numbers:
            raise ValueError("至少需要输入一个数字！")
        
        print("\n插入的数字：", numbers)
        for num in numbers:
            btree.insert(num)
        
        while True:
            print("\n请选择操作：")
            print("1. 插入数字")
            print("2. 删除数字")
            print("3. 查找数字")
            print("4. 退出")
            
            choice = input("请输入选择（1-4）：")
            
            if choice == '1':
                try:
                    num = int(input("请输入要插入的数字："))
                    btree.insert(num)
                    print("插入成功！")
                except ValueError:
                    print("请输入有效的整数！")
            
            elif choice == '2':
                try:
                    num = int(input("请输入要删除的数字："))
                    btree.delete(num)
                    print("删除成功！")
                except ValueError:
                    print("请输入有效的整数！")
            
            elif choice == '3':
                try:
                    num = int(input("请输入要查找的数字："))
                    node, pos = btree.search(num)
                    if node:
                        print(f"找到数字 {num}！")
                    else:
                        print(f"未找到数字 {num}！")
                except ValueError:
                    print("请输入有效的整数！")
            
            elif choice == '4':
                break
            
            else:
                print("无效的选择！")
        
        # 打印操作过程
        print_operations(btree.steps)
        
    except ValueError as e:
        print(f"错误：{str(e)}") 