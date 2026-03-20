"""
标题: 两数之和
描述: 给定一个整数数组 nums 和一个整数目标值 target，请你在该数组中找出 和为目标值 target 的那 两个 整数，并返回它们的数组下标。
"""
import sys

def twoSum(nums, target):
    mapping = {}
    for i, num in enumerate(nums):
        if target - num in mapping:
            return [mapping[target - num], i]
        mapping[num] = i
    return [-1, -1]

if __name__ == "__main__":
    lines = sys.stdin.readlines()
    if len(lines) >= 2:
        nums = [int(x) for x in lines[0].strip().split()]
        target = int(lines[1].strip())
        print(twoSum(nums, target))
