class SubPattern:
    seq = None
    pattern_num = None
    start_pos = None

    def __init__(self, seq, pattern_num, start_pos):
        self.seq = seq
        self.pattern_num = pattern_num
        self.start_pos = start_pos

    def get_seq(self):
        return self.seq

    def get_pattern_num(self):
        return self.pattern_num

    def get_start_pos(self):
        return self.start_pos

    def __hash__(self):
        return hash((self.seq, self.pattern_num, self.start_pos))

    def __eq__(self, other):
        return (self.seq, self.pattern_num, self.start_pos) == (other.seq, other.pattern_num, other.start_pos)

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not (self == other)

    def __str__(self):
        return 'seq: {}, pattern_num: {}, start_pos: {}'.format(self.seq, self.pattern_num, self.start_pos)
