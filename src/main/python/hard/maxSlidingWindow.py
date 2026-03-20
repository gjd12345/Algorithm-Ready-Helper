import sys
from collections import deque

def maxSlidingWindow(nums, k):
    if not nums:
        return []
    ans = []
    dq = deque()
    for i in range(len(nums)):
        # Remove indices out of window
        if dq and dq[0] < i - k + 1:
            dq.popleft()
        # Remove smaller elements from back
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()
        dq.append(i)
        # Add to answer if window is complete
        if i >= k - 1:
            ans.append(nums[dq[0]])
    return ans

if __name__ == "__main__":
    lines = sys.stdin.readlines()
    if len(lines) >= 2:
        line1 = lines[0].strip()
        k = int(lines[1].strip())
        nums = [int(x) for x in line1.split(',')]
        print(maxSlidingWindow(nums, k))
