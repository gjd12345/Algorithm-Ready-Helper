import sys

def combinationSum(candidates, target):
    ans = []
    path = []
    def backtrack(begin, current_sum):
        if current_sum == target:
            ans.append(list(path))
            return
        if current_sum > target:
            return
        for i in range(begin, len(candidates)):
            path.append(candidates[i])
            backtrack(i, current_sum + candidates[i])
            path.pop()
    
    backtrack(0, 0)
    return ans

if __name__ == "__main__":
    lines = sys.stdin.readlines()
    if len(lines) >= 2:
        nums = [int(x) for x in lines[0].strip().split(',')]
        target = int(lines[1].strip())
        print(combinationSum(nums, target))
