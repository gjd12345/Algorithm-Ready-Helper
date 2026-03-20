import sys

def search(nums, target):
    l, r = 0, len(nums) - 1
    while l <= r:
        mid = l + (r - l) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] <= nums[r]: # Right side is sorted
            if nums[mid] < target <= nums[r]:
                l = mid + 1
            else:
                r = mid - 1
        else: # Left side is sorted
            if nums[l] <= target < nums[mid]:
                r = mid - 1
            else:
                l = mid + 1
    return -1

if __name__ == "__main__":
    lines = sys.stdin.readlines()
    if len(lines) >= 2:
        nums = [int(x) for x in lines[0].strip().split(',')]
        target = int(lines[1].strip())
        print(search(nums, target))
