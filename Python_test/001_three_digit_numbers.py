#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：有四个数字：1、2、3、4，能组成多少个互不相同且无重复数字的三位数？各是多少？

程序分析：可填在百位、十位、个位的数字都是1、2、3、4。组成所有的排列后再去掉不满足条件的排列。
"""

# def find_three_digit_numbers():
#     count = 0
#     numbers = []
#     for i in range(1, 5):
#         for j in range(1, 5):
#             for k in range(1, 5):
#                 # 确保三个数字互不相同
#                 if (i != j) and (j != k) and (k != i):
#                     num = i * 100 + j * 10 + k
#                     numbers.append(num)
#                     count += 1
#     return count, numbers

# if __name__ == '__main__':
#     count, numbers = find_three_digit_numbers()
#     print(f"总数量：{count}")
#     print(f"所有三位数：{numbers}") 


# # 方法二：
# #!/usr/bin/python
# # -*- coding: UTF-8 -*-

# # 原答案没有指出三位数的数量，添加无重复三位数的数量

# d=[]
# for a in range(1,5):
#     for b in range(1,5):
#         for c in range(1,5):
#             if (a!=b) and (a!=c) and (c!=b):
#                 d.append([a,b,c])
# print ("总数量：", len(d))
# print (d)



# # 方法三：
# for i in range(1,5):
#     for j in range(1,5):
#         if i == j:
#             continue
#         for k in range(1,5):
#             if i == k or j == k:
#                 continue
#             print (i,j,k)


# 方法四：

def find_three_numbers():
    count = 0
    num = []
    for i in range(1,5):
        for j in range(1,5):
            for k in range(1,5):
                if i != j and i != k and j != k:
                    num.append(i*100+j*10+k)
                    count = count +1
    return count,num

if __name__ == '__main__':
    count,num = find_three_numbers()
    print(f"总数量:{count}")
    print(f"所有三位数:{num}")


# 方法五：

#!/usr/bin/env python
#-*- coding:utf-8 -*-

#用集合去除重复元素
import pprint

list_num=['1','2','3','4']
list_result=[]
for i in list_num:
    for j in list_num:
        for k in list_num:
            if len(set(i+j+k))==3:
                list_result+=[int(i+j+k)]
print("能组成%d个互不相同且无重复数字的三位数: "%len(list_result))
print(list_result)


s = set('aab')
print(s)
print(len(s))

