import sys
from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def sortedArrayToBST(nums):
    def build_bst(l, r):
        if l > r:
            return None
        mid = l + (r - l) // 2
        root = TreeNode(nums[mid])
        root.left = build_bst(l, mid - 1)
        root.right = build_bst(mid + 1, r)
        return root
    return build_bst(0, len(nums) - 1)

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
    for line in sys.stdin:
        if line.strip():
            nums = [int(x) for x in line.strip().split(',')]
            root = sortedArrayToBST(nums)
            print(level_order(root))
