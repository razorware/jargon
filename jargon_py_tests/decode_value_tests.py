import unittest

from jargon_py import decode_value


class DecodeValueTests(unittest.TestCase):

    def test_integer(self):
        expected = int(100)

        value = bytearray(b'100')

        self.assertEqual(expected, decode_value(value))

    def test_float(self):
        expected = float(3.14)

        value = bytearray(b'3.14')

        self.assertEqual(expected, decode_value(value))

    def test_list(self):
        expected = [100, "hello"]

        value = bytearray(b'100, hello')
        actual = decode_value(value)

        self.assertEqual(len(expected), len(actual))

        for i in [0, 1]:
            self.assertEqual(expected[i], actual[i])

    def test_tuple_list(self):
        expected = ("w h", [500, 300])

        value = bytearray(b'w:500 h: 300')
        actual = decode_value(value)

        self.assertEqual(expected[0], actual[0])

        for i in [0, 1]:
            self.assertEqual(expected[1][i], actual[1][i])

    def test_tuple_list_with_strings(self):
        expected = ("title greeting date", ["Test This", "hello, \"Dave\"", "1/1/2000"])

        value = bytearray(b'title:"Test This" greeting:"hello, \\"Dave\\"" date:1/1/2000')
        actual = decode_value(value)

        self.assertEqual(expected[0], actual[0])

        for i in [0, 1]:
            self.assertEqual(expected[1][i], actual[1][i])


if __name__ == '__main__':
    unittest.main()
