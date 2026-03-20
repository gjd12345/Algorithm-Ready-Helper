import sys

def generateParenthesis(n):
    ans = []
    def backtrack(l, r, cur):
        if l == 0 and r == 0:
            ans.append(cur)
            return
        if l > r:
            return
        if l > 0:
            backtrack(l - 1, r, cur + "(")
        if r > 0:
            backtrack(l, r - 1, cur + ")")
    backtrack(n, n, "")
    return ans

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            n = int(line.strip())
            print(generateParenthesis(n))
