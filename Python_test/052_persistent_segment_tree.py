#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现可持久化线段树及其基本操作。

程序分析：
1. 实现可持久化线段树的节点结构
2. 实现历史版本的保存和查询
3. 实现区间查询和单点修改
4. 处理历史版本的区间查询问题
"""

class Node:
    def __init__(self, left=None, right=None, val=0):
        self.left = left    # 左子节点
        self.right = right  # 右子节点
        self.val = val      # 节点值
        
class PersistentSegmentTree:
    def __init__(self, arr):
        self.arr = arr
        self.n = len(arr)
        self.roots = []  # 存储所有历史版本的根节点
        self.steps = []  # 记录操作步骤
        self.roots.append(self._build(0, self.n - 1))
    
    def _build(self, left: int, right: int) -> Node:
        """构建线段树"""
        node = Node()
        if left == right:
            node.val = self.arr[left]
            self.steps.append((left, node.val, "创建叶节点"))
            return node
        
        mid = (left + right) // 2
        node.left = self._build(left, mid)
        node.right = self._build(mid + 1, right)
        node.val = node.left.val + node.right.val
        self.steps.append((left, right, node.val, "合并节点"))
        return node
    
    def _update(self, node: Node, left: int, right: int, pos: int, val: int) -> Node:
        """创建新版本并更新节点"""
        new_node = Node()
        if left == right:
            new_node.val = val
            self.steps.append((pos, val, "更新叶节点"))
            return new_node
        
        mid = (left + right) // 2
        if pos <= mid:
            new_node.left = self._update(node.left, left, mid, pos, val)
            new_node.right = node.right
        else:
            new_node.left = node.left
            new_node.right = self._update(node.right, mid + 1, right, pos, val)
        
        new_node.val = new_node.left.val + new_node.right.val
        self.steps.append((left, right, new_node.val, "更新父节点"))
        return new_node
    
    def update(self, version: int, pos: int, val: int) -> int:
        """创建新版本并更新值"""
        self.roots.append(self._update(self.roots[version], 0, self.n - 1, pos, val))
        return len(self.roots) - 1
    
    def _query(self, node: Node, left: int, right: int, ql: int, qr: int) -> int:
        """查询区间和"""
        if ql <= left and right <= qr:
            self.steps.append((left, right, node.val, "完全包含"))
            return node.val
        
        mid = (left + right) // 2
        result = 0
        
        if ql <= mid:
            result += self._query(node.left, left, mid, ql, qr)
        if qr > mid:
            result += self._query(node.right, mid + 1, right, ql, qr)
            
        self.steps.append((ql, qr, result, "部分查询"))
        return result
    
    def query(self, version: int, left: int, right: int) -> int:
        """查询特定版本的区间和"""
        return self._query(self.roots[version], 0, self.n - 1, left, right)

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if len(step) == 3:
            pos, val, op = step
            print(f"{op}：位置 {pos}，值 {val}")
        else:
            left, right, val, op = step
            print(f"{op}：区间 [{left}, {right}]，值 {val}")

def get_input_numbers():
    """获取用户输入的数字"""
    numbers = []
    print("请输入5个数字：")
    while len(numbers) < 5:
        try:
            num = int(input(f"请输入第{len(numbers)+1}个数字："))
            numbers.append(num)
        except ValueError:
            print("请输入有效的整数！")
    return numbers

if __name__ == '__main__':
    try:
        # 获取输入数组
        numbers = get_input_numbers()
        print(f"\n原始数组：{numbers}")
        
        # 创建可持久化线段树
        pst = PersistentSegmentTree(numbers)
        
        while True:
            print("\n请选择操作：")
            print("1. 更新某个位置的值（创建新版本）")
            print("2. 查询某个版本的区间和")
            print("3. 退出")
            
            choice = input("请输入选择（1-3）：")
            
            if choice == '1':
                version = int(input("请输入要基于的版本号（从0开始）："))
                pos = int(input("请输入要更新的位置（0-4）："))
                val = int(input("请输入新的值："))
                new_version = pst.update(version, pos, val)
                print(f"创建了新版本：{new_version}")
            
            elif choice == '2':
                version = int(input("请输入要查询的版本号："))
                left = int(input("请输入区间左端点（0-4）："))
                right = int(input("请输入区间右端点（0-4）："))
                result = pst.query(version, left, right)
                print(f"区间和为：{result}")
            
            elif choice == '3':
                break
            
            else:
                print("无效的选择！")
        
        # 打印操作过程
        print_operations(pst.steps)
        
    except ValueError as e:
        print(f"错误：{str(e)}") 