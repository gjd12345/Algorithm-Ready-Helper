import sys
from collections import deque, defaultdict

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def pathSum(root, targetSum):
    prefix_sum = defaultdict(int)
    prefix_sum[0] = 1
    def dfs(node, curr_sum):
        if not node:
            return 0
        curr_sum += node.val
        count = prefix_sum[curr_sum - targetSum]
        prefix_sum[curr_sum] += 1
        count += dfs(node.left, curr_sum)
        count += dfs(node.right, curr_sum)
        prefix_sum[curr_sum] -= 1
        return count
    return dfs(root, 0)

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
        targetSum = int(lines[1].strip())
        root = build_tree(nodes)
        print(pathSum(root, targetSum))
