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


class Solution_gd:
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


class Solution_dp:
    def longestPalindrome(self, s):

        n = len(s)
        results = [[False] * n for i in range(n)]
        x, y = 0, 0

        for i in range(n):
            results[i][i] = True

        for i in range(n - 1):
            if s[i] == s[i+1]:
                results[i][i+1] = True
                if not x and not y:
                    x, y = i, i + 1

        for k in range(2, n):
            for i in range(n - 2):
                j = i + k
                if j == n:
                    break
                if results[i+1][j-1] and s[i] == s[j]:
                    results[i][j] = True

                    if j - i > y - x:
                        x, y = i, j
        return s[x:y+1]


if __name__ == "__main__":

    test = Solution_dp()

    s = "babad"
    print(test.longestPalindrome(s))

    s = "cbbd"
    print(test.longestPalindrome(s))

    s = "ab"
    print(test.longestPalindrome(s))