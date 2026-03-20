import sys

def singleNumber(nums):
    if not nums:
        return 0
    k = nums[0]
    for i in range(1, len(nums)):
        k ^= nums[i]
    return k

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            nums = [int(x) for x in line.strip().split(',')]
            print(singleNumber(nums))
