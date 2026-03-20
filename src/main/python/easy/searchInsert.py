import sys

def searchInsert(nums, target):
    l, r = 0, len(nums) - 1
    while l <= r:
        mid = l + (r - l) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] > target:
            r = mid - 1
        else:
            l = mid + 1
    return l

if __name__ == "__main__":
    lines = sys.stdin.readlines()
    if len(lines) >= 2:
        nums = [int(x) for x in lines[0].strip().split(',')]
        target = int(lines[1].strip())
        print(searchInsert(nums, target))
