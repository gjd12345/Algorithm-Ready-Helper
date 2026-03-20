import sys

def spiralOrder(matrix):
    if not matrix:
        return []
    m, n = len(matrix), len(matrix[0])
    ans = []
    l, r, t, b = 0, n - 1, 0, m - 1
    while len(ans) < m * n:
        for i in range(l, r + 1):
            ans.append(matrix[t][i])
        t += 1
        if len(ans) == m * n: break
        for i in range(t, b + 1):
            ans.append(matrix[i][r])
        r -= 1
        if len(ans) == m * n: break
        for i in range(r, l - 1, -1):
            ans.append(matrix[b][i])
        b -= 1
        if len(ans) == m * n: break
        for i in range(b, t - 1, -1):
            ans.append(matrix[i][l])
        l += 1
    return ans

if __name__ == "__main__":
    lines = sys.stdin.readlines()
    if lines:
        m, n = map(int, lines[0].strip().split())
        matrix = []
        for i in range(1, m + 1):
            matrix.append([int(x) for x in lines[i].strip().split()])
        print(spiralOrder(matrix))
