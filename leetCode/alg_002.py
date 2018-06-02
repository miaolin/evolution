"""
You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order and each of their nodes contain a single digit. Add the two numbers and return it as a linked list.

You may assume the two numbers do not contain any leading zero, except the number 0 itself.

Example

Input: (2 -> 4 -> 3) + (5 -> 6 -> 4)
Output: 7 -> 0 -> 8
Explanation: 342 + 465 = 807.
"""


# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def addTwoNumbers(self, l1, l2):
        """
        :param l1: ListNode
        :param l2: ListNode
        :return: ListNode
        """

        root = n = ListNode(0)
        accumulate = 0
        while l1 or l2 or accumulate:
            v1 = v2 = 0
            if l1 is not None:
                v1 = l1.val
                l1 = l1.next
            if l2 is not None:
                v2 = l2.val
                l2 = l2.next

            cur_value = v1 + v2 + accumulate
            if cur_value >= 10:
                cur_value -= 10
                accumulate = 1
            else:
                accumulate = 0
            n.next = ListNode(cur_value)
            n = n.next
        return root.next


if __name__ == "__main__":

    l1 = ListNode(2)
    l1.next = ListNode(4)
    l1.next.next = ListNode(3)

    l2 = ListNode(5)
    l2.next = ListNode(6)
    l2.next.next = ListNode(4)

    test = Solution()
    result_root = test.addTwoNumbers(l1, l2)

    while result_root is not None:
        print(result_root.val)
        result_root = result_root.next
