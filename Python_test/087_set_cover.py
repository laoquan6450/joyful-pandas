#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现集合覆盖问题的解决方案。

程序分析：
1. 实现贪心算法
2. 实现近似算法
3. 实现回溯算法
4. 优化求解过程
"""

from typing import List, Set, Dict, Tuple
from collections import defaultdict
import time

class SetCover:
    def __init__(self):
        self.steps = []  # 记录操作步骤
    
    def greedy(self, universe: Set[int], subsets: Dict[int, Set[int]]) -> List[int]:
        """贪心算法求解集合覆盖"""
        # 复制一份universe，用于跟踪未覆盖的元素
        elements = universe.copy()
        # 选中的子集索引
        selected = []
        
        # 当还有未覆盖的元素时继续选择子集
        while elements:
            # 找出能覆盖最多未覆盖元素的子集
            max_covered = 0
            best_subset = None
            
            for i, subset in subsets.items():
                covered = len(elements & subset)  # 计算交集大小
                if covered > max_covered:
                    max_covered = covered
                    best_subset = i
            
            if best_subset is None:
                break
            
            # 更新未覆盖元素集合
            elements -= subsets[best_subset]
            selected.append(best_subset)
            self.steps.append((best_subset, max_covered, "贪心选择"))
        
        return selected if not elements else []
    
    def weighted_greedy(self, universe: Set[int], subsets: Dict[int, Set[int]], 
                       weights: Dict[int, float]) -> List[int]:
        """带权重的贪心算法"""
        elements = universe.copy()
        selected = []
        
        while elements:
            # 计算每个子集的性价比（覆盖数/权重）
            max_ratio = 0
            best_subset = None
            
            for i, subset in subsets.items():
                if i not in selected:
                    covered = len(elements & subset)
                    if covered > 0:
                        ratio = covered / weights[i]
                        if ratio > max_ratio:
                            max_ratio = ratio
                            best_subset = i
            
            if best_subset is None:
                break
            
            elements -= subsets[best_subset]
            selected.append(best_subset)
            self.steps.append((best_subset, max_ratio, "权重贪心"))
        
        return selected if not elements else []
    
    def backtrack(self, universe: Set[int], subsets: Dict[int, Set[int]], 
                 max_time: float = 5.0) -> List[int]:
        """回溯算法求解（带时间限制）"""
        start_time = time.time()
        min_selected = list(subsets.keys())  # 初始解
        
        def is_covered(selected: List[int]) -> bool:
            """检查是否完全覆盖"""
            covered = set()
            for i in selected:
                covered |= subsets[i]
            return covered == universe
        
        def backtrack_util(curr_selected: List[int], remaining: List[int], depth: int):
            nonlocal min_selected
            
            # 检查时间限制
            if time.time() - start_time > max_time:
                return
            
            # 如果当前选择已经超过最优解，剪枝
            if len(curr_selected) >= len(min_selected):
                return
            
            # 检查当前选择是否是一个解
            if is_covered(curr_selected):
                min_selected = curr_selected.copy()
                self.steps.append((len(min_selected), "更新最优解"))
                return
            
            # 继续选择子集
            for i, subset_idx in enumerate(remaining):
                new_selected = curr_selected + [subset_idx]
                new_remaining = remaining[i+1:]
                backtrack_util(new_selected, new_remaining, depth + 1)
        
        # 开始回溯
        subset_indices = list(subsets.keys())
        backtrack_util([], subset_indices, 0)
        
        return min_selected if is_covered(min_selected) else []
    
    def optimize_solution(self, universe: Set[int], subsets: Dict[int, Set[int]]) -> List[int]:
        """优化的集合覆盖求解方案"""
        # 预处理：移除被其他集合完全包含的子集
        redundant = set()
        subset_items = list(subsets.items())
        
        for i, (idx1, set1) in enumerate(subset_items):
            for idx2, set2 in subset_items[i+1:]:
                if set1 <= set2:  # set1是set2的子集
                    redundant.add(idx1)
                    self.steps.append((idx1, "移除冗余子集"))
                    break
                elif set2 <= set1:  # set2是set1的子集
                    redundant.add(idx2)
                    self.steps.append((idx2, "移除冗余子集"))
        
        # 创建优化后的子集字典
        optimized_subsets = {i: s for i, s in subsets.items() if i not in redundant}
        
        # 使用贪心算法求解优化后的问题
        return self.greedy(universe, optimized_subsets)

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, step in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if len(step) == 2:
            val, operation = step
            if operation == "移除冗余子集":
                print(f"{operation}：子集 {val}")
            elif operation == "更新最优解":
                print(f"{operation}：当前大小 {val}")
        elif len(step) == 3:
            subset, value, operation = step
            if operation == "贪心选择":
                print(f"{operation}：选择子集 {subset}，覆盖 {value} 个元素")
            elif operation == "权重贪心":
                print(f"{operation}：选择子集 {subset}，性价比 {value:.2f}")

if __name__ == '__main__':
    try:
        # 创建SetCover对象
        sc = SetCover()
        
        # 获取输入
        n = int(input("请输入全集元素个数："))
        universe = set(range(n))
        
        m = int(input("请输入子集个数："))
        subsets = {}
        print("\n请输入每个子集的元素（空格分隔）：")
        for i in range(m):
            elements = set(map(int, input(f"子集 {i}: ").strip().split()))
            if elements:
                subsets[i] = elements
        
        while True:
            print("\n请选择算法：")
            print("1. 贪心算法")
            print("2. 带权重的贪心算法")
            print("3. 回溯算法")
            print("4. 优化算法")
            print("5. 退出")
            
            choice = input("请输入选择（1-5）：")
            
            if choice == '1':
                result = sc.greedy(universe, subsets)
                if result:
                    print("\n选择的子集：", result)
                    total_elements = set().union(*(subsets[i] for i in result))
                    print(f"覆盖的元素个数：{len(total_elements)}")
                else:
                    print("未找到有效解！")
            
            elif choice == '2':
                # 获取权重
                weights = {}
                print("\n请输入每个子集的权重：")
                for i in subsets:
                    weights[i] = float(input(f"子集 {i} 的权重: "))
                
                result = sc.weighted_greedy(universe, subsets, weights)
                if result:
                    print("\n选择的子集：", result)
                    total_weight = sum(weights[i] for i in result)
                    print(f"总权重：{total_weight:.2f}")
                else:
                    print("未找到有效解！")
            
            elif choice == '3':
                max_time = float(input("请输入最大运行时间（秒）："))
                result = sc.backtrack(universe, subsets, max_time)
                if result:
                    print("\n选择的子集：", result)
                    print(f"使用的子集数：{len(result)}")
                else:
                    print("未找到有效解或超时！")
            
            elif choice == '4':
                result = sc.optimize_solution(universe, subsets)
                if result:
                    print("\n选择的子集：", result)
                    total_elements = set().union(*(subsets[i] for i in result))
                    print(f"覆盖的元素个数：{len(total_elements)}")
                else:
                    print("未找到有效解！")
            
            elif choice == '5':
                break
            
            else:
                print("无效的选择！")
            
            # 打印操作过程
            print_operations(sc.steps)
            sc.steps.clear()  # 清空步骤记录
        
    except ValueError as e:
        print(f"错误：{str(e)}") 