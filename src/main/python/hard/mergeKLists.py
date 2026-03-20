"""
标题: 合并 K 个升序链表
描述: 给你一个链表数组，每个链表都已经按升序排列。请你将所有链表合并到一个升序链表中，返回合并后的链表。
"""
import sys

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def mergeKLists(lists):
    if not lists:
        return None
    return merge_range(lists, 0, len(lists) - 1)

def merge_range(lists, left, right):
    if left == right:
        return lists[left]
    mid = left + (right - left) // 2
    l = merge_range(lists, left, mid)
    r = merge_range(lists, mid + 1, right)
    return merge_two_lists(l, r)

def merge_two_lists(l, r):
    dummy = ListNode()
    cur = dummy
    while l and r:
        if l.val < r.val:
            cur.next = l
            l = l.next
        else:
            cur.next = r
            r = r.next
        cur = cur.next
    cur.next = l if l else r
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
    if lines:
        num = int(lines[0].strip())
        lists = []
        for i in range(1, num + 1):
            vals = lines[i].strip().split()
            if vals:
                lists.append(create_linked_list(vals))
        result = mergeKLists(lists)
        while result:
            print(result.val, end=" ")
            result = result.next
        print()
