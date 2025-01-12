#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
题目：实现基于数组的字典树（Trie Array）及其基本操作。

程序分析：
1. 使用数组实现字典树节点
2. 实现插入和查找操作
3. 实现前缀匹配功能
4. 优化空间使用
"""

class TrieArray:
    def __init__(self, max_nodes=100000):
        self.max_nodes = max_nodes
        self.nodes = [[0] * 26 for _ in range(max_nodes)]  # 子节点数组
        self.is_end = [False] * max_nodes  # 标记单词结束
        self.count = [0] * max_nodes  # 记录单词出现次数
        self.size = 1  # 当前节点数量
        self.steps = []  # 记录操作步骤
    
    def _char_to_index(self, char: str) -> int:
        """将字符转换为索引"""
        return ord(char.lower()) - ord('a')
    
    def insert(self, word: str) -> None:
        """插入单词"""
        current = 0  # 从根节点开始
        
        for char in word:
            index = self._char_to_index(char)
            if self.nodes[current][index] == 0:
                if self.size >= self.max_nodes:
                    raise OverflowError("字典树节点数量超出限制")
                self.nodes[current][index] = self.size
                self.steps.append((char, current, self.size, "创建新节点"))
                self.size += 1
            current = self.nodes[current][index]
            self.steps.append((char, current, -1, "移动到下一节点"))
        
        self.is_end[current] = True
        self.count[current] += 1
        self.steps.append((word, current, self.count[current], "标记单词结束"))
    
    def search(self, word: str) -> bool:
        """查找单词"""
        current = 0
        
        for char in word:
            index = self._char_to_index(char)
            if self.nodes[current][index] == 0:
                self.steps.append((char, current, -1, "查找失败"))
                return False
            current = self.nodes[current][index]
            self.steps.append((char, current, -1, "查找下一节点"))
        
        if self.is_end[current]:
            self.steps.append((word, current, self.count[current], "找到单词"))
            return True
        
        self.steps.append((word, current, -1, "未找到完整单词"))
        return False
    
    def starts_with(self, prefix: str) -> bool:
        """查找前缀"""
        current = 0
        
        for char in prefix:
            index = self._char_to_index(char)
            if self.nodes[current][index] == 0:
                self.steps.append((char, current, -1, "前缀查找失败"))
                return False
            current = self.nodes[current][index]
            self.steps.append((char, current, -1, "前缀查找继续"))
        
        self.steps.append((prefix, current, -1, "找到前缀"))
        return True

def print_operations(steps):
    """打印操作过程"""
    print("\n操作过程：")
    for i, (text, node, value, operation) in enumerate(steps, 1):
        print(f"\n第{i}步：")
        if operation == "创建新节点":
            print(f"{operation}：字符 '{text}'，从节点 {node} 到节点 {value}")
        elif operation == "移动到下一节点":
            print(f"{operation}：字符 '{text}'，当前节点 {node}")
        elif operation == "标记单词结束":
            print(f"{operation}：单词 '{text}'，出现次数 {value}")
        elif operation.startswith("查找"):
            if value == -1:
                print(f"{operation}：字符 '{text}'，当前节点 {node}")
            else:
                print(f"{operation}：单词 '{text}'，出现次数 {value}")
        else:  # 前缀查找
            print(f"{operation}：'{text}'，当前节点 {node}")

def get_input_words():
    """获取用户输入的单词"""
    words = []
    print("请输入5个不同的单词（仅包含小写字母）：")
    while len(words) < 5:
        try:
            word = input(f"请输入第{len(words)+1}个单词：").strip().lower()
            if not word.isalpha():
                print("请只输入字母！")
                continue
            if word in words:
                print("该单词已存在，请输入不同的单词！")
                continue
            words.append(word)
        except ValueError:
            print("输入无效！")
    return words

if __name__ == '__main__':
    try:
        # 创建字典树
        trie = TrieArray()
        
        # 获取输入单词并插入
        words = get_input_words()
        print(f"\n插入的单词：{words}")
        for word in words:
            trie.insert(word)
        
        while True:
            print("\n请选择操作：")
            print("1. 插入单词")
            print("2. 查找单词")
            print("3. 查找前缀")
            print("4. 退出")
            
            choice = input("请输入选择（1-4）：")
            
            if choice == '1':
                word = input("请输入要插入的单词：").strip().lower()
                if word.isalpha():
                    trie.insert(word)
                    print("插入成功！")
                else:
                    print("请只输入字母！")
            
            elif choice == '2':
                word = input("请输入要查找的单词：").strip().lower()
                if word.isalpha():
                    found = trie.search(word)
                    print("找到单词！" if found else "未找到单词！")
                else:
                    print("请只输入字母！")
            
            elif choice == '3':
                prefix = input("请输入要查找的前缀：").strip().lower()
                if prefix.isalpha():
                    found = trie.starts_with(prefix)
                    print("找到前缀！" if found else "未找到前缀！")
                else:
                    print("请只输入字母！")
            
            elif choice == '4':
                break
            
            else:
                print("无效的选择！")
        
        # 打印操作过程
        print_operations(trie.steps)
        
    except (ValueError, OverflowError) as e:
        print(f"错误：{str(e)}") 