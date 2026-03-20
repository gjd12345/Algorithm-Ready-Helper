import sys
from collections import Counter

def findAnagrams(s, p):
    if len(s) < len(p):
        return []
    
    ans = []
    p_count = Counter(p)
    s_count = Counter()
    
    l = 0
    for r in range(len(s)):
        s_count[s[r]] += 1
        
        if r - l + 1 > len(p):
            if s_count[s[l]] == 1:
                del s_count[s[l]]
            else:
                s_count[s[l]] -= 1
            l += 1
            
        if s_count == p_count:
            ans.append(l)
    return ans

if __name__ == "__main__":
    lines = sys.stdin.readlines()
    if len(lines) >= 2:
        s = lines[0].strip()
        p = lines[1].strip()
        print(findAnagrams(s, p))
