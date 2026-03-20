import sys
from collections import defaultdict

def subarraySum(nums, k):
    prefix_sum = defaultdict(int)
    prefix_sum[0] = 1
    ans = 0
    curr_sum = 0
    for num in nums:
        curr_sum += num
        ans += prefix_sum[curr_sum - k]
        prefix_sum[curr_sum] += 1
    return ans

if __name__ == "__main__":
    lines = sys.stdin.readlines()
    if len(lines) >= 2:
        nums = [int(x) for x in lines[0].strip().split(',')]
        k = int(lines[1].strip())
        print(subarraySum(nums, k))
