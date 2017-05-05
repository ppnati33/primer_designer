# -*- coding: utf-8 -*-
import sys
import numpy as np

multi_nucleotides = {'R': ['A', 'G'], 'Y': ['C', 'T'], 'S': ['G', 'C'], 'W': ['A', 'T'], 'K': ['G', 'T'],
                     'M': ['A', 'C'], 'B': ['C', 'G', 'T'], 'D': ['A', 'G', 'T'], 'H': ['A', 'C', 'T'],
                     'V': ['A', 'C', 'G']}  # , 'N': ['A', 'C', 'G', 'T']}

nucleotides = ['A', 'C', 'G', 'T']


def neg(x):
    return 0b11111111111111111111111111111111 - x


def _printTable(t, size):
    out = ""
    for i in range(len(t)):
        binaryForm = bin(t[i])
        binaryForm = binaryForm[2:]
        binaryForm = binaryForm.zfill(size)
        out += binaryForm + ", "
    out = out[: -2]
    print(out)


def print_bin(number, size):
    binaryForm = bin(number)
    binaryForm = binaryForm[2:]
    binaryForm = binaryForm.zfill(size)
    return binaryForm


def custom_equals(nucleotide, pattern_symbol):
    if pattern_symbol in nucleotides:
        return nucleotide == pattern_symbol
    elif nucleotide in multi_nucleotides[pattern_symbol]:
        return True
    return False


def bitap_search(haystack, needle, maxErrors):
    res = {}

    haystack_len = len(haystack)
    needle_len = len(needle)

    """Generating mask for each letter in haystack.
    This mask shows presence letter in needle.
    """
    def _generate_alphabet(needle, haystack):
        alphabet = {}
        for letter in nucleotides:
            if letter not in alphabet:
                letter_position_in_needle = 0
                for symbol in needle:
                    letter_position_in_needle <<= 1
                    letter_position_in_needle |= int(not custom_equals(letter, symbol))
                alphabet[letter] = letter_position_in_needle

        for key, value in alphabet.items():
            print("key: " + key + " value: " + print_bin(value, needle_len))
        return alphabet

    alphabet = _generate_alphabet(needle, haystack)

    table = []
    # first index - over k (errors count, numeration starts from 1), second - over columns (letters of haystack)
    empty_column = (2 << (needle_len - 1)) - 1

    #   Generate underground level of table
    underground = []
    [underground.append(empty_column) for i in range(haystack_len + 1)]
    table.append(underground)
    _printTable(table[0], needle_len)

    #   Execute precise matching
    k = 1
    table.append([empty_column])
    for columnNum in range(1, haystack_len + 1):
        prev_column = (table[k][columnNum - 1]) >> 1
        letter_pattern = alphabet[haystack[columnNum - 1]]
        cur_column = prev_column | letter_pattern
        table[k].append(cur_column)
        if (cur_column & 0x1) == 0:
            place = haystack[columnNum - needle_len: columnNum]
            #return (place, k - 1)
            # if place not in res:
            #     res[place] = list()
            # res[place].append(k - 1)
    _printTable(table[k], needle_len)

    #   Execute fuzzy searching with calculation Levenshtein distance
    for k in range(2, maxErrors + 2):
        print("Errors =", k - 1)
        table.append([empty_column])

        for columnNum in range(1, haystack_len + 1):
            prev_column = (table[k][columnNum - 1]) >> 1
            letter_pattern = alphabet[haystack[columnNum - 1]]
            cur_column = prev_column | letter_pattern
            # check replace operation
            res_column = cur_column & (table[k - 1][columnNum - 1] >> 1)

            table[k].append(res_column)
            if (res_column & 0x1) == 0:
                start_pos = columnNum - needle_len
                end_pos = columnNum
                place = haystack[start_pos: end_pos]
                #return (place, k - 1)
                if place not in res:
                    res[place] = list()
                res[place].append(start_pos)

        _printTable(table[k], needle_len)
    #return ("", -1)
    return res


"""Highlight letters in fullWord, which concur with letters in pattern with same order.
wordPart - it's a part of fullWord, where matching with pattern letters will execute.
"""
class bitapHighlighter():

    def __init__(self, full_word, word_part, pattern):
        self._full_word = full_word
        self._word_part = word_part
        self._pattern = pattern
        self._largest_sequence = ""

    """Finding longest sequence of letters in word. Letters must have same order, as in pattern
    """
    def _next_sequence(self, from_pattern_pos, from_word_pos, prev_sequence):
        for pattern_pos in range(from_pattern_pos, len(self._pattern)):
            char = self._pattern[pattern_pos]
            for word_pos in range(from_word_pos, len(self._word_part)):
                if char == self._word_part[word_pos]:
                    sequence = prev_sequence + char
                    self._next_sequence(pattern_pos + 1, word_pos + 1, sequence)
        if len(self._largest_sequence) < len(prev_sequence):
            self._largest_sequence = prev_sequence

    """Divide fullWord on parts: head, place(wordPart) and tail.
    Select each letter of wordPart, which present in _largestSequence with <b></b> tags
    Return gathered parts in one highlighted full word
    """
    def _gather_full_word(self):
        place_pos = self._full_word.find(self._word_part)
        head = self._full_word[0: place_pos]
        tail = self._full_word[place_pos + len(self._word_part):]
        highlighted_place = ""
        for symbol in self._word_part:
            if symbol == self._largest_sequence[0: 1]:
                highlighted_place += "<b>" + symbol + "</b>"
                self._largest_sequence = self._largest_sequence[1:]
            else:
                highlighted_place += symbol
        return head + highlighted_place + tail

    """Run highlighting and return highlited word.
    """

    def getHighlightedWord(self):
        self._next_sequence(0, 0, "")
        return self._gather_full_word()


haystack = 'CCGGAACGACTT'
needle = 'GAA'
errorsCount = 1
print("haystack = " + haystack + ". needle = " + needle + ". errorsCount = " + str(errorsCount))

#   Display letters of haystack in columns
out = ""
out = out.ljust(len(needle) + 2)
for i in range(len(haystack)):
    out += haystack[i].ljust(len(needle)) + "  "
out = out[: -2]
print(out)

#   Start bitap searching
res = bitap_search(haystack, needle, int(errorsCount))
print(res)
#print("Result of Bitap searching: ", needlePlace, errors)
# print(bitapHighlighter(haystack, needlePlace, needle).getHighlightedWord())
