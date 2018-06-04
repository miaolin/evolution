"""
Given a string s, find the longest palindromic substring in s. You may assume that the maximum length of s is 1000.

Example 1:

Input: "babad"
Output: "bab"
Note: "aba" is also a valid answer.
Example 2:

Input: "cbbd"
Output: "bb"
"""


class Solution:
    # greedy solution
    def longestPalindrome(self, s):
        """
        :type s: str
        :rtype: str
        """

        if s == s[::-1] or len(s) < 2:
            return s

        res = ""
        for i in range(len(s)):
            tmp = self.helper(s, i, i)
            if len(tmp) > len(res):
                res = tmp

            tmp = self.helper(s, i, i + 1)
            if len(tmp) > len(res):
                res = tmp
        return res

    def helper(self, s, l, r):
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1
            r += 1
        return s[l+1:r]




if __name__ == "__main__":

    test = Solution()

    s = "babad"
    print(test.longestPalindrome(s))

    s = "cbbd"
    print(test.longestPalindrome(s))

    s = "ab"
    print(test.longestPalindrome(s))