import unittest

from jargon_test_harness import *


class FileMapTests(unittest.TestCase):

    def test_construct(self):
        fmap = FileMap(root_path)
        expected = path.abspath(root_path)

        self.assertEqual(expected, fmap.root)

    def test_fmap_load(self):
        fmap = FileMap(root_path)
        fmap.load("jargon_1.jss")
        fso = fmap.fso

        expected = path.join(path.abspath(root_path), "jargon_1.jss")

        self.assertEqual(expected, fso.file)

if __name__ == '__main__':
    unittest.main()
