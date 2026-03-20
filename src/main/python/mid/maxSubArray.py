import sys

def maxSubArray(nums):
    ans = float('-inf')
    pre = 0
    for num in nums:
        pre = max(pre + num, num)
        ans = max(ans, pre)
    return ans

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            nums = [int(x) for x in line.strip().split(',')]
            print(maxSubArray(nums))
