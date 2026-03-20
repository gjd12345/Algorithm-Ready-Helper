import sys
from collections import deque

def orangesRotting(grid):
    if not grid:
        return 0
    m, n = len(grid), len(grid[0])
    queue = deque()
    fresh = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 2:
                queue.append((i, j))
            elif grid[i][j] == 1:
                fresh += 1
    if fresh == 0:
        return 0
    
    time = 0
    while queue and fresh > 0:
        time += 1
        for _ in range(len(queue)):
            r, c = queue.popleft()
            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    queue.append((nr, nc))
    return time if fresh == 0 else -1

if __name__ == "__main__":
    lines = sys.stdin.readlines()
    if lines:
        m, n = map(int, lines[0].strip().split())
        grid = []
        for i in range(1, m + 1):
            grid.append([int(x) for x in list(lines[i].strip())])
        print(orangesRotting(grid))
