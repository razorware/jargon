from os import path

from jargon_py import *
from jargon_py.nodes import *


def load(file):
    fso = FSysObj(file)
    p = Parser()
    '''
    First pass -- finds keys annotating start position of raw node contents
    '''
    raw_nodes = p.parse(fso)
    '''
    Second pass -- build key-node values
    '''
    key_nodes = p.build_nodes(raw_nodes)

    return key_nodes


class FileMap:

    @property
    def root(self):
        return path.abspath(self.__root_path)

    def __init__(self, f_path):
        self.__root_path = f_path

        self.fso = None

    def load(self, jss_file):
        file = path.join(self.__root_path, jss_file)
        self.fso = FSysObj(file)


class FSysObj:
    """
    File System Object: may be either a directory or a file.
    """
    @property
    def buffer(self):
        return self.__buffer

    def __init__(self, file):
        self.file = path.abspath(file)
        self.__buffer = None

    def set_bytes(self, buffer):
        self.__buffer = buffer


class Parser:

    def __init__(self):
        """
        """
        self.__fso = None

    def parse(self, fso):
        """
        :param fso: FSysObj (File system object)

        :return:
        """
        self.__fso = fso
        with open(self.__fso.file, 'rb') as file:
            self.__fso.set_bytes(file.read())

        return self.__scan()

    def build_nodes(self, raw_nodes):
        """
        Iterate nodes and build child values

        :param raw_nodes:
        :type raw_nodes: list

        :return: dict
        """
        buffer = self.__fso.buffer
        length = len(buffer)

        key_nodes = []
        for n in raw_nodes:
            kn = KeyNode(n.name, n.parent)

            if n.nodes:
                children = self.build_nodes(n.nodes)
                for ch in children:
                    kn.add_node(ch[1])
            else:
                # no child nodes but value instead
                idx = n.start
                value = bytearray()

                # reads the entirety of line
                while buffer[idx] not in CR_LF and buffer[idx] != CLOSE_BLOCK and idx < length:
                    # '"' will cause everything to read
                    if buffer[idx] == DBL_QUOTE:
                        idx += 1

                        if buffer[idx] in CR_LF:
                            continue

                        while buffer[idx] != DBL_QUOTE:
                            # skip '\'
                            if buffer[idx] == ESCAPE:
                                idx += 1

                            value.append(buffer[idx])
                            idx += 1

                        continue

                    value.append(buffer[idx])
                    idx += 1

                if len(value) > 0:
                    kn.set_value(self.__build_value(value.decode()))

            key_nodes.append((kn.name, kn))

        return key_nodes

    def __scan(self, index=0, read_length=None):
        buffer = self.__fso.buffer
        idx = index
        length = len(buffer) if read_length is None else idx+read_length
        nodes = []

        while idx < length:
            if buffer[idx] in WHITESPACE:
                idx += 1
                continue

            idx = self.__ignore_comments(idx)
            tag, idx = get_tag(buffer, idx)

            start = idx
            if buffer[idx] == OPEN_BLOCK:
                idx += 1
                start = idx

                while buffer[idx] != CLOSE_BLOCK:
                    idx += 1

            nodes.append(RawNode(tag.decode(), start=start))

            idx += 1

        return nodes

    def __ignore_comments(self, idx):
        buffer = self.__fso.buffer

        if buffer[idx] == FWD_SLASH:
            token = bytes([buffer[idx], buffer[idx+1]])
            # check single-line
            if token == LINE_COMMENT:
                idx += 2
                while buffer[idx] not in CR_LF:
                    idx += 1
            # check multi-line
            elif token == START_BLOCK_COMMENT:
                idx += 2
                while token != CLOSE_BLOCK_COMMENT:
                    if buffer[idx] == ASTERISK:
                        token = bytes([buffer[idx], buffer[idx+1]])
                        idx += 2
                    else:
                        idx += 1

                while buffer[idx] in WHITESPACE:
                    idx += 1

        return idx

    def __length_to_balance(self, bal_index, start, begin, end):
        buffer = self.__fso.buffer
        bal_be = bal_index
        idx = start

        while bal_be != 0 and idx < len(buffer):
            idx = self.__ignore_comments(idx)

            if buffer[idx] == begin:
                bal_be += 1
            elif buffer[idx] == end:
                bal_be -= 1

            idx += 1

        return idx - start

    @staticmethod
    def __build_value(value):
        """

        :param value:
        :type value: str

        :return:
        """
        if value.startswith('"'):
            pass

        return value
