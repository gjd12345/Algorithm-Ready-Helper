import sys

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def mergeTwoLists(list1, list2):
    dummy = ListNode()
    cur = dummy
    while list1 and list2:
        if list1.val < list2.val:
            cur.next = list1
            list1 = list1.next
        else:
            cur.next = list2
            list2 = list2.next
        cur = cur.next
    cur.next = list1 if list1 else list2
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
        vals1 = lines[0].strip().split()
        vals2 = lines[1].strip().split()
        
        list1 = create_linked_list(vals1)
        list2 = create_linked_list(vals2)
        
        result = mergeTwoLists(list1, list2)
        curr = result
        while curr:
            print(curr.val, end=" ")
            curr = curr.next
        print()
