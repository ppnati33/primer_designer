class Pattern:
    enzyme = None
    names = None

    def __init__(self, enzyme, names):
        self.enzyme = enzyme
        self.names = names

    def get_names(self):
        return self.names

    def get_enzyme(self):
        return self.enzyme

    def __str__(self):
        return 'enzyme: {}, names: {}'.format(self.enzyme, str(self.names))

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
