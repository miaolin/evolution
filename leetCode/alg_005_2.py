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

    test = Solution()

    s = "babad"
    print(test.longestPalindrome(s))
