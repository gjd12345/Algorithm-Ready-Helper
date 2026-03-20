import sys

def searchMatrix2(matrix, target):
    if not matrix:
        return False
    m, n = len(matrix), len(matrix[0])
    r, c = 0, n - 1
    while r < m and c >= 0:
        if matrix[r][c] == target:
            return True
        elif matrix[r][c] < target:
            r += 1
        else:
            c -= 1
    return False

if __name__ == "__main__":
    lines = sys.stdin.readlines()
    if lines:
        m, n, target = map(int, lines[0].strip().split())
        matrix = []
        for i in range(1, m + 1):
            matrix.append([int(x) for x in lines[i].strip().split(',')])
        print(searchMatrix2(matrix, target))
