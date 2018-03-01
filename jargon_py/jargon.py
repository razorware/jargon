from os import path

from nodes import *

OPEN = 123      # '{'
CLOSE = 125     # '}'
SPACE = 32      # ' '
EOL = 13        # '\r'
LF = 10         # '\n'
TAB = 9         # '\t'
FWD_SLASH = 47  # '/'
ASTERISK = 42   # '*'
TAG_DELIM = 58  # ':'

WHITESPACE = [SPACE, TAB, EOL, LF]
CRLF = [EOL, LF]
LINE_COMMENT = bytes([FWD_SLASH, FWD_SLASH])
START_COMMENT_BLOCK = bytes([FWD_SLASH, ASTERISK])
CLOSE_COMMENT_BLOCK = bytes([ASTERISK, FWD_SLASH])


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
        return self.__bytes

    def __init__(self, file):
        self.file = path.abspath(file)
        self.__bytes = None

    def set_bytes(self, bytes):
        self.__bytes = bytes


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

                while buffer[idx] not in CRLF and buffer[idx] != CLOSE:
                    value.append(buffer[idx])
                    idx += 1

                if len(value) > 0:
                    kn.set_value(value.decode())

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

            # if we encounter '}' here assume container close and break loop
            if buffer[idx] == CLOSE:
                break

            key = bytearray()
            while idx < length and buffer[idx] != OPEN and buffer[idx] != TAG_DELIM:
                if buffer[idx] in WHITESPACE:
                    idx += 1
                    continue

                idx = self.__ignore_comments(idx)

                if buffer[idx] == CLOSE:
                    break

                key.append(buffer[idx])
                idx += 1

            # can check to see if start location is valid
            if len(key) > 0:
                start = -1
                raw_node = RawNode(key.decode())

            if buffer[idx] == TAG_DELIM:
                idx += 1

                # skip any spaces
                while buffer[idx] in WHITESPACE:
                    idx += 1

                start = idx
                # read the node content
                while buffer[idx] not in CRLF:
                    idx += 1
                # complete to line feed
                while buffer[idx] in CRLF:
                    idx += 1

            if buffer[idx] == OPEN:
                bal_oc = 1
                idx += 1
                start = idx
                children = None

                while bal_oc != 0 and idx < length:
                    if buffer[idx] in WHITESPACE:
                        idx += 1
                        continue

                    if buffer[idx] not in [OPEN, CLOSE]:
                        # skip comments
                        idx = self.__ignore_comments(idx)
                        # read node content
                        content_len = self.__length_to_balance(bal_oc, idx, OPEN, CLOSE)
                        children = self.__scan(idx, content_len)

                        idx += content_len - 1

                    if buffer[idx] == OPEN:
                        bal_oc += 1
                    elif buffer[idx] == CLOSE:
                        bal_oc -= 1

                    idx += 1

                if children is not None:
                    for ch in children.__iter__():
                        raw_node.append(ch)

            raw_node.start = start
            nodes.append(raw_node)

            idx += 1

        return nodes

    def __ignore_comments(self, idx):
        buffer = self.__fso.buffer

        if buffer[idx] == FWD_SLASH:
            token = bytes([buffer[idx], buffer[idx+1]])
            # check single-line
            if token == LINE_COMMENT:
                idx += 2
                while buffer[idx] not in CRLF:
                    idx += 1
            # check multi-line
            elif token == START_COMMENT_BLOCK:
                idx += 2
                while token != CLOSE_COMMENT_BLOCK:
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
        bal_oc = bal_index
        idx = start

        while bal_oc != 0 and idx < len(buffer):
            idx = self.__ignore_comments(idx)

            if buffer[idx] == begin:
                bal_oc += 1
            elif buffer[idx] == end:
                bal_oc -= 1

            idx += 1

        return idx - start
