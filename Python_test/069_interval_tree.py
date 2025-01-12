#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现区间树（Interval Tree）及其基本操作。

程序分析：
1. 实现区间树的基本结构
2. 实现区间的插入和删除
3. 实现区间查询操作
4. 维护区间信息
"""

from typing import List, Optional, Tuple

class Interval:
    def __init__(self, low: int, high: int):
        self.low = low
        self.high = high
    
    def __str__(self):
        return f"[{self.low}, {self.high}]"

class IntervalNode:
    def __init__(self, interval: Interval):
        self.interval = interval
        self.max_high = interval.high
        self.left = None
        self.right = None

class IntervalTree:
    def __init__(self):
        self.root = None
        self.steps = []  # 记录操作步骤
    
    def _update_max_high(self, node: IntervalNode) -> None:
        """更新节点的最大上界"""
        node.max_high = node.interval.high
        if node.left:
            node.max_high = max(node.max_high, node.left.max_high)
        if node.right:
            node.max_high = max(node.max_high, node.right.max_high)
    
    def insert(self, interval: Interval) -> None:
        """插入区间"""
        def _insert(node: Optional[IntervalNode], interval: Interval) -> IntervalNode:
            if not node:
                self.steps.append((str(interval), "创建新节点"))
                return IntervalNode(interval)
            
            if interval.low < node.interval.low:
                node.left = _insert(node.left, interval)
            else:
                node.right = _insert(node.right, interval)
            
            self._update_max_high(node)
            self.steps.append((str(interval), str(node.interval), "更新最大上界"))
            return node
        
        self.root = _insert(self.root, interval)
    
    def search_overlapping(self, interval: Interval) -> List[Interval]:
        """查找与给定区间重叠的所有区间"""
        result = []
        
        def _overlaps(i1: Interval, i2: Interval) -> bool:
            """判断两个区间是否重叠"""
            return not (i1.high < i2.low or i1.low > i2.high)
        
        def _search(node: Optional[IntervalNode], interval: Interval) -> None:
            if not node:
                return
            
            if _overlaps(node.interval, interval):
                result.append(node.interval)
                self.steps.append((str(interval), str(node.interval), "找到重叠区间"))
            
            # 如果左子树的最大上界大于查询区间的下界，继续搜索左子树
            if node.left and node.left.max_high >= interval.low:
                _search(node.left, interval)
            
            # 如果当前节点的下界小于等于查询区间的上界，搜索右子树
            if node.right and node.interval.low <= interval.high:
                _search(node.right, interval)
        
        _search(self.root, interval)
        return result
    
    def delete(self, interval: Interval) -> None:
        """删除区间"""
        def _find_min(node: IntervalNode) -> IntervalNode:
            current = node
            while current.left:
                current = current.left
            return current
        
        def _delete(node: Optional[IntervalNode], interval: Interval) -> Optional[IntervalNode]:
            if not node:
                return None
            
            if interval.low == node.interval.low and interval.high == node.interval.high:
                self.steps.append((str(interval), "删除节点"))
                if not node.left:
                    return node.right
                elif not node.right:
                    return node.left
                
                # 有两个子节点的情况
                successor = _find_min(node.right)
                node.interval = successor.interval
                node.right = _delete(node.right, successor.interval)
            
            elif interval.low < node.interval.low:
                node.left = _delete(node.left, interval)
            else:
                node.right = _delete(node.right, interval)
            
            if node:
                self._update_max_high(node)
                self.steps.append((str(node.interval), "更新节点"))
            
            return node
        
        self.root = _delete(self.root, interval)

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if len(step) == 2:
            interval, operation = step
            if operation == "创建新节点":
                print(f"{operation}：区间 {interval}")
            elif operation == "删除节点":
                print(f"{operation}：区间 {interval}")
            else:  # 更新节点
                print(f"{operation}：区间 {interval}")
        else:  # len(step) == 3
            int1, int2, operation = step
            if operation == "找到重叠区间":
                print(f"{operation}：查询区间 {int1} 与 {int2}")
            else:  # 更新最大上界
                print(f"{operation}：插入区间 {int1} 到节点 {int2}")

def get_input_intervals() -> List[Interval]:
    """获取用户输入的区间"""
    intervals = []
    print("请输入区间（每行输入两个数表示区间的起点和终点，输入非数字结束）：")
    while True:
        try:
            line = input()
            low, high = map(int, line.split())
            if low > high:
                print("区间起点必须小于等于终点！")
                continue
            intervals.append(Interval(low, high))
        except ValueError:
            break
    return intervals

if __name__ == '__main__':
    try:
        # 创建区间树
        tree = IntervalTree()
        
        # 获取输入区间并插入
        intervals = get_input_intervals()
        if not intervals:
            raise ValueError("至少需要输入一个区间！")
        
        print("\n插入的区间：")
        for interval in intervals:
            print(interval)
            tree.insert(interval)
        
        while True:
            print("\n请选择操作：")
            print("1. 插入区间")
            print("2. 查找重叠区间")
            print("3. 删除区间")
            print("4. 退出")
            
            choice = input("请输入选择（1-4）：")
            
            if choice == '1':
                try:
                    print("请输入区间的起点和终点：")
                    low, high = map(int, input().split())
                    if low > high:
                        print("区间起点必须小于等于终点！")
                        continue
                    tree.insert(Interval(low, high))
                    print("插入成功！")
                except ValueError:
                    print("请输入有效的整数！")
            
            elif choice == '2':
                try:
                    print("请输入要查询的区间的起点和终点：")
                    low, high = map(int, input().split())
                    if low > high:
                        print("区间起点必须小于等于终点！")
                        continue
                    results = tree.search_overlapping(Interval(low, high))
                    if results:
                        print("\n找到的重叠区间：")
                        for interval in results:
                            print(interval)
                    else:
                        print("\n未找到重叠区间！")
                except ValueError:
                    print("请输入有效的整数！")
            
            elif choice == '3':
                try:
                    print("请输入要删除的区间的起点和终点：")
                    low, high = map(int, input().split())
                    if low > high:
                        print("区间起点必须小于等于终点！")
                        continue
                    tree.delete(Interval(low, high))
                    print("删除成功！")
                except ValueError:
                    print("请输入有效的整数！")
            
            elif choice == '4':
                break
            
            else:
                print("无效的选择！")
        
        # 打印操作过程
        print_operations(tree.steps)
        
    except ValueError as e:
        print(f"错误：{str(e)}") 