class SearchResult:
    enzyme_with_mutation = None
    enzyme_mutation_position = None
    enzyme_start_position = None
    primer = None

    def __init__(self, enzyme_with_mutation, enzyme_mutation_position, enzyme_start_position):
        self.enzyme_with_mutation = enzyme_with_mutation
        self.enzyme_mutation_position = enzyme_mutation_position
        self.enzyme_start_position = enzyme_start_position

    def get_enzyme_with_mutation(self):
        return self.enzyme_with_mutation

    def get_enzyme_mutation_position(self):
        return self.enzyme_mutation_position

    def get_enzyme_start_position(self):
        return self.enzyme_start_position

    def get_primer(self):
        return self.primer

    def set_primer(self, primer):
        self.primer = primer

    def __str__(self):
        res = 'enzyme: {}, names: {}, enzyme_with_mutation: {}, enzyme_mutation_position: {}, enzyme_start_position; {}'\
            .format(self.enzyme, str(self.names), self.enzyme_with_mutation, self.enzyme_mutation_position,
                    self.enzyme_start_position)
        res += '\nprimer: '
        res += self.primer
        return res

    def __hash__(self):
        return hash((self.enzyme, self.enzyme_with_mutation, self.enzyme_mutation_position, self.enzyme_start_position))

    def __eq__(self, other):
        return (self.enzyme, self.enzyme_with_mutation, self.enzyme_mutation_position, self.enzyme_start_position) == \
               (other.enzyme, other.enzyme_with_mutation, other.enzyme_mutation_position, other.enzyme_start_position)

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not (self == other)
