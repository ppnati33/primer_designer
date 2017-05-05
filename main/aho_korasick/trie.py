from main.aho_korasick.state import TrieNode


class Trie:
    root = None
    patterns = None
    is_build = None

    def __init__(self, patterns):
        self.root = TrieNode('-1')
        self.patterns = patterns  # ['e', 'he', 'she', 'his', 'her', 'hers', 'is', 'ers']  # ['cash', 'shew', 'ew']
        self.is_build = False

    def get_root(self):
        return self.root

    def compose_trie(self):
        for p in self.patterns:
            self.add_pattern_to_trie(p)
        self.build_suf_links()
        self.is_build = True

    def add_pattern_to_trie(self, pattern):
        cur_node = self.root
        for i in range(len(pattern.get_seq())):
            if pattern.get_formatted_seq():
                char = pattern.get_formatted_seq()[i]
            else:
                char = pattern.get_seq()[i]
            # Перейти по уже существующей ветке или добавить новую
            cur_node = cur_node.get_or_add_child(char)
            if i == (len(pattern.get_seq()) - 1):
                cur_node.add_output(pattern)

    def build_suf_links(self):
        self.root.set_fail_state(self.root)
        suf_links = []
        children = self.root.get_transitions()
        for char, node in children:
            node.set_fail_state(self.root)
            suf_links.append(node)

        while suf_links:
            prev_level_node = suf_links.pop(0)
            for char, node in prev_level_node.get_transitions():
                pf = prev_level_node.get_fail_state()
                pfc = pf.get_child(char)
                while pf != self.root and not pfc:
                    pf = pf.get_fail_state()
                    pfc = pf.get_child(char)
                if pfc:  # pfc
                    node.set_fail_state(pfc)
                else:
                    node.set_fail_state(self.root)
                # node.add_output(node.get_fail_state().get_output())
                node.update_output(node.get_fail_state().get_output())
                suf_links.append(node)
