"""
There are two sorted arrays nums1 and nums2 of size m and n respectively.

Find the median of the two sorted arrays. The overall run time complexity should be O(log (m+n)).

Example 1:
nums1 = [1, 3]
nums2 = [2]

The median is 2.0
Example 2:
nums1 = [1, 2]
nums2 = [3, 4]

The median is (2 + 3)/2 = 2.5
"""


class Solution:
    def findMedianSortedArrays(self, nums1, nums2):
        sum_l = len(nums1) + len(nums2)
        if sum_l % 2 == 1:
            return self.findKth(nums1, nums2, sum_l//2)
        else:
            return (self.findKth(nums1, nums2, sum_l//2 - 1) + self.findKth(nums1, nums2, sum_l//2)) / 2.0

    def findKth(self, A, B, k):
        # A is always the shorter one
        if len(A) > len(B):
            A, B = B, A

        if not A:
            return B[k]

        if k == (len(A) + len(B) - 1):
            return max(A[-1], B[-1])

        i = len(A) // 2
        j = k - i
        if A[i] > B[j]:
            return self.findKth(A[:i], B[j:], i)
        else:
            return self.findKth(A[i:], B[:j], j)


if __name__ == "__main__":

    test = Solution()

    nums1 = [1, 3]
    nums2 = [2]
    print(test.findMedianSortedArrays(nums1, nums2))

    nums1 = [1, 2]
    nums2 = [3, 4]
    print(test.findMedianSortedArrays(nums1, nums2))