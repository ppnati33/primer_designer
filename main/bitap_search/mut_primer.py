from Bio.Seq import Seq


class Primer:

    primer_sequence = None
    mismatch_positions = None
    is_forward = None

    def __init__(self, mismatch_positions, is_forward):
        self.mismatch_positions = mismatch_positions
        self.is_forward = is_forward

    def get_mismatch_positions(self):
        return self.mismatch_positions

    def get_primer_sequence(self):
        return self.primer_sequence

    def set_primer_sequence(self, rest_part, site_part, site_seq):
        site_part = list(site_part)
        for m_pos in self.mismatch_positions:
            site_part[m_pos] = site_seq[m_pos]
        site_part = "".join(site_part)
        if self.is_forward:
            self.primer_sequence = rest_part + site_part[: self.mismatch_positions[-1] + 1]
        else:
            seq = Seq(site_part[self.mismatch_positions[-1]:] + rest_part)
            self.primer_sequence = str(seq.reverse_complement())

    def get_is_forward(self):
        return self.is_forward

    def __str__(self):
        return 'primer_sequence: {}, mismatch_positions: {}'.format(self.primer_sequence, str(self.mismatch_positions))
