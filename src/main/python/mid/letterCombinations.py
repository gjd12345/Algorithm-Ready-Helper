import sys

def letterCombinations(digits):
    if not digits:
        return []
    mapping = {
        '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
        '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
    }
    ans = []
    path = []
    def backtrack(index):
        if index == len(digits):
            ans.append("".join(path))
            return
        for char in mapping[digits[index]]:
            path.append(char)
            backtrack(index + 1)
            path.pop()
    backtrack(0)
    return ans

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(letterCombinations(line.strip()))
