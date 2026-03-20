import sys

def uniquePaths(m, n):
    dp = [[1] * n for _ in range(m)]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i-1][j] + dp[i][j-1]
    return dp[m-1][n-1]

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            m, n = map(int, line.strip().split())
            print(uniquePaths(m, n))
