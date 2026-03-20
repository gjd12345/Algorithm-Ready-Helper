import sys
from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def kthSmallest(root, k):
    count = 0
    ans = 0
    def dfs(node):
        nonlocal count, ans
        if not node:
            return
        dfs(node.left)
        count += 1
        if count == k:
            ans = node.val
            return
        dfs(node.right)
    dfs(root)
    return ans

def build_tree(nodes):
    if not nodes or nodes[0] == "null":
        return None
    root = TreeNode(int(nodes[0]))
    queue = deque([root])
    index = 1
    while queue and index < len(nodes):
        cur = queue.popleft()
        if index < len(nodes) and nodes[index] != "null":
            cur.left = TreeNode(int(nodes[index]))
            queue.append(cur.left)
        index += 1
        if index < len(nodes) and nodes[index] != "null":
            cur.right = TreeNode(int(nodes[index]))
            queue.append(cur.right)
        index += 1
    return root

if __name__ == "__main__":
    lines = sys.stdin.readlines()
    if len(lines) >= 2:
        nodes = lines[0].strip().split(',')
        k = int(lines[1].strip())
        root = build_tree(nodes)
        print(kthSmallest(root, k))
