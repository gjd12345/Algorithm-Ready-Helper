import sys
from collections import Counter

def minWindow(s, t):
    if len(s) < len(t):
        return ""
    
    target_counts = Counter(t)
    required = len(target_counts)
    window_counts = {}
    formed = 0
    
    l, r = 0, 0
    ans = float("inf"), None, None # length, left, right
    
    while r < len(s):
        char = s[r]
        window_counts[char] = window_counts.get(char, 0) + 1
        
        if char in target_counts and window_counts[char] == target_counts[char]:
            formed += 1
            
        while l <= r and formed == required:
            char = s[l]
            if r - l + 1 < ans[0]:
                ans = (r - l + 1, l, r)
            
            window_counts[char] -= 1
            if char in target_counts and window_counts[char] < target_counts[char]:
                formed -= 1
            l += 1
        r += 1
        
    return "" if ans[1] is None else s[ans[1]:ans[2]+1]

if __name__ == "__main__":
    lines = sys.stdin.readlines()
    if len(lines) >= 2:
        s = lines[0].strip()
        t = lines[1].strip()
        print(minWindow(s, t))
