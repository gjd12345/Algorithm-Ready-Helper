import sys

def canJump(nums):
    max_position = 0
    for i, num in enumerate(nums):
        if i > max_position:
            return False
        max_position = max(max_position, i + num)
        if max_position >= len(nums) - 1:
            return True
    return False

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            nums = [int(x) for x in line.strip().split(',')]
            print(canJump(nums))
