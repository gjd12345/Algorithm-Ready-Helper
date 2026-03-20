import sys

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def sortList(head):
    if not head or not head.next:
        return head
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    temp = slow.next
    slow.next = None
    left = sortList(head)
    right = sortList(temp)
    
    dummy = ListNode()
    cur = dummy
    while left and right:
        if left.val < right.val:
            cur.next = left
            left = left.next
        else:
            cur.next = right
            right = right.next
        cur = cur.next
    cur.next = left if left else right
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
    for line in sys.stdin:
        if line.strip():
            vals = line.strip().split()
            head = create_linked_list(vals)
            result = sortList(head)
            while result:
                print(result.val, end=" ")
                result = result.next
            print()
