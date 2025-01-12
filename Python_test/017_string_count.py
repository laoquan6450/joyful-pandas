#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：输入一行字符，分别统计出其中英文字母、空格、数字和其它字符的个数。

程序分析：
1. 利用字符串的各种判断方法
2. 也可以使用正则表达式
3. 需要考虑Unicode字符
"""

import re

def count_chars_method1(text):
    """使用字符串方法统计"""
    letters = sum(c.isalpha() for c in text)
    spaces = sum(c.isspace() for c in text)
    digits = sum(c.isdigit() for c in text)
    others = len(text) - letters - spaces - digits
    return letters, spaces, digits, others

def count_chars_method2(text):
    """使用正则表达式统计"""
    letters = len(re.findall(r'[a-zA-Z]', text))
    spaces = len(re.findall(r'\s', text))
    digits = len(re.findall(r'\d', text))
    others = len(text) - letters - spaces - digits
    return letters, spaces, digits, others

if __name__ == '__main__':
    text = input('请输入一行字符：')
    
    # 使用字符串方法
    letters1, spaces1, digits1, others1 = count_chars_method1(text)
    print('\n使用字符串方法统计结果：')
    print(f'英文字母：{letters1}')
    print(f'空格：{spaces1}')
    print(f'数字：{digits1}')
    print(f'其他字符：{others1}')
    
    # 使用正则表达式
    letters2, spaces2, digits2, others2 = count_chars_method2(text)
    print('\n使用正则表达式统计结果：')
    print(f'英文字母：{letters2}')
    print(f'空格：{spaces2}')
    print(f'数字：{digits2}')
    print(f'其他字符：{others2}') 