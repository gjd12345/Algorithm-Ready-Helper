"""
标题: 二叉树的最近公共祖先
描述: 给定一个二叉树, 找到该树中两个指定节点的最近公共祖先。
"""
import sys
from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def lowestCommonAncestor(root, p, q):
    if not root or root == p or root == q:
        return root
    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)
    if left and right:
        return root
    return left if left else right

def find_node(root, val):
    if not root or root.val == val:
        return root
    left = find_node(root.left, val)
    if left: return left
    return find_node(root.right, val)

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
    if len(lines) >= 3:
        nodes = lines[0].strip().split(',')
        p_val = int(lines[1].strip())
        q_val = int(lines[2].strip())
        root = build_tree(nodes)
        p = find_node(root, p_val)
        q = find_node(root, q_val)
        result = lowestCommonAncestor(root, p, q)
        if result:
            print(result.val)
