TAB = 9             # '\t'
LF = 10             # '\n'
EOL = 13            # '\r'
SPACE = 32          # ' '
DBL_QUOTE = 34      # '"'
SGL_QUOTE = 39      # '\''
ASTERISK = 42       # '*'
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
