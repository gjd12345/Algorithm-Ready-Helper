"""
标题: 接雨水
描述: 给定 n 个非负整数表示每个宽度为 1 的柱子的高度图，计算按此排列的柱子，下雨之后能接多少雨水。
"""
import sys

def trap(height):
    n = len(height)
    if n <= 2:
        return 0
    ans = 0
    l_max, r_max = height[0], height[n-1]
    l, r = 1, n - 2
    while l <= r:
        l_max = max(l_max, height[l])
        r_max = max(r_max, height[r])
        if l_max < r_max:
            ans += l_max - height[l]
            l += 1
        else:
            ans += r_max - height[r]
            r -= 1
    return ans

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            nums = [int(x) for x in line.strip().split(',')]
            print(trap(nums))
