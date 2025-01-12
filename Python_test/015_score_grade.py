#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：利用条件运算符的嵌套来完成此题：学习成绩>=90分的同学用A表示，60-89分之间的用B表示，60分以下的用C表示。

程序分析：
1. 可以使用if-elif-else语句
2. 也可以使用条件运算符（三元运算符）
3. 需要考虑输入验证
"""

def get_grade_if_else(score):
    """使用if-elif-else语句判断成绩等级"""
    if score >= 90:
        return 'A'
    elif score >= 60:
        return 'B'
    else:
        return 'C'

def get_grade_conditional(score):
    """使用条件运算符判断成绩等级"""
    return 'A' if score >= 90 else ('B' if score >= 60 else 'C')

if __name__ == '__main__':
    try:
        score = float(input('请输入成绩：'))
        if 0 <= score <= 100:
            # 使用if-elif-else方法
            grade1 = get_grade_if_else(score)
            print(f"使用if-elif-else方法：成绩等级为 {grade1}")
            
            # 使用条件运算符方法
            grade2 = get_grade_conditional(score)
            print(f"使用条件运算符方法：成绩等级为 {grade2}")
        else:
            print("成绩必须在0-100之间！")
    except ValueError:
        print("请输入有效的数字！") 