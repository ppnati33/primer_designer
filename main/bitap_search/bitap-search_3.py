from main.bitap_search.pattern import Pattern


class BitapSearch:
    multi_nucleotides = {'R': ['A', 'G'], 'Y': ['C', 'T'], 'S': ['G', 'C'], 'W': ['A', 'T'], 'K': ['G', 'T'],
                         'M': ['A', 'C'], 'B': ['C', 'G', 'T'], 'D': ['A', 'G', 'T'], 'H': ['A', 'C', 'T'],
                         'V': ['A', 'C', 'G'], 'N': ['A', 'C', 'G', 'T']}

    nucleotides = ['A', 'C', 'G', 'T']
    patterns = None
    patterns_count = None
    max_errors = None
    summary_pattern = None
    summary_pattern_len = None
    Ms = None
    T = None
    T1 = None

    def __init__(self, patterns, max_errors):
        self.patterns = patterns
        self.patterns_count = len(patterns)
        self.max_errors = max_errors
        self.summary_pattern = "".join(sp.get_enzyme() for sp in patterns)
        self.summary_pattern_len = len(self.summary_pattern)
        self.Ms = self.calculate_m_array()
        self.T = self.generate_T()
        self.T1 = self.generate_T1(self.summary_pattern, self.Ms[0])

    def calculate_m_array(self):
        Ms = []
        for k in range(self.max_errors + 1):
            if k == 0 or k == 1:
                M = 0
                for pattern_num in range(self.patterns_count):
                    for pos in range(len(self.patterns[pattern_num].get_enzyme())):
                        if pos != len(self.patterns[pattern_num].get_enzyme()) - 1:
                            M |= 1
                            M <<= 1
                        if pos == len(self.patterns[pattern_num].get_enzyme()) - 1 \
                                and pattern_num != self.patterns_count - 1:
                            M <<= 1
                M >>= 1
                Ms.append(M)
            else:
                Ms.append(0)
        self.print_table(Ms, self.summary_pattern_len)
        return Ms

    def bitap_search(self, sequence):
        res = {}
        seq_len = len(sequence)

        table = []
        # first index - over k (errors count, numeration starts from 1), second - over columns (letters of haystack)
        empty_column = (2 << (self.summary_pattern_len - 1)) - 1

        # Generate underground level of table
        underground = []
        [underground.append(empty_column) for i in range(seq_len + 1)]
        table.append(underground)
        self.print_table(table[0], self.summary_pattern_len)

        #   Execute precise matching
        k = 1
        table.append([empty_column])
        for column_num in range(1, seq_len + 1):
            prev_column = (table[k][column_num - 1]) >> 1
            letter_pattern = self.T[sequence[column_num - 1]]
            cur_column = prev_column | letter_pattern
            cur_column &= self.T1[sequence[column_num - 1]]
            table[k].append(cur_column)
            # for pattern in reversed(needles):
            #     if (cur_column & 0x1) == 0:
            #         place = haystack[column_num - len(pattern): column_num]
            #         # return (place, k - 1)
            #         if place not in res:
            #             res[place] = list()
            #         res[place].append(column_num - len(pattern))
            #     cur_column >>= len(pattern)
        self.print_table(table[k], self.summary_pattern_len)

        #   Execute fuzzy searching with calculation Levenshtein distance
        for k in range(2, self.max_errors + 2):
            print("Errors =", k - 1)
            table.append([empty_column])

            for column_num in range(1, seq_len + 1):
                prev_column = (table[k][column_num - 1]) >> 1
                letter_pattern = self.T[sequence[column_num - 1]]
                cur_column = prev_column | letter_pattern
                # check replace operation
                res_column = cur_column & (table[k - 1][column_num - 1] >> 1)
                res_column &= self.Ms[k - 1]
                table[k].append(res_column)
                for pattern in reversed(self.patterns):
                    if (res_column & 0x1) == 0:
                        start_pos = column_num - len(pattern.get_enzyme())
                        end_pos = column_num
                        place = sequence[start_pos: end_pos]
                        mismatch_pos = [i for i, (left, right) in enumerate(zip(place, pattern.get_enzyme()))
                                        if left != right]
                        if mismatch_pos:
                            new_matched_pattern = Pattern(pattern.get_enzyme(), pattern.get_names(), place, mismatch_pos)
                            if new_matched_pattern not in res:
                                res[new_matched_pattern] = list()
                            res[new_matched_pattern].append(start_pos)
                    res_column >>= len(pattern.get_enzyme())
            self.print_table(table[k], self.summary_pattern_len)
        return res

    def print_table(self, t, size):
        out = ""
        for i in range(len(t)):
            binary_form = bin(t[i])
            binary_form = binary_form[2:]
            binary_form = binary_form.zfill(size)
            out += binary_form + ", "
        out = out[: -2]
        print(out)

    def get_printable_bin(self, number, size):
        binary_form = bin(number)
        binary_form = binary_form[2:]
        binary_form = binary_form.zfill(size)
        return binary_form

    def custom_equals(self, nucleotide, pattern_symbol):
        if pattern_symbol in self.nucleotides:
            return nucleotide == pattern_symbol
        elif nucleotide in self.multi_nucleotides[pattern_symbol]:
            return True
        return False

    def generate_T(self):
        T = {}
        for letter in self.nucleotides:
            if letter not in T:
                letter_position_in_needle = 0
                for symbol in self.summary_pattern:
                    letter_position_in_needle <<= 1
                    letter_position_in_needle |= int(not self.custom_equals(letter, symbol))
                T[letter] = letter_position_in_needle

        print("T = ")
        for key, value in T.items():
            print("key: " + key + " value: " + self.get_printable_bin(value, self.summary_pattern_len))
        return T

    def generate_T1(self, summary_pattern, vector_M):
        T1 = {}
        for letter in self.nucleotides:
            if letter not in T1:
                letter_position_in_needle = 0
                for symbol in summary_pattern:
                    letter_position_in_needle <<= 1
                    letter_position_in_needle |= int(not self.custom_equals(letter, symbol))
                letter_position_in_needle |= vector_M
                T1[letter] = letter_position_in_needle

        print("T1 = ")
        for key, value in T1.items():
            print("key: " + key + " value: " + self.get_printable_bin(value, self.summary_pattern_len))
        return T1

if __name__ == "__main__":
    seq = 'CCGGAACGAATTCG'
    max_err = 1
    p1 = Pattern('GAA', ['name1'])
    p2 = Pattern('CCTG', ['name2'])
    p3 = Pattern('TAAG', ['name3'])
    pats = [p1, p2, p3]
    bsearch = BitapSearch(pats, max_err)
    res = bsearch.bitap_search(seq)
    for k, v in res.items():
        print(str(k) + ": " + str(v))
