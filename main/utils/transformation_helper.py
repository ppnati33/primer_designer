class TransformationHelper:
    multi_2_nucleotides = {'R': ['A', 'G'], 'Y': ['C', 'T'], 'S': ['G', 'C'], 'W': ['A', 'T'], 'K': ['G', 'T'],
                           'M': ['A', 'C'], 'B': ['C', 'G', 'T'], 'D': ['A', 'G', 'T'], 'H': ['A', 'C', 'T'],
                           'V': ['A', 'C', 'G']}

    def __init__(self):
        super().__init__()

    def check_multi_nucleotides(self, sequence):
        if any(s in sequence for s in self.multi_2_nucleotides.keys()):
            return True
        else:
            return False

    def get_formatted_patterns(self, seq):
        formatted_patterns = []
        for i in range(len(seq)):
            symbol = seq[i]
            if symbol in self.multi_2_nucleotides.keys():
                if not formatted_patterns:
                    for replacement in self.multi_2_nucleotides[symbol]:
                        formatted_seq = list(seq)
                        formatted_seq[i] = replacement
                        formatted_patterns.append(''.join(formatted_seq))
                else:
                    initial_size = len(formatted_patterns)
                    for j in range(0, initial_size):
                        pattern = formatted_patterns.pop(0)
                        for replacement in self.multi_2_nucleotides[symbol]:
                            formatted_seq = list(pattern)
                            formatted_seq[i] = replacement
                            formatted_patterns.append(''.join(formatted_seq))
            i += 1
        return formatted_patterns
