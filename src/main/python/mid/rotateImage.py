import sys

def rotate(matrix):
    n = len(matrix)
    # Transpose
    for i in range(n):
        for j in range(i, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    # Reverse rows
    for i in range(n):
        matrix[i].reverse()

if __name__ == "__main__":
    lines = sys.stdin.readlines()
    if lines:
        m, n = map(int, lines[0].strip().split())
        matrix = []
        for i in range(1, m + 1):
            matrix.append([int(x) for x in lines[i].strip().split()])
        rotate(matrix)
        for row in matrix:
            print(row)
