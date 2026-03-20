import sys

def majorityElement(nums):
    vote = 0
    ans = 0
    for num in nums:
        if vote == 0:
            ans = num
        if num == ans:
            vote += 1
        else:
            vote -= 1
    return ans

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            nums = [int(x) for x in line.strip().split(',')]
            print(majorityElement(nums))
