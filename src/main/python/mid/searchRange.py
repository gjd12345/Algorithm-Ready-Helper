import sys

def searchRange(nums, target):
    def find_bound(is_first):
        l, r = 0, len(nums) - 1
        res = -1
        while l <= r:
            mid = l + (r - l) // 2
            if nums[mid] == target:
                res = mid
                if is_first: r = mid - 1
                else: l = mid + 1
            elif nums[mid] < target:
                l = mid + 1
            else:
                r = mid - 1
        return res
    
    return [find_bound(True), find_bound(False)]

if __name__ == "__main__":
    lines = sys.stdin.readlines()
    if len(lines) >= 2:
        nums = [int(x) for x in lines[0].strip().split(',')]
        target = int(lines[1].strip())
        print(searchRange(nums, target))
