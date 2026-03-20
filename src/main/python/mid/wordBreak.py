import sys

def wordBreak(s, wordDict):
    word_set = set(wordDict)
    dp = [False] * (len(s) + 1)
    dp[0] = True
    for i in range(1, len(s) + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
    return dp[len(s)]

if __name__ == "__main__":
    lines = sys.stdin.readlines()
    if len(lines) >= 2:
        s = lines[0].strip()
        wordDict = lines[1].strip().split()
        print(wordBreak(s, wordDict))
