import sys

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverseList(head):
    prev = None
    curr = head
    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node
    return prev

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            vals = line.strip().split()
            if not vals:
                continue
            head = ListNode(int(vals[0]))
            curr = head
            for i in range(1, len(vals)):
                curr.next = ListNode(int(vals[i]))
                curr = curr.next
            
            rev_head = reverseList(head)
            while rev_head:
                print(rev_head.val)
                rev_head = rev_head.next
