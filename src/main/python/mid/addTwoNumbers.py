"""
标题: 两数相加
描述: 给你两个 非空 的链表，表示两个非负的整数。它们每位数字都是按照 逆序 的方式存储的，并且每个节点只能存储 一位 数字。请你将两个数相加，并以相同形式返回一个表示和的链表。
"""
import sys

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def addTwoNumbers(l1, l2):
    dummy = ListNode()
    cur = dummy
    carry = 0
    while l1 or l2 or carry:
        val1 = l1.val if l1 else 0
        val2 = l2.val if l2 else 0
        total = val1 + val2 + carry
        carry = total // 10
        cur.next = ListNode(total % 10)
        cur = cur.next
        if l1: l1 = l1.next
        if l2: l2 = l2.next
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
        l1 = create_linked_list(vals1)
        l2 = create_linked_list(vals2)
        result = addTwoNumbers(l1, l2)
        while result:
            print(result.val, end=" ")
            result = result.next
        print()
