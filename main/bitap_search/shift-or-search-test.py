import numpy as np

multi_nucleotides = {'R': ['A', 'G'], 'Y': ['C', 'T'], 'S': ['G', 'C'], 'W': ['A', 'T'], 'K': ['G', 'T'],
                     'M': ['A', 'C'], 'B': ['C', 'G', 'T'], 'D': ['A', 'G', 'T'], 'H': ['A', 'C', 'T'],
                     'V': ['A', 'C', 'G']}


# patterns preprocessing
def get_bitmask_table(pattern):
    m = len(pattern)
    # Build char -> bitmask table for pattern
    T = {}
    for i in range(m):
        c = pattern[i]
        multi_nucl = multi_nucleotides.get(c, [])
        # if multi_nucl:
        #     for nucleotide in multi_nucl:
        #         if nucleotide in T:
        #             T[nucleotide] ^= (1 << i)
        #         else:
        #             T[nucleotide] = ~(1 << i)
        # else:
        # if c in T:
        #     T[c] ^= (1 << i)
        # else:
        #     T[c] = ~(1 << i)
        for i in range(m):
            T[pattern[i]] = (T.get(pattern[i], 0) | (1 << i))

    for key, value in T.items():
        print("key: " + key + " value: " + bin(value))# np.binary_repr(value, 64))
    return T


def shift_or_search(text, pattern):
    res = []
    D = -1
    m = len(pattern)
    n = len(text)
    T = get_bitmask_table(pattern)
    mask = ~(1 << (m - 1))
    # print(np.binary_repr(mask, 64))
    # print(np.binary_repr(D, 64))
    # print(np.binary_repr((D << 1), 64))
    for i in range(n):
        c = text[i]
        if c in T:
            D = (D << 1) | T[c]
        else:
            D = -1
        if ~(mask | D):
            res.append(i - m + 1)
    return res


def bitap_search(text, pattern, errors_count):
    m = len(pattern)
    n = len(text)
    T = get_bitmask_table(pattern)
    mask = ~(1 << (m - 1))
    for k in range(errors_count):
        for column in range(n):
            pass
if __name__ == "__main__":
    seq = "CCGGAAAAAATT"
    enzyme = "GA"
    res = shift_or_search(seq, enzyme)
    print(res)
