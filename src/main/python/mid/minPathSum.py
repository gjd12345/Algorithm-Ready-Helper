import sys

def minPathSum(grid):
    if not grid:
        return 0
    m, n = len(grid), len(grid[0])
    dp = [[0] * n for _ in range(m)]
    dp[0][0] = grid[0][0]
    for i in range(1, n):
        dp[0][i] = dp[0][i-1] + grid[0][i]
    for i in range(1, m):
        dp[i][0] = dp[i-1][0] + grid[i][0]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j]
    return dp[m-1][n-1]

if __name__ == "__main__":
    lines = sys.stdin.readlines()
    if len(lines) >= 2:
        m, n = map(int, lines[0].strip().split())
        grid = []
        for i in range(1, m + 1):
            grid.append([int(x) for x in lines[i].strip().split(',')])
        print(minPathSum(grid))
