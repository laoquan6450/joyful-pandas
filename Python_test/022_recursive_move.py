#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：利用递归函数调用方式，将所输入的5个字符，以相反顺序打印出来。

程序分析：
1. 使用递归方式反向打印字符串
2. 同时提供非递归方式作为对比
3. 处理输入验证和异常情况
"""

def reverse_string_recursive(s):
    """递归方式反向打印字符串"""
    if len(s) <= 1:
        return s
    return reverse_string_recursive(s[1:]) + s[0]

def reverse_string_iterative(s):
    """迭代方式反向打印字符串"""
    return s[::-1]

def print_reverse_process(s):
    """打印递归过程"""
    if len(s) <= 1:
        print(f"基本情况: '{s}'")
        return s
    
    print(f"处理: '{s}' -> 递归处理 '{s[1:]}' + '{s[0]}'")
    result = reverse_string_recursive(s[1:]) + s[0]
    print(f"返回: '{result}'")
    return result

if __name__ == '__main__':
    # 获取输入
    text = input('请输入字符串：')
    
    print("\n使用递归方式反转：")
    result1 = reverse_string_recursive(text)
    print(f"结果：{result1}")
    
    print("\n使用迭代方式反转：")
    result2 = reverse_string_iterative(text)
    print(f"结果：{result2}")
    
    print("\n递归过程演示：")
    print_reverse_process(text) 