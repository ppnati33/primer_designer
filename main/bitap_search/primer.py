class Primer:

    primer_sequence = None
    primer_start_position = None

    def __init__(self, primer_start_pos):
        self.primer_start_position = primer_start_pos

    def get_primer_start_position(self):
        return self.primer_start_position

    def get_primer_sequence(self):
        return self.primer_sequence

    def set_primer_sequence(self, seq):
        self.primer_sequence = seq

    def __str__(self):
        return 'primer_sequence: {}, primer_start_pos: {}'.format(self.primer_sequence, self.primer_start_position)
