import sys

def maxProfit(prices):
    if not prices:
        return 0
    ans = 0
    pre = prices[0]
    for price in prices:
        pre = min(pre, price)
        ans = max(ans, price - pre)
    return ans

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            nums = [int(x) for x in line.strip().split(',')]
            print(maxProfit(nums))
