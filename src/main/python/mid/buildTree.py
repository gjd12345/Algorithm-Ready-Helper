import sys
from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def buildTree(preorder, inorder):
    inorder_map = {val: i for i, val in enumerate(inorder)}
    def build(pb, pe, ib, ie):
        if pb > pe or ib > ie:
            return None
        root_val = preorder[pb]
        root = TreeNode(root_val)
        idx = inorder_map[root_val]
        left_size = idx - ib
        root.left = build(pb + 1, pb + left_size, ib, idx - 1)
        root.right = build(pb + left_size + 1, pe, idx + 1, ie)
        return root
    return build(0, len(preorder) - 1, 0, len(inorder) - 1)

def level_order(root):
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        result.append(node.val)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return result

if __name__ == "__main__":
    lines = sys.stdin.readlines()
    if len(lines) >= 2:
        preorder = [int(x) for x in lines[0].strip().split(',')]
        inorder = [int(x) for x in lines[1].strip().split(',')]
        root = buildTree(preorder, inorder)
        print(level_order(root))
