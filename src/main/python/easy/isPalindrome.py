import sys

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def isPalindrome(head):
    if not head or not head.next:
        return True
    
    # 1. Fast and slow pointers to find middle
    slow, fast = head, head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        
    # 2. Reverse second half
    prev = None
    curr = slow
    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node
    
    # 3. Compare two halves
    p1, p2 = head, prev
    while p2:
        if p1.val != p2.val:
            return False
        p1 = p1.next
        p2 = p2.next
    return True

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
            print(isPalindrome(head))
