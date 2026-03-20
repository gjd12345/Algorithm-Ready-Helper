import sys

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def swapPairs(head):
    dummy = ListNode(0, head)
    curr = dummy
    while curr.next and curr.next.next:
        first = curr.next
        second = curr.next.next
        first.next = second.next
        second.next = first
        curr.next = second
        curr = first
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
            result = swapPairs(head)
            while result:
                print(result.val, end=" ")
                result = result.next
            print()
