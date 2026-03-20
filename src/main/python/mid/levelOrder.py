import sys
from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def levelOrder(root):
    if not root:
        return []
    ans = []
    queue = deque([root])
    while queue:
        level_size = len(queue)
        level_vals = []
        for _ in range(level_size):
            node = queue.popleft()
            level_vals.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        ans.append(level_vals)
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
            print(levelOrder(root))
