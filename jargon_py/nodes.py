from key_token import KeyToken


class RawNode:

    @property
    def nodes(self):
        return self.__nodes

    def __init__(self, key, parent=None, start=0):
        self.parent = parent
        self.name = key
        self.start = start
        self.__nodes = None

    def append(self, child_node):
        if self.__nodes is None:
            self.__nodes = []

        child_node.parent = self
        self.__nodes.append(child_node)

    def __str__(self):
        return '{name}'.format(name=self.name)


class KeyNode:

    @property
    def name(self):
        return self.__token.name

    @property
    def value(self):
        return self.__value

    def __init__(self, key, parent):
        self.parent = parent
        self.__token = KeyToken(key)
        self.__value = None

    def add_node(self, node):
        if not self.__value:
            self.__value = {}

        self.__value.update({node: node.value})

    def set_value(self, value):
        if not self.__value:
            self.__value = value

    def __eq__(self, other):
        return self.__token == other.__token

    def __ne__(self, other):
        return self.__token != other.__token

    def __hash__(self):
        return self.__token.__hash__()

    def __str__(self):
        return '{name}'.format(name=self.name)
