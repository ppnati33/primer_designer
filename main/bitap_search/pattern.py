class Pattern:
    seq_place = None
    mismatch_position = None
    enzyme = None
    names = None

    def __init__(self, enzyme, names, seq_place=None, mismatch_position=None):
        self.enzyme = enzyme
        self.names = names
        self.seq_place = seq_place
        self.mismatch_position = mismatch_position

    def set_seq_place(self, formatted_seq):
        self.seq_place = formatted_seq

    def get_seq_place(self):
        return self.seq_place

    def get_names(self):
        return self.names

    def get_enzyme(self):
        return self.enzyme

    def get_mismatch_position(self):
        return self.mismatch_position

    def set_mismatch_position(self, mismatch_position):
        self.mismatch_position = mismatch_position

    def __str__(self):
        return 'enzyme: {}, seq_place: {}, mismatch_pos: {}, names: {}'.format(self.enzyme, self.seq_place,
                                                                               str(self.mismatch_position), str(self.names))

    def __hash__(self):
        # return hash((self.enzyme, self.seq_place))
        return hash(self.enzyme)

    def __eq__(self, other):
        # return (self.enzyme, self.seq_place) == (other.enzyme, other.seq_place)
        return self.enzyme == other.enzyme

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not (self == other)
