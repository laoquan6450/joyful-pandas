#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：暂停一秒输出，并格式化当前时间。

程序分析：使用 time 模块的 sleep 函数实现暂停，strftime 函数格式化时间。
"""

import time

def time_delay_demo():
    # 循环输出当前时间，每次暂停1秒
    for i in range(3):  # 演示3次
        # 获取当前时间并格式化
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        print(current_time)
        
        # 暂停1秒
        time.sleep(1)

if __name__ == '__main__':
    print("开始演示时间延迟...")
    time_delay_demo()
    print("演示结束") 