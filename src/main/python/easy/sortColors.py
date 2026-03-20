import sys

def sortColors(nums):
    n = len(nums)
    a, c, b = 0, 0, n - 1
    while c <= b:
        if nums[c] == 0:
            nums[a], nums[c] = nums[c], nums[a]
            a += 1
            c += 1
        elif nums[c] == 1:
            c += 1
        else:
            nums[c], nums[b] = nums[b], nums[c]
            b -= 1

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            nums = [int(x) for x in line.strip().split(',')]
            sortColors(nums)
            print(nums)
