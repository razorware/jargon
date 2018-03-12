
def get_nodes(collection, key):
    results = filter(lambda r: r[0] == key, collection)

    for k, n in results:
        yield n


def first(iterator):
    item = None

    for i in iterator:
        item = i
        break

    return item


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
        return self.__name

    @property
    def value(self):
        return self.__value

    def __init__(self, key, parent):
        self.parent = parent
        self.__name = key
        self.__value = None

    def add_node(self, node):
        if not self.__value:
            self.__value = []

        self.__value.append((node.name, node))

    def set_value(self, value):
        if isinstance(value, tuple):
            from collections import namedtuple
            attribs = value[0]
            values = value[1]
            val_cls = namedtuple(self.name, attribs)

            value = val_cls(*values)

        if not self.__value:
            self.__value = value

    def __getitem__(self, item):
        results = get_nodes(self.__value, item)

        for v in results:
            yield v

    def __hash__(self):
        return self.__value.__hash__()

    def __str__(self):
        return '{name}'.format(name=self.__name)
