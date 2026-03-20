"""
标题: 最长回文子串
描述: 给你一个字符串 s，找到 s 中最长的回文子串。
"""
import sys

def longestPalindrome(s):
    if not s:
        return ""
    n = len(s)
    ans = ""
    for i in range(2 * n - 1):
        l = i // 2
        r = l + i % 2
        while l >= 0 and r < n and s[l] == s[r]:
            if r - l + 1 > len(ans):
                ans = s[l:r+1]
            l -= 1
            r += 1
    return ans

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(longestPalindrome(line.strip()))
