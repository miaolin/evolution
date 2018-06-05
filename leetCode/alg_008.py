"""
Implement atoi which converts a string to an integer.
The function first discards as many whitespace characters as necessary until the first non-whitespace character is found.
Then, starting from this character, takes an optional initial plus or minus sign followed by as many numerical digits as
possible, and interprets them as a numerical value.

The string can contain additional characters after those that form the integral number, which are ignored and have no
effect on the behavior of this function.

If the first sequence of non-whitespace characters in str is not a valid integral number, or if no such sequence exists
because either str is empty or it contains only whitespace characters, no conversion is performed.

If no valid conversion could be performed, a zero value is returned.

Note:

Only the space character ' ' is considered as whitespace character.
Assume we are dealing with an environment which could only store integers within the 32-bit signed integer range:
[−2^31,  2^31 − 1]. If the numerical value is out of the range of representable values,
INT_MAX (2^31 − 1) or INT_MIN (−2^31) is returned.
Example 1:

Input: "42"
Output: 42
Example 2:

Input: "   -42"
Output: -42
Explanation: The first non-whitespace character is '-', which is the minus sign.
             Then take as many numerical digits as possible, which gets 42.
Example 3:

Input: "4193 with words"
Output: 4193
Explanation: Conversion stops at digit '3' as the next character is not a numerical digit.
Example 4:

Input: "words and 987"
Output: 0
Explanation: The first non-whitespace character is 'w', which is not a numerical
             digit or a +/- sign. Therefore no valid conversion could be performed.
Example 5:

Input: "-91283472332"
Output: -2147483648
Explanation: The number "-91283472332" is out of the range of a 32-bit signed integer.
             Thefore INT_MIN (−2^31) is returned.
"""


class Solution:
    def myAtoi(self, str_value):
        """
        :type str_value: str
        :rtype: int
        """
        int_char = [str(n) for n in range(0, 10)]
        sign_char = ["-", "+"]
        valid_char = int_char + sign_char

        convert_flag = False
        b_idx, e_idx = -1, -1
        for n, char in enumerate(str_value):
            if not convert_flag:
                if char == " ":
                    continue
                elif char in valid_char:
                    convert_flag = True
                    b_idx = n
                    continue
                else:
                    break
            elif char not in int_char:
                e_idx = n
                break

        if b_idx == -1:
            return 0
        elif e_idx == -1:
            e_idx = len(str_value)

        if str_value[b_idx] in sign_char and e_idx - b_idx == 1:
            return 0
        
        INT_MIN, INT_MAX = -pow(2, 31), pow(2, 31) - 1
        if str_value[b_idx] == "-":
            int_value = -int(str_value[b_idx+1:e_idx])
        elif str_value[b_idx] == "+":
            int_value = int(str_value[b_idx+1:e_idx])
        else:
            int_value = int(str_value[b_idx:e_idx])

        if int_value < INT_MIN:
            return INT_MIN
        elif int_value > INT_MAX:
            return INT_MAX
        else:
            return int_value


if __name__ == "__main__":

    test = Solution()

    str_value = "4193 with words"
    print(test.myAtoi(str_value))

    str_value = "words and 987"
    print(test.myAtoi(str_value))

    str_value = "   -42"
    print(test.myAtoi(str_value))

    str_value = "-91283472332"
    print(test.myAtoi(str_value))

    str_value = "3.14159"
    print(test.myAtoi(str_value))