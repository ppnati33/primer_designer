import sys

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


def bitapSearch(haystack, needle, maxErrors):
    res = {}

    haystackLen = len(haystack)
    needleLen = len(needle)

    def _generateAlphabet(needle):
        alphabet = {}
        for letter in nucleotides:
            if letter not in alphabet:
                letterPositionInNeedle = 0
                for symbol in needle:
                    letterPositionInNeedle <<= 1
                    letterPositionInNeedle |= int(letter != symbol)
                alphabet[letter] = letterPositionInNeedle
        for key, value in alphabet.items():
            print("key: " + key + " value: " + print_bin(value, len(needle)))
        return alphabet

    alphabet = _generateAlphabet(needle)

    table = []
    # first index - over k (errors count, numeration starts from 1), second - over columns (letters of haystack)
    emptyColumn = (2 << (needleLen - 1)) - 1

    #   Generate underground level of table
    underground = []
    [underground.append(emptyColumn) for i in range(haystackLen + 1)]
    table.append(underground)
    _printTable(table[0], needleLen)

    #   Execute precise matching
    k = 1
    table.append([emptyColumn])
    for columnNum in range(1, haystackLen + 1):
        prevColumn = (table[k][columnNum - 1]) >> 1
        letterPattern = alphabet[haystack[columnNum - 1]]
        curColumn = prevColumn | letterPattern
        table[k].append(curColumn)
        if (curColumn & 0x1) == 0:
            place = haystack[columnNum - needleLen: columnNum]
            #return (place, k - 1)
            # if place not in res:
            #     res[place] = list()
            # res[place].append(columnNum - needleLen)
    _printTable(table[k], needleLen)

    #   Execute fuzzy searching with calculation Levenshtein distance
    for k in range(2, maxErrors + 2):
        print("Errors =", k - 1)
        table.append([emptyColumn])

        for columnNum in range(1, haystackLen + 1):
            prevColumn = (table[k][columnNum - 1]) >> 1
            letterPattern = alphabet[haystack[columnNum - 1]]
            curColumn = prevColumn | letterPattern
            curColumn &= table[k - 1][columnNum - 1] >> 1

            table[k].append(curColumn)
            if (curColumn & 0x1) == 0:
                startPos = columnNum - needleLen  # taking in account Replace operation
                endPos = columnNum  # taking in account Replace operation
                place = haystack[startPos: endPos]
                #return (place, k - 1)
                if place not in res:
                    res[place] = list()
                res[place].append(startPos)
        _printTable(table[k], needleLen)
    #return ("", -1)
    return res


haystack = 'CCGGAACGAATT'
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
res = bitapSearch(haystack, needle, int(errorsCount))
print(res)
