#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：输入某年某月某日，判断这一天是这一年的第几天？（使用datetime模块）

程序分析：
1. 使用datetime模块处理日期
2. 计算输入日期与当年第一天的差值
3. 注意处理输入验证
"""

from datetime import datetime, date

def day_of_year_datetime(year, month, day):
    """使用datetime计算是当年的第几天"""
    try:
        # 创建输入的日期对象
        input_date = date(year, month, day)
        # 创建当年第一天的日期对象
        first_day = date(year, 1, 1)
        # 计算差值
        delta = input_date - first_day
        return delta.days + 1
    except ValueError:
        return None

if __name__ == '__main__':
    try:
        year = int(input('年：'))
        month = int(input('月：'))
        day = int(input('日：'))
        
        result = day_of_year_datetime(year, month, day)
        if result is not None:
            print(f'这是这一年的第 {result} 天')
        else:
            print('请输入有效的日期！')
    except ValueError:
        print('请输入有效的数字！') 