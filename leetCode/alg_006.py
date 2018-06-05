"""
The string "PAYPALISHIRING" is written in a zigzag pattern on a given number of rows like this: (you may want to display this pattern in a fixed font for better legibility)

P   A   H   N
A P L S I I G
Y   I   R
And then read line by line: "PAHNAPLSIIGYIR"

Write the code that will take a string and make this conversion given a number of rows:

string convert(string s, int numRows);
Example 1:
Input: s = "PAYPALISHIRING", numRows = 3
Output: "PAHNAPLSIIGYIR"

P   A   H   N
A P L S I I G
Y   I   R

Example 2:
Input: s = "PAYPALISHIRING", numRows = 4
Output: "PINALSIGYAHRPI"
Explanation:

P     I    N
A   L S  I G
Y A   H R
P     I
"""


class Solution:
    def convert(self, s, numRows):
        """
        :type s: str
        :type numRows: int
        :rtype: str
        """
        n = len(s)
        str = ""
        if numRows == 1:
            return s

        for row_index in range(numRows):
            # if (numRows % 2 == 1 and row_index % 2 == 0) or (numRows % 2 == 0 and row_index in [0, numRows-1]):
            if row_index in [0, numRows - 1]:
                for idx in range(row_index, n, (numRows - 1) * 2):
                    str += s[idx]
            else:
                b_index = row_index
                while b_index < n:
                    str += s[b_index]
                    b_index += (numRows - row_index - 1) * 2
                    if b_index < n:
                        str += s[b_index]
                    b_index += row_index * 2
        return str
    

if __name__ == "__main__":

    test = Solution()

    s = "PAYPALISHIRING"
    numRows = 5
    print(test.convert(s, numRows))
    numRows = 4
    print(test.convert(s, numRows))