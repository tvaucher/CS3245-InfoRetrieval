"""
Given a digit string, return all possible letter combinations that the number could represent.

# A mapping of digit to letters (just like on the telephone buttons) is given below.
# Example
# Input:Digit string "23"
# Output: ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"].
"""
from functools import reduce

class Solution(object):
    def letterCombinations(self, digits):
        """
        :type digits: str
        :rtype: List[str]
        """

        if digits == '':
            return []

        digit_mapping = {'1':'*',
                         '2': 'abc',
                         '3': 'def',
                         '4': 'ghi',
                         '5': 'jkl',
                         '6': 'mno',
                         '7': 'pqrs',
                         '8': 'tuv',
                         '9': 'wxyz',
                         '0': ' '}

        # Using reduce (higher order function / functional programming)
        return reduce((lambda acc, d: [x + y for x in acc for y in digit_mapping[d]]), digits, [""])

        def generate_letter_combinations(digits, digit_maping):
            """
            using generators
            """
            if digits == '':
                yield ''
            else:
                for letter in digit_maping[digits[0]]:
                    for rest in generate_letter_combinations(digits[1:], digit_maping):
                        yield letter + rest

        # return list(generate_letter_combinations(digits, digit_mapping))

print(Solution().letterCombinations(input("Pls input string combination :")))
