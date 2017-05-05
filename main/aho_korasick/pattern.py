class Pattern:
    formatted_seq = None
    seq = None
    names = None

    def __init__(self, seq, names, formatted_seq=None):
        self.seq = seq
        self.names = names
        self.formatted_seq = formatted_seq

    def set_formatted_seq(self, formatted_seq):
        self.formatted_seq = formatted_seq

    def get_formatted_seq(self):
        return self.formatted_seq

    def get_names(self):
        return self.names

    def get_seq(self):
        return self.seq

    def __str__(self):
        return 'seq: {}, formatted_seq: {}, names: {}'.format(self.seq, self.formatted_seq, str(self.names))

    def __hash__(self):
        return hash((self.seq, self.formatted_seq))

    def __eq__(self, other):
        return (self.seq, self.formatted_seq) == (other.seq, other.formatted_seq)

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not (self == other)
