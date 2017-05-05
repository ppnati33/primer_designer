class TrieNode:
    # Существующие выходящие ветки из узла
    transitions = None
    # Значение узла
    char_value = None
    # Является ли узел конечным состоянием автомата
    is_final = None
    suf_link = None
    # Ссылка на первое состояние(узел) в связи неудач
    fail_state = None
    # Список паттернов, которые заканчиваются в этом узле
    output = None

    def __init__(self, value):
        self.transitions = {}
        self.char_value = value
        self.is_final = False
        self.fail_state = None
        self.output = set()

    def get_char_value(self):
        return self.char_value

    def get_fail_state(self):
        return self.fail_state

    def set_fail_state(self, f_state):
        self.fail_state = f_state

    def add_output(self, pattern):
        self.output.add(pattern)
        # self.output.append(pattern)

    def update_output(self, patterns):
        self.output.update(patterns)

    def get_or_add_child(self, char):
        # Пытаемся взять следующую существующую ветку
        next_node = self.get_child(char)
        if not next_node:
            next_node = self.add_child(char)
        return next_node

    def get_child(self, char):
        return self.transitions.get(char, None)

    def add_child(self, char):
        if char in self.transitions:
            return self.transitions[char]
        else:
            new_node = TrieNode(char)
            self.transitions[char] = new_node
        return new_node

    def get_output(self):
        return self.output

    def get_transitions(self):
        return self.transitions.items()  # итератор

    def __str__(self):
        return 'symbol: {}, transitions: {}'.format(self.char_value, str(self.transitions))
