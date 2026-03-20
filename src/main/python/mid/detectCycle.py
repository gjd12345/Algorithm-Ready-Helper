import sys

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def detectCycle(head):
    if not head or not head.next:
        return None
    slow, fast = head, head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            curr = head
            while slow != curr:
                slow = slow.next
                curr = curr.next
            return slow
    return None

def create_linked_list_with_cycle(vals, pos):
    if not vals:
        return None
    nodes = [ListNode(int(v)) for v in vals]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i+1]
    if pos != -1 and pos < len(nodes):
        nodes[-1].next = nodes[pos]
    return nodes[0]

if __name__ == "__main__":
    lines = sys.stdin.readlines()
    if len(lines) >= 2:
        vals = lines[0].strip().split()
        pos = int(lines[1].strip())
        head = create_linked_list_with_cycle(vals, pos)
        result = detectCycle(head)
        if result:
            print(result.val)
        else:
            print("null")
