#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：企业发放的奖金根据利润提成。

利润(I)低于或等于10万元时，奖金可提10%；
利润高于10万元，低于20万元时，低于10万元的部分按10%提成，高于10万元的部分，可提成7.5%；
20万到40万之间时，高于20万元的部分，可提成5%；
40万到60万之间时高于40万元的部分，可提成3%；
60万到100万之间时，高于60万元的部分，可提成1.5%；
高于100万元时，超过100万元的部分按1%提成。
从键盘输入当月利润I，求应发放奖金总数？
"""

# def calculate_bonus(profit):
#     thresholds = [1000000, 600000, 400000, 200000, 100000, 0]
#     rates = [0.01, 0.015, 0.03, 0.05, 0.075, 0.1]
#     bonus = 0
#     for i in range(len(thresholds)):
#         if profit > thresholds[i]:
#             bonus += (profit - thresholds[i]) * rates[i]
#             profit = thresholds[i]
#     return bonus

# if __name__ == '__main__':
#     try:
#         profit = int(input('请输入当月利润（元）：'))
#         bonus = calculate_bonus(profit)
#         print(f'应发放奖金总数为：{bonus:.2f}元')
#     except ValueError:
#         print('请输入有效的数字！') 


# 方法二：



def sum_bonus(num):

    if num <= 100000:
        bonus = num * 0.1
    elif num <= 200000:
        bonus = 100000 * 0.1 + (num -100000) * 0.075
    elif num <= 400000:
        bonus = 100000 * 0.1 + 100000 * 0.075 + (num - 200000) * 0.05
    elif num <= 600000:
        bonus = 100000 * 0.1 + 100000 * 0.075 + 200000 * 0.05 + (num - 400000) * 0.03
    elif num <= 1000000:
        bonus = 100000 * 0.1 + 100000 * 0.075 + 200000 * 0.05 + 200000 * 0.03 + (num - 600000) * 0.015
    else:
        bonus = 100000 * 0.1 + 100000 * 0.075 + 200000 * 0.05 + 200000 * 0.03 + 400000 * 0.015 + (num - 1000000) * 0.01

    return bonus

if __name__ == '__main__':
    num = int(input('请输入利润：'))
    bonus = sum_bonus(num)
    print(f'应发放奖金总数为：{bonus:.2f}元')

