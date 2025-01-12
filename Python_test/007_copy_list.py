#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：将一个列表的数据复制到另一个列表中。

程序分析：使用切片操作、列表推导式、copy模块等多种方法。
"""

import copy

def copy_list_demo():
    # 原始列表
    original = [1, [2, 3], {'a': 4}]
    
    # 方法1：切片操作（浅拷贝）
    copy1 = original[:]
    
    # 方法2：list()函数（浅拷贝）
    copy2 = list(original)
    
    # 方法3：copy方法（浅拷贝）
    copy3 = original.copy()
    
    # 方法4：copy模块的copy方法（浅拷贝）
    copy4 = copy.copy(original)
    
    # 方法5：copy模块的deepcopy方法（深拷贝）
    copy5 = copy.deepcopy(original)
    
    # 测试浅拷贝和深拷贝的区别
    print("原始列表:", original)
    
    # 修改嵌套列表
    original[1][0] = 'X'
    
    print("\n修改后：")
    print("原始列表:", original)
    print("切片拷贝:", copy1)
    print("list()拷贝:", copy2)
    print("copy()方法:", copy3)
    print("copy模块浅拷贝:", copy4)
    print("深拷贝:", copy5)

if __name__ == '__main__':
    copy_list_demo() 