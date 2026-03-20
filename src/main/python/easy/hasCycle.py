import sys

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def hasCycle(head):
    if not head or not head.next:
        return False
    slow = head
    fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False

if __name__ == "__main__":
    lines = sys.stdin.readlines()
    if len(lines) >= 2:
        nodes_vals = lines[0].strip().split()
        pos = int(lines[1].strip())
        
        if not nodes_vals:
            print(False)
            sys.exit()
            
        head = ListNode(int(nodes_vals[0]))
        curr = head
        nodes = [head]
        for i in range(1, len(nodes_vals)):
            curr.next = ListNode(int(nodes_vals[i]))
            curr = curr.next
            nodes.append(curr)
            
        if pos != -1 and pos < len(nodes):
            curr.next = nodes[pos]
            
        print(hasCycle(head))
