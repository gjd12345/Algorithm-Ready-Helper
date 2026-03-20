import sys

def lengthOfLongestSubstring(s):
    l = 0
    ans = 0
    char_set = set()
    for r in range(len(s)):
        while s[r] in char_set:
            char_set.remove(s[l])
            l += 1
        char_set.add(s[r])
        ans = max(ans, r - l + 1)
    return ans

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(lengthOfLongestSubstring(line.strip()))
