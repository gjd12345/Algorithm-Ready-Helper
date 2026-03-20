import sys

def largestRectangleArea(heights):
    ans = 0
    stack = [-1]
    for i in range(len(heights)):
        while stack[-1] != -1 and heights[i] <= heights[stack[-1]]:
            height = heights[stack.pop()]
            width = i - stack[-1] - 1
            ans = max(ans, height * width)
        stack.append(i)
        
    while stack[-1] != -1:
        height = heights[stack.pop()]
        width = len(heights) - stack[-1] - 1
        ans = max(ans, height * width)
    return ans

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            nums = [int(x) for x in line.strip().split(',')]
            print(largestRectangleArea(nums))
