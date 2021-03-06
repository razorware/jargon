
TAB = 9             # '\t'
LF = 10             # '\n'
EOL = 13            # '\r'
SPACE = 32          # ' '
DBL_QUOTE = 34      # '"'
SGL_QUOTE = 39      # '\''
ASTERISK = 42       # '*'
LIST_DELIM = 44     # ','
FWD_SLASH = 47      # '/'
TAG_DELIM = 58      # ':'
LINE_TERM = 59      # ';'
ESCAPE = 92         # '\\'
OPEN_BLOCK = 123    # '{'
CLOSE_BLOCK = 125   # '}'

WHITESPACE = bytes([SPACE, TAB, EOL, LF])
CR_LF = bytes([EOL, LF])
LINE_COMMENT = bytes([FWD_SLASH, FWD_SLASH])
START_BLOCK_COMMENT = bytes([FWD_SLASH, ASTERISK])
CLOSE_BLOCK_COMMENT = bytes([ASTERISK, FWD_SLASH])


def is_whitespace(b):
    return b in WHITESPACE


def is_line_terminator(b):
    return b == LINE_TERM


def get_tag(buffer, idx):
    tag = bytearray()
    length = len(buffer)

    while idx < length and \
            (buffer[idx] != TAG_DELIM and buffer[idx] != OPEN_BLOCK):
        if is_whitespace(buffer[idx]):
            idx += 1
            continue

        tag.append(buffer[idx])
        idx += 1

    # make tag immutable
    return bytes(tag), idx


def ignore_whitespace(buffer, idx):
    while idx < len(buffer) and is_whitespace(buffer[idx]):
        idx += 1

    return idx


def ignore_comments(buffer, idx):
    # consume whitespace
    idx = ignore_whitespace(buffer, idx)

    if idx < len(buffer) and buffer[idx] == FWD_SLASH:
        token = bytes([buffer[idx], buffer[idx+1]])
        # check single-line
        if token == LINE_COMMENT:
            idx += 2
            while idx < len(buffer) and buffer[idx] not in CR_LF:
                idx += 1
        # check multi-line
        elif token == START_BLOCK_COMMENT:
            idx += 2
            while token != CLOSE_BLOCK_COMMENT:
                if idx < len(buffer)+1 and buffer[idx] == ASTERISK:
                    token = bytes([buffer[idx], buffer[idx+1]])
                    idx += 2
                else:
                    idx += 1

            while buffer[idx] in WHITESPACE:
                idx += 1

    return idx


def iterate(tup_coll):
    length = None
    for l in tup_coll:
        if not length:
            length = len(l)
            continue
        if len(l) != length:
            # invalid iteration - lengths not equal
            raise IndexError("collection lengths not equal")

    idx = 0
    while idx < length:
        tpl = []
        for l in tup_coll:
            tpl.append(l[idx])

        yield tuple(tpl)

        idx += 1


def is_digit(buffer):
    digits = bytes(b'0123456789')
    idx = 0
    length = len(buffer)
    digit = True
    has_decimal = False

    if buffer.startswith(b'-'):
        idx += 1

    while idx < length and digit:
        digit = buffer[idx] in digits
        if not digit and buffer[idx] != 46:       # '.'
            break

        if not has_decimal:
            if buffer[idx] == 46:
                has_decimal = True
                digit = digit or True
        elif has_decimal and buffer[idx] == 46:
            digit = digit and False

        idx += 1

    return digit


def is_collection(candidate):
    import collections
    return not isinstance(candidate, str) and isinstance(candidate, collections.Sequence)


def read_text(buffer, idx, escapes=True):
    value = bytearray()

    while buffer[idx] != DBL_QUOTE:
        # skip '\'
        if buffer[idx] == ESCAPE:
            if not escapes:
                value.append(ESCAPE)

            idx += 1

        value.append(buffer[idx])
        idx += 1

    return value, idx


def split(buffer):
    """
    Splits buffer on ',' yielding bytearray parts

    :param buffer: buffer
    :type buffer: bytearray

    :return:
    """
    idx = 0
    length = len(buffer)
    part = bytearray()
    # assumption: if count is incremented then can assume last element can be yielded
    count = 0

    while idx < length:
        if buffer[idx] == DBL_QUOTE:
            idx += 1
            temp, idx = read_text(buffer, idx, escapes=False)
            part += temp
            idx += 1
            continue
        if buffer[idx] == LIST_DELIM:
            idx += 1

            yield part
            count += 1

            part.clear()
            if is_whitespace(buffer[idx]):
                idx += 1
                continue

        part.append(buffer[idx])
        idx += 1

    if count > 0 and len(part):
        yield part

        part.clear()


def decode_value(value):
        """
        Determines if there are any special results expected from the formatting of the value:
            bytearray(b'w:500 h:300') expects to return a tuple with 'w' and 'h' attributes and
            nodes of 500 & 300 respective
        :param value:
        :type value: bytearray

        :return:
        """
        idx = 0
        length = len(value)
        temp = bytearray()

        result = None

        if len(value.split(b',')) > 1:
            result = []
            for p in split(value):
                result.append(decode_value(p))

        if result and len(result):
            return result

        if is_digit(value):
            if len(value.split(b'.')) > 1:
                result = float(value)
            elif int(value):
                result = int(value)

        if result:
            return result

        tags, nodes = ([], [])
        while idx < length:
            idx = ignore_whitespace(value, idx)

            if value[idx] == TAG_DELIM:
                tags.append(temp.decode())
                temp.clear()
                idx += 1
                idx = ignore_whitespace(value, idx)

                while idx < length and not is_whitespace(value[idx]):
                    if value[idx] == DBL_QUOTE:
                        idx += 1
                        temp, idx = read_text(value, idx)
                        idx += 1

                        nodes.append(temp.decode())
                        temp.clear()

                        continue

                    temp.append(value[idx])
                    idx += 1

                if len(temp):
                    nodes.append(decode_value(temp))
                    temp.clear()

                idx += 1
                continue

            temp.append(value[idx])
            idx += 1

        if len(tags) and len(nodes):
            node_set = {}
            i = 0
            for k, v in iterate((tags, nodes)):
                node_set.update({k: nodes[i]})
                i += 1

            return node_set

        if len(temp) > 0:
            return temp.decode()

        if result:
            return result

        return value.decode()
