from main.aho_korasick_wildcard.trie import Trie
import numpy as np

from main.aho_korasick_wildcard.sub_pattern import SubPattern


class AhoKorasickWildcard:
    sib_trie = None
    # сайты, содержащих N
    patterns = None
    # количество сайтов, содержащих N
    patterns_count = None
    # количество частей, на которые был разделен каждый сайт
    patters_parts_num_list = None

    # TODO: add neb_wildcard_patterns trie build
    def __init__(self, sib_wildcard_patterns, neb_wildcard_patterns):
        self.patterns = sib_wildcard_patterns
        self.patterns_count = len(sib_wildcard_patterns)
        self.patters_parts_num_list = []
        patterns_for_trie = self.get_patterns_for_trie(sib_wildcard_patterns)
        self.sib_trie = Trie(patterns_for_trie)
        self.sib_trie.compose_trie()

    def sib_traverse(self, sequence):
        cur_node = self.sib_trie.get_root()
        i = 0
        # res = []
        search_results = {}
        while i < len(sequence):
            symbol = sequence[i]
            next_node = cur_node.get_child(symbol)
            while not next_node:
                cur_node = cur_node.get_fail_state()
                next_node = cur_node.get_child(symbol)
                if cur_node == self.sib_trie.get_root() and not next_node:
                    i += 1
                    break
            if next_node:
                cur_node = next_node
                for pattern in cur_node.get_output():
                    if pattern not in search_results:
                        search_results[pattern] = list()
                    search_results[pattern].append(i - len(pattern.get_seq()) + 1)
                i += 1
                # res.extend(cur_node.get_output())
        return search_results

    def get_patterns_for_trie(self, wildcard_patterns):
        patterns_for_trie = []
        pattern_index = 0
        while pattern_index < len(wildcard_patterns):
            parts_count = 0
            start_pos = 0
            if wildcard_patterns[pattern_index].get_formatted_seq():
                wildcard_pattern = wildcard_patterns[pattern_index].get_formatted_seq()
            else:
                wildcard_pattern = wildcard_patterns[pattern_index].get_seq()
            n_index = wildcard_pattern.find('N', start_pos)
            while n_index != -1:
                seq = wildcard_pattern[start_pos:n_index]
                if seq != 'N' and seq != '':
                    patterns_for_trie.append(SubPattern(seq, pattern_index, start_pos))
                    parts_count += 1
                start_pos = n_index + 1
                n_index = wildcard_pattern.find('N', start_pos)
            seq = wildcard_pattern[start_pos:]
            if seq != '':
                patterns_for_trie.append(SubPattern(seq, pattern_index, start_pos))
                parts_count += 1
            pattern_index += 1
            self.patters_parts_num_list.append(parts_count)
        return patterns_for_trie

    def do_sib_search(self, sequence):
        res = {}
        c_matrix = np.zeros((self.patterns_count, len(sequence)))
        # Используя алгоритм Ахо-Корасика, найти для каждой строки Pi из patterns_for_trie
        # начальные позиции всех вхождений Pi в текст Т
        search_results = self.sib_traverse(sequence)
        # Для каждого такого начала j строки Pi в Т увеличить счетчик в ячейке j - li матрицы
        # c_matrix на единицу
        for pattern, start_positions in search_results.items():
            for j in start_positions:
                if j - pattern.get_start_pos() >= 0:
                    c_matrix[pattern.get_pattern_num()][j - pattern.get_start_pos()] += 1
        # Просмотреть матрицу c_matrix в поисках ячеек со значением k. Вхождение Pj в T,
        # начинающееся с позиции p, имеется в том и только в том случае, если С(j, p) = k.
        for index, row in np.ndenumerate(c_matrix):
            k = self.patters_parts_num_list[index[0]]
            if c_matrix[index] == k and (index[1] + len(self.patterns[index[0]].get_seq())) <= len(sequence):
                if self.patterns[index[0]] not in res:
                    res[self.patterns[index[0]]] = list()
                res[self.patterns[index[0]]].append(index[1])
        return res

    def do_neb_search(self, sequence):
        res = {}
        return res

if __name__ == "__main__":
    pass
    # w_patterns = ['GCNGCC', 'AANNTTT', 'GTTTTNN', 'NNN']
    # aksw = AhoKorasickWildcard(w_patterns, w_patterns)
    # results = aksw.do_sib_search('AGCAGCCCAAGTTTT')
    # print(results)
