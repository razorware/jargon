TAB = 9         # '\t'
LF = 10         # '\n'
EOL = 13        # '\r'
SPACE = 32      # ' '
ASCII = 35      # '#'
TAG_DELIM = 58  # ':'
LINE_TERM = 59  # ';'
ESCAPE = 92     # '\\'
OR = 124        # '|'

WHITESPACE = bytearray([TAG_DELIM, TAB, LF, EOL, SPACE])

__grammar_file = 'jargon.grm'


def is_whitespace(b):
    return b in WHITESPACE


def is_line_terminator(b):
    return b == LINE_TERM


class Lexer:

    @property
    def definitions(self):
        return self.__definitions

    @property
    def grammars(self):
        return self.__grammars

    def __init__(self, grammar_file):
        with open(grammar_file, 'rb') as file:
            self.__bytes = file.read()

        self.__definitions = {}
        self.__grammars = {}
        self.__parse_grammar_file()

    def __parse_grammar_file(self):
        buffer = self.__bytes
        idx = 0
        length = len(buffer)

        while idx < length:
            tag, idx = self.__get_tag(idx)

            while buffer[idx] == TAG_DELIM or is_whitespace(buffer[idx]):
                idx += 1

            # if tag == b'CHARACTER':
            #     pause = True

            definition, idx = self.__get_definition(idx)

            if idx < length:
                while (buffer[idx] == TAG_DELIM or
                       buffer[idx] == LINE_TERM or
                       buffer[idx] in WHITESPACE):
                    idx += 1

                    if idx >= length:
                        break

            self.__definitions.update({tag: definition})

            # idx += 1

    def __get_tag(self, idx):
        tag = bytearray()
        buffer = self.__bytes
        length = len(buffer)

        while idx < length and buffer[idx] != TAG_DELIM:
            tag.append(buffer[idx])
            idx += 1

        # make tag immutable
        return bytes(tag), idx

    def __get_definition(self, idx):
        definition = []
        buffer = self.__bytes
        length = len(buffer)

        while idx < length and buffer[idx] != LINE_TERM:
            b = buffer[idx]
            grp = bytearray()

            while b != OR and b not in WHITESPACE and b != LINE_TERM:
                if b == ESCAPE:
                    idx += 1
                    b = buffer[idx]
                elif b == ASCII:
                    idx += 1
                    b = buffer[idx]

                    # read what follows to next space - an ASCII code
                    ascii_bytes = bytearray()
                    while b not in WHITESPACE:
                        ascii_bytes.append(b)
                        idx += 1
                        b = buffer[idx]

                    b = int(ascii_bytes)
                    # b = chr(ascii_code).encode()[0]

                grp.append(b)
                idx += 1

                b = buffer[idx]

            if b == OR or b in WHITESPACE or b == LINE_TERM:
                if len(grp) > 0:
                    definition.append(grp)

                idx += 1
                continue

        return definition, idx


def __load_grammar():
    from os import path

    file_path = path.abspath(path.dirname(__file__))
    file_path = path.join(file_path, __grammar_file)
    lexer = Lexer(file_path)

    return lexer.definitions


Grammar = __load_grammar()
