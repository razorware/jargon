import unittest

from jargon_py.lexer import Grammar


class GrammarTests(unittest.TestCase):

    def test_grammar_construct(self):
        self.assertIsNotNone(Grammar)

    def test_letter_definition(self):
        exp_def = [bytearray(b'A'), bytearray(b'B'), bytearray(b'C'), bytearray(b'D'), bytearray(b'E'), bytearray(b'F'),
                   bytearray(b'G'), bytearray(b'H'), bytearray(b'I'), bytearray(b'J'), bytearray(b'K'), bytearray(b'L'),
                   bytearray(b'M'), bytearray(b'N'), bytearray(b'O'), bytearray(b'P'), bytearray(b'Q'), bytearray(b'R'),
                   bytearray(b'S'), bytearray(b'T'), bytearray(b'U'), bytearray(b'V'), bytearray(b'W'), bytearray(b'X'),
                   bytearray(b'Y'), bytearray(b'Z'), bytearray(b'a'), bytearray(b'b'), bytearray(b'c'), bytearray(b'd'),
                   bytearray(b'e'), bytearray(b'f'), bytearray(b'g'), bytearray(b'h'), bytearray(b'i'), bytearray(b'j'),
                   bytearray(b'k'), bytearray(b'l'), bytearray(b'm'), bytearray(b'n'), bytearray(b'o'), bytearray(b'p'),
                   bytearray(b'q'), bytearray(b'r'), bytearray(b's'), bytearray(b't'), bytearray(b'u'), bytearray(b'v'),
                   bytearray(b'w'), bytearray(b'x'), bytearray(b'y'), bytearray(b'z')]
        letters = Grammar[bytes(b'LETTER')]

        self.assertEqual(len(exp_def), len(letters))

        i = 0
        while i < len(exp_def):
            self.assertEqual(exp_def[i], letters[i])

            i += 1

    def test_hexadecimal_definition(self):
        exp_def = [bytearray(b'DECDIGIT'), bytearray(b'A'), bytearray(b'B'), bytearray(b'C'), bytearray(b'D'),
                   bytearray(b'E'), bytearray(b'F')]

        hexdigits = Grammar[bytes(b'HEXDIGIT')]

        self.assertEqual(len(exp_def), len(hexdigits))

        i = 0
        while i < len(exp_def):
            self.assertEqual(exp_def[i], hexdigits[i])

            i += 1

    def test_symbol_definition(self):
        #   { } , \; \: # \"
        exp_def = [bytearray(b'{'), bytearray(b'}'), bytearray(b','), bytearray(b';'), bytearray(b':'), bytearray(b'"')]

        symbols = Grammar[bytes(b'SYMBOL')]

        self.assertEqual(len(exp_def), len(symbols))

        i = 0
        while i < len(exp_def):
            self.assertEqual(exp_def[i], symbols[i], i)

            i += 1

    def test_character_definition(self):
        #   LETTER DECDIGIT _ #32 #10
        exp_def = [bytearray(b'LETTER'), bytearray(b'DECDIGIT'), bytearray(b'_'), bytearray(b' '), bytearray(b'\n')]

        characters = Grammar[bytes(b'CHARACTER')]

        self.assertEqual(len(exp_def), len(characters))

        i = 0
        while i < len(exp_def):
            self.assertEqual(exp_def[i], characters[i], i)

            i += 1


if __name__ == '__main__':
    unittest.main()
