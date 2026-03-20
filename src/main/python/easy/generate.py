def generate(numRows):
    if numRows == 0:
        return []
    ans = [[1]]
    for i in range(1, numRows):
        prev_row = ans[-1]
        path = [1]
        for j in range(len(prev_row) - 1):
            path.append(prev_row[j] + prev_row[j + 1])
        path.append(1)
        ans.append(path)
    return ans

if __name__ == "__main__":
    import sys
    for line in sys.stdin:
        if line.strip():
            n = int(line.strip())
            print(generate(n))
