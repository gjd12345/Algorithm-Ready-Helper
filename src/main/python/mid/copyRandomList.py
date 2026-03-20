class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random

def copyRandomList(head):
    if not head:
        return None
    mapping = {}
    cur = head
    while cur:
        mapping[cur] = Node(cur.val)
        cur = cur.next
    cur = head
    while cur:
        node = mapping[cur]
        node.next = mapping.get(cur.next)
        node.random = mapping.get(cur.random)
        cur = cur.next
    return mapping[head]
