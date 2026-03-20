import sys

def maxProduct(nums):
    if not nums:
        return 0
    max_pre = min_pre = ans = nums[0]
    for i in range(1, len(nums)):
        if nums[i] < 0:
            max_pre, min_pre = min_pre, max_pre
        max_pre = max(nums[i], max_pre * nums[i])
        min_pre = min(nums[i], min_pre * nums[i])
        ans = max(ans, max_pre)
    return ans

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            nums = [int(x) for x in line.strip().split(',')]
            print(maxProduct(nums))
