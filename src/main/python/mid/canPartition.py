import sys

def canPartition(nums):
    total_sum = sum(nums)
    if total_sum % 2 != 0:
        return False
    target = total_sum // 2
    dp = [False] * (target + 1)
    dp[0] = True
    for num in nums:
        for i in range(target, num - 1, -1):
            dp[i] = dp[i] or dp[i - num]
    return dp[target]

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            nums = [int(x) for x in line.strip().split(',')]
            print(canPartition(nums))
