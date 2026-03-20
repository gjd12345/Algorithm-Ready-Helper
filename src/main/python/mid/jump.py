import sys

def jump(nums):
    ans = 0
    end = 0
    max_step = 0
    for i in range(len(nums) - 1):
        max_step = max(max_step, i + nums[i])
        if i == end:
            ans += 1
            end = max_step
    return ans

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            nums = [int(x) for x in line.strip().split(',')]
            print(jump(nums))
