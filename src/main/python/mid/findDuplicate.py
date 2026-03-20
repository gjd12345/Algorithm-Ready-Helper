import sys

def findDuplicate(nums):
    slow, fast = 0, 0
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    
    slow = 0
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    return slow

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            nums = [int(x) for x in line.strip().split(',')]
            print(findDuplicate(nums))
