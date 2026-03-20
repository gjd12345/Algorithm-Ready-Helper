import sys

def permute(nums):
    ans = []
    path = []
    used = [False] * len(nums)
    def backtrack():
        if len(path) == len(nums):
            ans.append(list(path))
            return
        for i in range(len(nums)):
            if not used[i]:
                used[i] = True
                path.append(nums[i])
                backtrack()
                path.pop()
                used[i] = False
    backtrack()
    return ans

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            nums = [int(x) for x in line.strip().split(',')]
            print(permute(nums))
