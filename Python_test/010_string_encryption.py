#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：对字符串进行简单的加密。

程序分析：
1. 对每个字符的ASCII码进行操作
2. 提供加密和解密两个功能
3. 可以指定偏移量
"""

def encrypt(text, offset=3):
    """
    加密字符串
    :param text: 原始字符串
    :param offset: 偏移量，默认为3
    :return: 加密后的字符串
    """
    result = ''
    for char in text:
        if char.isalpha():
            # 处理字母
            ascii_offset = ord('A') if char.isupper() else ord('a')
            # 计算新的字符位置并确保在字母范围内
            new_pos = (ord(char) - ascii_offset + offset) % 26
            result += chr(ascii_offset + new_pos)
        else:
            # 非字母字符保持不变
            result += char
    return result

def decrypt(text, offset=3):
    """
    解密字符串
    :param text: 加密后的字符串
    :param offset: 偏移量，默认为3
    :return: 解密后的字符串
    """
    return encrypt(text, -offset)

if __name__ == '__main__':
    # 测试加密解密功能
    original_text = "Hello, World! 123"
    print(f"原始字符串: {original_text}")
    
    # 加密
    encrypted_text = encrypt(original_text)
    print(f"加密后: {encrypted_text}")
    
    # 解密
    decrypted_text = decrypt(encrypted_text)
    print(f"解密后: {decrypted_text}")
    
    # 测试不同偏移量
    offset = 5
    print(f"\n使用偏移量 {offset}:")
    encrypted_text = encrypt(original_text, offset)
    print(f"加密后: {encrypted_text}")
    decrypted_text = decrypt(encrypted_text, offset)
    print(f"解密后: {decrypted_text}") 