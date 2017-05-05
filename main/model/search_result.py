class SearchResult:

    site_names = None
    site_sequence = None
    site_len = None
    frequency = None
    cut_positions = None

    def __init__(self, sequence, cut_positions):
        self.site_sequence = sequence
        self.site_len = len(sequence)
        self.cut_positions = cut_positions
        self.frequency = len(cut_positions)
        self.site_names = []

    def get_site_names(self):
        return self.site_names

    def set_site_names(self, names):
        self.site_names = names

    def get_site_sequence(self):
        return self.site_sequence

    def get_site_length(self):
        return self.site_len

    def get_frequency(self):
        return self.frequency

    def get_cut_positions(self):
        return self.cut_positions

    def __str__(self):
        return 'Names: {}, Site Sequence: {}, Site Length: {}, Frequency: {}, Cut Positions: {}'\
            .format(str(self.site_len), self.site_sequence, self.site_len, self.frequency, str(self.cut_positions))
