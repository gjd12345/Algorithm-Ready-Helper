"""
标题: 岛屿数量
描述: 给你一个由 '1'（陆地）和 '0'（水）组成的二维网格，请你计算网格中岛屿的数量。
"""
import sys

def numIslands(grid):
    if not grid:
        return 0
    m, n = len(grid), len(grid[0])
    ans = 0
    def dfs(i, j):
        if i < 0 or j < 0 or i >= m or j >= n or grid[i][j] != '1':
            return
        grid[i][j] = '0'
        dfs(i-1, j)
        dfs(i+1, j)
        dfs(i, j-1)
        dfs(i, j+1)
    
    for i in range(m):
        for j in range(n):
            if grid[i][j] == '1':
                dfs(i, j)
                ans += 1
    return ans

if __name__ == "__main__":
    lines = sys.stdin.readlines()
    if lines:
        rows, cols = map(int, lines[0].strip().split())
        grid = []
        for i in range(1, rows + 1):
            grid.append(list(lines[i].strip()))
        print(numIslands(grid))
