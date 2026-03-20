import sys

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverseKGroup(head, k):
    count = 0
    cur = head
    while cur:
        count += 1
        cur = cur.next
    
    dummy = ListNode(0, head)
    node = dummy
    cur = head
    pre = None
    
    while count >= k:
        pre = None
        for _ in range(k):
            nxt = cur.next
            cur.next = pre
            pre = cur
            cur = nxt
        
        tail = node.next
        node.next = pre
        tail.next = cur
        node = tail
        count -= k
        
    return dummy.next

def create_linked_list(vals):
    if not vals:
        return None
    head = ListNode(int(vals[0]))
    curr = head
    for i in range(1, len(vals)):
        curr.next = ListNode(int(vals[i]))
        curr = curr.next
    return head

if __name__ == "__main__":
    lines = sys.stdin.readlines()
    if len(lines) >= 2:
        vals = lines[0].strip().split()
        k = int(lines[1].strip())
        head = create_linked_list(vals)
        result = reverseKGroup(head, k)
        while result:
            print(result.val, end=" ")
            result = result.next
        print()
