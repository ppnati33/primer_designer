import xml.etree.ElementTree as e_tree
import re

from main.aho_korasick.pattern import Pattern
from main.model.enzyme_entity import EnzymeEntity
from main.utils.transformation_helper import TransformationHelper


class EnzymesReader:
    # SIB_ENZYMES_XML_PATH = '../../resources/static/xml/syb_enzymes.xml'
    # NEB_ENZYMES_XML_PATH = '../../resources/static/xml/neb_enzymes.xml'
    SIB_ENZYMES_XML_PATH = 'resources/static/xml/syb_enzymes.xml'
    NEB_ENZYMES_XML_PATH = 'resources/static/xml/neb_enzymes.xml'

    all_sib_enzymes_data = None
    all_neb_enzymes_data = None

    def __init__(self):
        self.all_sib_enzymes_data = self.get_enzymes_data(self.SIB_ENZYMES_XML_PATH)
        self.all_neb_enzymes_data = self.get_enzymes_data(self.NEB_ENZYMES_XML_PATH)

    def get_sib_enzymes_data(self):
        return self.all_sib_enzymes_data

    def get_neb_enzymes_data(self):
        return self.all_neb_enzymes_data

    def get_enzymes_data(self, enzyme_file_path):
        enzymes_data = []
        tree = e_tree.parse(enzyme_file_path)
        root_element = tree.getroot()
        enzyme_objs = root_element.findall('enzyme')
        for enzyme_obj in enzyme_objs:
            name = str(enzyme_obj.find('name').text)
            top_site = str(enzyme_obj.find('recognition_site_1').text)
            bottom_site = str(enzyme_obj.find('recognition_site_2').text)
            # TODO: fill link property of enzyme object
            link = ''
            enzyme = EnzymeEntity(name, top_site, bottom_site, link)
            enzymes_data.append(enzyme)
        # print(enzymes_data)
        return enzymes_data

    def get_sib_simple_patterns(self):
        return self.get_simple_patterns(self.all_sib_enzymes_data)

    def get_neb_simple_pattens(self):
        return self.get_simple_patterns(self.all_neb_enzymes_data)

    def get_simple_patterns(self, enzymes_list):
        enzymes_seq_names = {}
        for enzyme in enzymes_list:
            if enzyme.get_top_site().find('N') == -1:
                sequence = enzyme.get_top_site().replace('↑', '')
                if sequence not in enzymes_seq_names:
                    enzymes_seq_names[sequence] = list()
                enzymes_seq_names[sequence].append(enzyme.get_e_name())
        simple_patterns = self.process_multi_nucleotides(enzymes_seq_names)
        return simple_patterns

    def get_sib_wildcard_patterns(self):
        return self.get_wildcard_patterns(self.all_sib_enzymes_data)

    def get_neb_wildcard_patterns(self):
        return self.get_wildcard_patterns(self.all_neb_enzymes_data)

    def get_wildcard_patterns(self, enzymes_list):
        enzymes_seq_names = {}
        for enzyme in enzymes_list:
            sequence = enzyme.get_top_site()
            if sequence.find('N') != -1:
                sequence = sequence.replace('(N)', '')
                start_digit_pos = 0
                digits = []
                while start_digit_pos < len(sequence):
                    if sequence[start_digit_pos].isdigit():
                        end_digit_pos = start_digit_pos + 1
                        while sequence[end_digit_pos].isdigit():
                            end_digit_pos += 1
                        digits.append(sequence[start_digit_pos:end_digit_pos])
                        start_digit_pos = end_digit_pos
                    else:
                        start_digit_pos += 1
                sequence = self.replace_all_digits_by_n(sequence, digits)
                sequence = sequence.replace('↑', '')
                if sequence not in enzymes_seq_names:
                    enzymes_seq_names[sequence] = list()
                enzymes_seq_names[sequence].append(enzyme.get_e_name())
        wildcard_patterns = self.process_multi_nucleotides(enzymes_seq_names)
        return wildcard_patterns

    def get_all_sib_patterns(self):
        return self.get_all_patterns(self.all_sib_enzymes_data)

    def get_all_neb_patterns(self):
        return self.get_all_patterns(self.all_neb_enzymes_data)

    def get_all_patterns(self, enzymes_list):
        patterns = {}
        for enzyme in enzymes_list:
            sequence = enzyme.get_top_site()
            e_name = enzyme.get_e_name()
            if sequence.find('N') != -1:
                sequence = sequence.replace('(N)', '')
                start_digit_pos = 0
                digits = []
                while start_digit_pos < len(sequence):
                    if sequence[start_digit_pos].isdigit():
                        end_digit_pos = start_digit_pos + 1
                        while sequence[end_digit_pos].isdigit():
                            end_digit_pos += 1
                        digits.append(sequence[start_digit_pos:end_digit_pos])
                        start_digit_pos = end_digit_pos
                    else:
                        start_digit_pos += 1
                sequence = self.replace_all_digits_by_n(sequence, digits)
            sequence = sequence.replace('↑', '')
            if sequence in patterns:
                patterns[sequence].add_name(e_name)
            else:
                p = Pattern(sequence, [e_name])
                patterns[sequence] = p
        return list(patterns.values())


    def replace_all_digits_by_n(self, sequence, digits):
        for digit in digits:
            n_seq = 'N' * int(digit)
            sequence = sequence.replace(digit, n_seq)
        return sequence

    def process_multi_nucleotides(self, enzymes_seq_names):
        transformer = TransformationHelper()
        patterns = []
        for seq, names in enzymes_seq_names.items():
            if transformer.check_multi_nucleotides(seq):
                formatted_seqs = transformer.get_formatted_patterns(seq)
                for formatted_seq in formatted_seqs:
                    pattern = Pattern(seq, names, formatted_seq)
                    patterns.append(pattern)
            else:
                pattern = Pattern(seq, names)
                patterns.append(pattern)
        return patterns


if __name__ == "__main__":
    pass
    # patts = EnzymesReader.get_sib_enzymes_seq_names_data()
    # enzymes_seq_names_test = {'aRggY': ['name1', 'name2'], 'cgggWWttt': ['name3']}
    # patts = EnzymesReader.process_multi_nucleotides(enzymes_seq_names_test)
    # for p in patts:
    #    print(str(p))
    er = EnzymesReader()
    patts = er.get_all_sib_patterns()
    for p in patts:
        print(str(p))
