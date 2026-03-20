import sys

def partition(s):
    ans = []
    path = []
    def backtrack(start):
        if start == len(s):
            ans.append(list(path))
            return
        for i in range(start, len(s)):
            if is_palindrome(s, start, i):
                path.append(s[start:i+1])
                backtrack(i + 1)
                path.pop()
                
    def is_palindrome(s, l, r):
        while l < r:
            if s[l] != s[r]:
                return False
            l += 1
            r -= 1
        return True
        
    backtrack(0)
    return ans

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(partition(line.strip()))
