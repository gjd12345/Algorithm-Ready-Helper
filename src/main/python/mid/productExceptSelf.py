import sys

def productExceptSelf(nums):
    n = len(nums)
    ans = [1] * n
    for i in range(1, n):
        ans[i] = ans[i-1] * nums[i-1]
    r = 1
    for i in range(n-1, -1, -1):
        ans[i] *= r
        r *= nums[i]
    return ans

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            nums = [int(x) for x in line.strip().split(',')]
            print(productExceptSelf(nums))
