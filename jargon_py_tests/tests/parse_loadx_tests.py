import unittest

from jargon_py_tests.jargon_test_harness import *

from jargon_py.query import *
from jargon_py.jargon import load_bin


class ParseLoadXTests(unittest.TestCase):

    def test_load_bin(self):
        buffer = bytearray(b'Window { target: sample.Sample; title: "Hello, World"; size: w:500 h:300;}')
        root = load_bin(buffer)

        window = one(root['Window'])
        children = child_tags(window)

        self.assertTrue('target' in children)
        self.assertTrue('title' in children)
        self.assertTrue('size' in children)

        self.assertEqual("sample.Sample", one(window['target']).value)
        self.assertEqual("Hello, World", one(window['title']).value)

        size = one(window['size']).value

        self.assertEqual(500, size['w'])
        self.assertEqual(300, size['h'])

    def test_load_app(self):
        buffer = bytearray(b'application: n:"Sample App" t:views.sample_1;')
        root = load_bin(buffer)

        app = one(root['application'])
        attribs = app.value

        self.assertTrue(isinstance(attribs, dict))
        self.assertTrue('n' in attribs)
        self.assertTrue('t' in attribs)


if __name__ == '__main__':
    unittest.main()
