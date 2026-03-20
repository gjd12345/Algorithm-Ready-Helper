import sys

def merge(intervals):
    if not intervals:
        return []
    intervals.sort(key=lambda x: x[0])
    merged = []
    for interval in intervals:
        if not merged or merged[-1][1] < interval[0]:
            merged.append(interval)
        else:
            merged[-1][1] = max(merged[-1][1], interval[1])
    return merged

if __name__ == "__main__":
    lines = sys.stdin.readlines()
    if lines:
        n = int(lines[0].strip())
        intervals = []
        for i in range(1, n + 1):
            intervals.append([int(x) for x in lines[i].split()])
        print(merge(intervals))
