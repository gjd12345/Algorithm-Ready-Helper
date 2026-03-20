import sys

def longestConsecutive(nums):
    num_set = set(nums)
    longest_streak = 0
    for num in num_set:
        if num - 1 not in num_set:
            current_num = num
            current_streak = 1
            while current_num + 1 in num_set:
                current_num += 1
                current_streak += 1
            longest_streak = max(longest_streak, current_streak)
    return longest_streak

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            nums = [int(x) for x in line.strip().split(',')]
            print(longestConsecutive(nums))
