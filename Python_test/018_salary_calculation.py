#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：企业发放的奖金根据利润提成。
程序分析：
请利用数轴来分界，定位。注意定义时需把奖金定义成长整型。
从键盘输入当月利润I，求应发放奖金总数？

奖金计算规则：
I≤10万元时，奖金可提10%
10万<I≤20万时，低于10万的部分按10%提成，高于10万的部分，可提成7.5%
20万<I≤40万时，高于20万元的部分，可提成5%
40万<I≤60万时，高于40万元的部分，可提成3%
60万<I≤100万时，高于60万元的部分，可提成1.5%
I>100万时，超过100万元的部分按1%提成
"""

def calculate_bonus(profit):
    """计算奖金"""
    # 设置阶梯界限和对应的提成比例
    thresholds = [1000000, 600000, 400000, 200000, 100000, 0]
    rates = [0.01, 0.015, 0.03, 0.05, 0.075, 0.1]
    
    bonus = 0
    for i in range(len(thresholds)):
        if profit > thresholds[i]:
            # 计算当前阶梯的奖金
            bonus += (profit - thresholds[i]) * rates[i]
            # 更新剩余利润
            profit = thresholds[i]
    
    return bonus

def format_currency(amount):
    """格式化货币输出"""
    return f"{amount:,.2f}"

if __name__ == '__main__':
    try:
        profit = float(input('请输入当月利润（元）：'))
        if profit < 0:
            print("利润不能为负数！")
        else:
            bonus = calculate_bonus(profit)
            print(f'利润：{format_currency(profit)}元')
            print(f'应发放奖金：{format_currency(bonus)}元')
    except ValueError:
        print("请输入有效的数字！") 