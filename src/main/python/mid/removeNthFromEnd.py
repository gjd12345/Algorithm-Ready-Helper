import sys

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def removeNthFromEnd(head, n):
    dummy = ListNode(0, head)
    slow = fast = dummy
    for _ in range(n + 1):
        fast = fast.next
    while fast:
        slow = slow.next
        fast = fast.next
    slow.next = slow.next.next
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
        n = int(lines[1].strip())
        head = create_linked_list(vals)
        result = removeNthFromEnd(head, n)
        while result:
            print(result.val, end=" ")
            result = result.next
        print()
