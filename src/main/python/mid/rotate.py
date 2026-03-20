import sys

def rotate(nums, k):
    n = len(nums)
    k %= n
    def reverse(l, r):
        while l < r:
            nums[l], nums[r] = nums[r], nums[l]
            l += 1
            r -= 1
    reverse(0, n - 1)
    reverse(0, k - 1)
    reverse(k, n - 1)

if __name__ == "__main__":
    lines = sys.stdin.readlines()
    if len(lines) >= 2:
        nums = [int(x) for x in lines[0].strip().split(',')]
        k = int(lines[1].strip())
        rotate(nums, k)
        print(nums)
