"""
标题: 字母异位词分组
描述: 给你一个字符串数组，请你将 字母异位词 组合在一起。可以按任意顺序返回结果列表。
"""
import sys
from collections import defaultdict

def groupAnagrams(strs):
    mapping = defaultdict(list)
    for s in strs:
        key = "".join(sorted(s))
        mapping[key].append(s)
    return list(mapping.values())

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            strs = line.strip().split()
            print(groupAnagrams(strs))
