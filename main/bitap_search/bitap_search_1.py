# -*- coding: utf-8 -*-
import sys
import numpy as np

multi_nucleotides = {'R': ['A', 'G'], 'Y': ['C', 'T'], 'S': ['G', 'C'], 'W': ['A', 'T'], 'K': ['G', 'T'],
                     'M': ['A', 'C'], 'B': ['C', 'G', 'T'], 'D': ['A', 'G', 'T'], 'H': ['A', 'C', 'T'],
                     'V': ['A', 'C', 'G'], 'N': ['A', 'C', 'G', 'T']}

nucleotides = ['A', 'C', 'G', 'T']


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


def calculate_m_vector(patterns):
    M = 0
    for pattern_num in range(len(patterns)):
        for pos in range(len(patterns[pattern_num])):
            if pos != len(patterns[pattern_num]) - 1:
                M |= 1
                M <<= 1
            if pos == len(patterns[pattern_num]) - 1 and pattern_num != len(patterns) - 1:
                M <<= 1
    M >>= 1
    return M


def calculate_m_array(patterns, errors):
    Ms = []
    for k in range(errors + 1):
        if k == 0 or k == 1:
            M = 0
            for pattern_num in range(len(patterns)):
                for pos in range(len(patterns[pattern_num])):
                    if pos != len(patterns[pattern_num]) - 1:
                        M |= 1
                        M <<= 1
                    if pos == len(patterns[pattern_num]) - 1 and pattern_num != len(patterns) - 1:
                        M <<= 1
            M >>= 1
            Ms.append(M)
        else:
            Ms.append(0)
    return Ms


def generate_T(summary_pattern):
    T = {}
    for letter in nucleotides:
        if letter not in T:
            letter_position_in_needle = 0
            for symbol in summary_pattern:
                letter_position_in_needle <<= 1
                letter_position_in_needle |= int(not custom_equals(letter, symbol))
            T[letter] = letter_position_in_needle

    for key, value in T.items():
        print("key: " + key + " value: " + print_bin(value, len(summary_pattern)))
    return T


def generate_T1(summary_pattern, vector_M):
    T1 = {}
    for letter in nucleotides:
        if letter not in T1:
            letter_position_in_needle = 0
            for symbol in summary_pattern:
                letter_position_in_needle <<= 1
                letter_position_in_needle |= int(not custom_equals(letter, symbol))
            letter_position_in_needle |= vector_M
            T1[letter] = letter_position_in_needle

    for key, value in T1.items():
        print("key: " + key + " value: " + print_bin(value, len(summary_pattern)))
    return T1


def bitap_search(haystack, needles, maxErrors):
    res = {}
    haystack_len = len(haystack)
    # needles_len = len(needles)
    summary_pattern = "".join(needles)
    sum_patterns_len = len(summary_pattern)
    Ms = calculate_m_array(needles, maxErrors)
    print("Ms = ")
    _printTable(Ms, sum_patterns_len)

    print("T = ")
    T = generate_T(summary_pattern)
    print("T1 = ")
    T1 = generate_T1(summary_pattern, Ms[0])

    table = []
    # first index - over k (errors count, numeration starts from 1), second - over columns (letters of haystack)
    empty_column = (2 << (sum_patterns_len - 1)) - 1

    #   Generate underground level of table
    underground = []
    [underground.append(empty_column) for i in range(haystack_len + 1)]
    table.append(underground)
    _printTable(table[0], sum_patterns_len)

    #   Execute precise matching
    k = 1
    table.append([empty_column])
    for column_num in range(1, haystack_len + 1):
        prev_column = (table[k][column_num - 1]) >> 1
        letter_pattern = T[haystack[column_num - 1]]
        cur_column = prev_column | letter_pattern
        cur_column &= T1[haystack[column_num - 1]]
        table[k].append(cur_column)
        # for pattern in reversed(needles):
        #     if (cur_column & 0x1) == 0:
        #         place = haystack[column_num - len(pattern): column_num]
        #         # return (place, k - 1)
        #         if place not in res:
        #             res[place] = list()
        #         res[place].append(column_num - len(pattern))
        #     cur_column >>= len(pattern)
    _printTable(table[k], sum_patterns_len)

    #   Execute fuzzy searching with calculation Levenshtein distance
    for k in range(2, maxErrors + 2):
        print("Errors =", k - 1)
        table.append([empty_column])

        for column_num in range(1, haystack_len + 1):
            prev_column = (table[k][column_num - 1]) >> 1
            letter_pattern = T[haystack[column_num - 1]]
            cur_column = prev_column | letter_pattern
            # check replace operation
            res_column = cur_column & (table[k - 1][column_num - 1] >> 1)
            res_column &= Ms[k-1]
            table[k].append(res_column)
            for pattern in reversed(needles):
                if (res_column & 0x1) == 0:
                    start_pos = column_num - len(pattern)
                    end_pos = column_num
                    place = haystack[start_pos: end_pos]
                    # return (place, k - 1)
                    if pattern not in res:
                        res[pattern] = list()
                    res[pattern].append(start_pos)
                res_column >>= len(pattern)
        _printTable(table[k], sum_patterns_len)
    # return ("", -1)
    return res


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


haystack = 'CCGGAACGAATTCG'
#TODO: не работает для случая, когда N стоит в начале паттерна
needles = ['GAAN', 'TNC', 'RCG']  # , 'TGT', 'CGG']
errorsCount = 1
# print("haystack = " + haystack + ". needle = " + needles + ". errorsCount = " + str(errorsCount))

#   Display letters of haystack in columns
out = ""
out = out.ljust(len(needles) + 2)
for i in range(len(haystack)):
    out += haystack[i].ljust(len(needles)) + "  "
out = out[: -2]
print(out)

#   Start bitap searching
res = bitap_search(haystack, needles, int(errorsCount))
print(res)
