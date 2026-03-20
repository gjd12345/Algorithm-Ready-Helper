import sys

def subsets(nums):
    ans = []
    path = []
    def backtrack(start):
        ans.append(list(path))
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1)
            path.pop()
    backtrack(0)
    return ans

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            nums = [int(x) for x in line.strip().split(',')]
            print(subsets(nums))
