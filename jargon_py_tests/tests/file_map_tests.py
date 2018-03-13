import unittest

from jargon_py_tests.jargon_test_harness import *


class FileMapTests(unittest.TestCase):

    def test_construct(self):
        file_map = FileMap(root_path)
        expected = path.abspath(root_path)

        self.assertEqual(expected, file_map.root)

    def test_fmap_load(self):
        file_map = FileMap(root_path)
        file_map.load("jargon_1.jss")
        file_obj = file_map.fso

        expected = path.join(path.abspath(root_path), "jargon_1.jss")

        self.assertEqual(expected, file_obj.file)

if __name__ == '__main__':
    unittest.main()
