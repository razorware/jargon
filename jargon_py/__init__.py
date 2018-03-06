TAB = 9         # '\t'
LF = 10         # '\n'
EOL = 13        # '\r'
SPACE = 32      # ' '
DBL_QUOTE = 34  # '"'
SGL_QUOTE = 39  # '\''
ASTERISK = 42   # '*'
FWD_SLASH = 47  # '/'
TAG_DELIM = 58  # ':'
LINE_TERM = 59  # ';'
ESCAPE = 92     # '\\'
OPEN = 123      # '{'
CLOSE = 125     # '}'

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

    while idx < length and buffer[idx] != TAG_DELIM:
        tag.append(buffer[idx])
        idx += 1

    # make tag immutable
    return bytes(tag), idx
