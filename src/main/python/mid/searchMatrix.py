import sys

def searchMatrix(matrix, target):
    if not matrix:
        return False
    m, n = len(matrix), len(matrix[0])
    l, r = 0, m * n - 1
    while l <= r:
        mid = l + (r - l) // 2
        val = matrix[mid // n][mid % n]
        if val == target:
            return True
        elif val < target:
            l = mid + 1
        else:
            r = mid - 1
    return False

if __name__ == "__main__":
    lines = sys.stdin.readlines()
    if lines:
        m, n, target = map(int, lines[0].strip().split())
        matrix = []
        for i in range(1, m + 1):
            matrix.append([int(x) for x in lines[i].strip().split(',')])
        print(searchMatrix(matrix, target))
