"""
Given a string, find the length of the longest substring without repeating characters.

Examples:

Given "abcabcbb", the answer is "abc", which the length is 3.

Given "bbbbb", the answer is "b", with the length of 1.

Given "pwwkew", the answer is "wke", with the length of 3.
Note that the answer must be a substring, "pwke" is a subsequence and not a substring.
"""


class Solution:
    def lengthOfLongestSubstring(self, s):
        """
        type s: str
        return: int

        beats 10% of py3 submissions
        """

        if len(s) == 0:
            return 0

        max_len = 0
        for n in range(len(s)):
            m = n + 1
            cur_str = s[n:m]
            while m < len(s):
                if s[m] in cur_str:
                    break
                else:
                    m += 1
                    cur_str = s[n:m]
            print([n, m])
            max_len = max(max_len, m - n)
        return max_len


if __name__ == "__main__":

    test = Solution()
    s1 = "abcabcbb"
    print(test.lengthOfLongestSubstring(s1))

    s2 = "bbbb"
    print(test.lengthOfLongestSubstring(s2))

    s3 = "pwwkew"
    print(test.lengthOfLongestSubstring(s3))
