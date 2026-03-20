import sys

def partitionLabels(s):
    last_pos = {char: i for i, char in enumerate(s)}
    ans = []
    start = end = 0
    for i, char in enumerate(s):
        end = max(end, last_pos[char])
        if i == end:
            ans.append(end - start + 1)
            start = i + 1
    return ans

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(partitionLabels(line.strip()))
