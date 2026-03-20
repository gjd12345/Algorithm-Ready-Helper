import sys

def isValid(s):
    stack = []
    mapping = {")": "(", "]": "[", "}": "{"}
    for char in s:
        if char in mapping.values():
            stack.append(char)
        elif char in mapping.keys():
            if not stack or stack.pop() != mapping[char]:
                return False
        else:
            # Skip non-bracket characters if any
            continue
    return not stack

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(isValid(line.strip()))
