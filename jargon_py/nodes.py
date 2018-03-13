from collections import namedtuple

from jargon_py.query import *

Node = namedtuple("Node", "name node")


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

    @property
    def nodes(self):
        return self.__nodes

    def __init__(self, key, parent):
        self.parent = parent
        self.__name = key
        self.__value = None
        self.__nodes = NodeCollection()

    def add_node(self, node):
        self.__nodes.add(node)

    def set_value(self, value):
        self.__value = value

    def __hash__(self):
        return self.__value.__hash__()

    def __str__(self):
        return '{name}'.format(name=self.__name)

    def __iter__(self):
        return self.__nodes.__iter__()

    def __getitem__(self, item):
        return self.__nodes[item]


class NodeCollection:

    def __init__(self):
        self.__nodes = []

    def add(self, node):
        """
        Add a KeyNode to Collection

        :param node:    a key node object
        :type node:     KeyNode

        :return: void
        """
        self.__nodes.append(Node(node.name, node))

    def __len__(self):
        return len(self.__nodes)

    def __iter__(self):
        for n in self.__nodes:
            yield n

    def __getitem__(self, item):
        results = get_nodes(self.__nodes, item)

        for r in results:
            yield r
