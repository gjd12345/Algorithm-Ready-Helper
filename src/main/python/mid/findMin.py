import sys

def findMin(nums):
    ans = float('inf')
    l, r = 0, len(nums) - 1
    while l <= r:
        mid = l + (r - l) // 2
        if nums[mid] <= nums[r]:
            ans = min(ans, nums[mid])
            r = mid - 1
        else:
            ans = min(ans, nums[l])
            l = mid + 1
    return ans

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            nums = [int(x) for x in line.strip().split(',')]
            print(findMin(nums))
