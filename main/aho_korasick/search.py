from main.aho_korasick.trie import Trie


class AhoKorasickSearch:
    sib_trie = None

    def __init__(self, sib_patterns, neb_patterns):
        self.sib_trie = Trie(sib_patterns)
        self.sib_trie.compose_trie()
        # TODO: do parallel trie building
        self.neb_trie = Trie(neb_patterns)
        self.neb_trie.compose_trie()

    def neb_traverse(self, sequence):
        search_results = self.traverse_sequence(sequence, self.neb_trie.get_root())
        return search_results

    def sib_traverse(self, sequence):
        search_results = self.traverse_sequence(sequence, self.sib_trie.get_root())
        return search_results

    def traverse_sequence(self, sequence, trie_root):
        cur_node = trie_root
        i = 0
        # res = []
        search_results = {}
        while i < len(sequence):
            symbol = sequence[i]
            next_node = cur_node.get_child(symbol)
            while not next_node:
                cur_node = cur_node.get_fail_state()
                next_node = cur_node.get_child(symbol)
                if cur_node == trie_root and not next_node:
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


if __name__ == "__main__":
    # aks = AhoKorasickSearch()
    # ['e', 'he', 'she', 'his', 'her', 'hers', 'is', 'ers']
    # results = aks.sib_traverse('shershehishers')  # 'cashew'
    # print(results)
    pass
