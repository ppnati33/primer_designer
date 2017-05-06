class Pattern:
    seq_place = None
    mismatch_position = None
    match_start_positions = None
    enzyme = None
    names = None
    primers = None

    def __init__(self, enzyme, names, seq_place=None, mismatch_position=None):
        self.enzyme = enzyme
        self.names = names
        self.seq_place = []
        self.mismatch_position = []
        self.match_start_positions = []
        self.primers = []

    def get_primers(self):
        return self.primers

    def add_primers(self, primer):
        self.primers.append(primer)

    def set_seq_place(self, formatted_seq):
        self.seq_place = formatted_seq

    def add_seq_place(self, seq_place):
        self.seq_place.append(seq_place)

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

    def add_mismatch_position(self, position):
        self.mismatch_position.extend(position)

    def get_match_start_positions(self):
        return self.match_start_positions

    def set_match_start_positions(self, match_start_positions):
        self.match_start_positions = match_start_positions

    def add_match_start_positions(self, position):
        self.match_start_positions.append(position)

    def __str__(self):
        return 'enzyme: {}, names: {}, seq_places: {}, mismatch_positions: {}, matching_start_potions: {}, ' \
               'primers: {}'.format(self.enzyme, str(self.names), str(self.seq_place), str(self.mismatch_position),
                    str(self.match_start_positions), str(self.primers))

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
