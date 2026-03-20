import sys
from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

ans = 0

def diameterOfBinaryTree(root):
    global ans
    ans = 0
    dfs(root)
    return ans

def dfs(root):
    global ans
    if root is None:
        return -1
    left = dfs(root.left) + 1
    right = dfs(root.right) + 1
    ans = max(ans, left + right)
    return max(left, right)

def build_tree(s):
    if not s or s[0] == "null":
        return None
    root = TreeNode(int(s[0]))
    queue = deque([root])
    index = 1
    while queue and index < len(s):
        cur = queue.popleft()
        if index < len(s) and s[index] != "null":
            cur.left = TreeNode(int(s[index]))
            queue.append(cur.left)
        index += 1
        if index < len(s) and s[index] != "null":
            cur.right = TreeNode(int(s[index]))
            queue.append(cur.right)
        index += 1
    return root

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            s = line.strip().split(',')
            root = build_tree(s)
            print(diameterOfBinaryTree(root))
