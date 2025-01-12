#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：输入某年某月某日，判断这一天是这一年的第几天？

程序分析：以3月5日为例，应该先把前两个月的加起来，然后再加上5天。
特殊情况，闰年且输入月份大于2时需考虑多加一天。
"""

# def is_leap_year(year):
#     return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

# def day_of_year(year, month, day):
#     # 每个月的天数（非闰年）
#     months = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
#     # 如果是闰年且超过2月，加一天
#     if is_leap_year(year) and month > 2:
#         day += 1
    
#     # 计算前面几个月的总天数
#     return sum(months[:month]) + day

# if __name__ == '__main__':
#     try:
#         year = int(input('年：'))
#         month = int(input('月：'))
#         day = int(input('日：'))
#         result = day_of_year(year, month, day)
#         print(f'这是这一年的第 {result} 天')
#     except ValueError:
#         print('请输入有效的数字！') 



# 首先定义一个函数来判断是否是闰年

# def run_yead(year):
#     return year % 4 ==0 and year % 100 != 0 or year % 400 == 0

# # 计算总得天数
# def sum_days(year,month,day):

#     # 每个月的天数
#     months = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

#     # 如果是闰年且超过2月，加一天
#     if run_yead(year) and month > 2:
#         day += 1

#     # 计算前面几个月的总天数
#     return sum(months[:month]) + day

# if __name__ == '__main__':

#     try:
#         year = int(input('年：'))
#         month = int(input('月：'))
#         day = int(input('日：'))
#         result = sum_days(year, month, day)
#         print(f'这是这一年的第 {result} 天')
#     except ValueError:
#         print('请输入有效的数字！') 



# 方法二：
year = int(input('年：'))
month = int(input('月：'))
day = int(input('日:'))

# 闰年的
months01 = [31,60,91,121,152,182,213,244,274,305,335,366]
# 非闰年的
months02 = [31,59,90,120,151,181,212,243,273,304,334,365]

if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
    print(months01[month-1]+day)
else:
    print(months02[month-1]+day)

