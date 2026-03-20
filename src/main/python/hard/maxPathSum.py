import sys
from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

ans = float('-inf')

def maxPathSum(root):
    global ans
    ans = float('-inf')
    def dfs(node):
        global ans
        if not node:
            return 0
        left = max(0, dfs(node.left))
        right = max(0, dfs(node.right))
        ans = max(ans, node.val + left + right)
        return node.val + max(left, right)
    
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
    for line in sys.stdin:
        if line.strip():
            nodes = line.strip().split(',')
            root = build_tree(nodes)
            print(maxPathSum(root))
