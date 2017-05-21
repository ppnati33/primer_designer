from Bio.Seq import Seq


class CustomSearchResult:
    enzyme_with_mismatch = None
    mismatch_positions = None
    start_pos = None
    primer = None

    def __init__(self, enzyme_with_mismatch, mismatch_positions, start_pos):
        self.enzyme_with_mismatch = enzyme_with_mismatch
        self.mismatch_positions = [pos + start_pos for pos in mismatch_positions]
        self.start_pos = start_pos

    def get_enzyme_with_mismatch(self):
        return self.enzyme_with_mismatch

    def get_mismatch_positions(self):
        return self.mismatch_positions

    def get_start_pos(self):
        return self.start_pos

    def get_primer(self):
        return self.primer

    def set_primer(self, primer):
        self.primer = primer

    def __str__(self):
        res = 'enzyme: {}, names: {}, enzyme_with_mutation: {}, enzyme_mutation_position: {}, enzyme_start_position; {}'\
            .format(self.enzyme, str(self.names), self.enzyme_with_mismatch, str(self.mismatch_positions),
                    self.start_pos)
        res += '\nprimer: '
        res += self.primer
        return res

    def __hash__(self):
        return hash((self.enzyme, self.enzyme_with_mismatch, str(self.mismatch_positions), self.start_pos))

    def __eq__(self, other):
        return (self.enzyme, self.enzyme_with_mismatch, str(self.mismatch_positions), self.start_pos) == \
               (other.enzyme, other.enzyme_with_mismatch, str(other.mismatch_positions), other.start_pos)

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not (self == other)
