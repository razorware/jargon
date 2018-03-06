import unittest

from jargon_py_tests.jargon_test_harness import *


class ParserScanTests(unittest.TestCase):

    def test_construction(self):
        self.assertIsNotNone(Parser())

    def test_empty_node(self):
        """
        Loads jargon_0.jss

            Window {}

        Node[0] .name = 'Window'
                .start = 8
                .nodes = None
        :return:
        """
        file_map = FileMap(root_path)
        file_map.load("jargon_0.jss")
        nodes = Parser().parse(file_map.fso)

        self.assertTrue(len(nodes) == 1)

        key_node = nodes[0]
        self.assertTrue(key_node.name == 'Window')
        self.assertTrue(key_node.start == 8)
        self.assertTrue(key_node.nodes is None)

    def test_crlf(self):
        starts = [8, 19, 31, 43, 59, 72]

        file_map = FileMap(root_path)
        file_map.load("jargon_1.jss")
        nodes = Parser().parse(file_map.fso)

        self.assertEqual(len(starts), len(nodes))

        idx = 0
        while idx < len(starts):
            key_node = nodes[idx]

            self.assertTrue(key_node.name == 'Window',
                            '\n[{idx}] exp: \'Window\'\n  act: \'{kn}\''.format(idx=idx,
                                                                                kn=key_node.name))
            self.assertTrue(key_node.start == starts[idx],
                            '\n[{idx}] exp: \'{exp}\'\n    act: \'{act}\''.format(idx=idx,
                                                                                  exp=starts[idx],
                                                                                  act=key_node.start))
            self.assertTrue(key_node.nodes is None)

            idx += 1

    def test_ignore_single_line_comments(self):
        file_map = FileMap(root_path)
        file_map.load("jargon_2.jss")
        nodes = Parser().parse(file_map.fso)

        self.assertTrue(len(nodes) == 1)

        key_node = nodes[0]
        self.assertTrue(key_node.name == 'Window')
        self.assertTrue(key_node.start == 41)
        self.assertTrue(key_node.nodes is None)

    def test_ignore_multi_line_comments(self):
        file_map = FileMap(root_path)
        file_map.load("jargon_3.jss")
        nodes = Parser().parse(file_map.fso)

        self.assertTrue(len(nodes) == 1)

        key_node = nodes[0]
        self.assertTrue(key_node.name == 'Window')
        self.assertTrue(key_node.start == 47)
        self.assertTrue(key_node.nodes is None)

    def test_nested_comments(self):
        names = ['Window', 'Window', 'Resources']
        starts = [44, 107, 195]

        file_map = FileMap(root_path)
        file_map.load("jargon_4.jss")
        nodes = Parser().parse(file_map.fso)

        self.assertEqual(len(starts), len(nodes))

        idx = 0
        while idx < len(starts):
            key_node = nodes[idx]

            self.assertTrue(key_node.name == names[idx],
                            '\n[{idx}] exp: \'{exp}\'\n  act: \'{act}\''.format(idx=idx,
                                                                                exp=names[idx],
                                                                                act=key_node.name))
            self.assertTrue(key_node.start == starts[idx],
                            '\n[{idx}] exp: \'{exp}\'\n    act: \'{act}\''.format(idx=idx,
                                                                                  exp=starts[idx],
                                                                                  act=key_node.start))
            self.assertTrue(key_node.nodes is None)

            idx += 1

    def test_empty_nested_node(self):
        file_map = FileMap(root_path)
        file_map.load("jargon_5.jss")
        nodes = Parser().parse(file_map.fso)

        parent = nodes[0]

        self.assertEqual(1, len(parent.nodes))

        child = parent.nodes[0]

        self.assertEqual('child', child.name)
        self.assertEqual(81, child.start)
        self.assertTrue(child.nodes is None)

    def test_populated_node(self):
        expected_name = "target"
        expected_start = 19

        file_map = FileMap(root_path)
        file_map.load("jargon_6.jss")
        nodes = Parser().parse(file_map.fso)
        parent = nodes[0]

        actual_child = parent.nodes[0]

        self.assertEqual(expected_name, actual_child.name)
        self.assertEqual(expected_start, actual_child.start)

    def test_populated_multi_node(self):
        expected_names = ["target", "size"]
        expected_starts = [19, 44]

        file_map = FileMap(root_path)
        file_map.load("jargon_7.jss")
        nodes = Parser().parse(file_map.fso)
        parent = nodes[0]

        self.assertEqual(2, len(parent.nodes))

        i = 0
        for n in parent.nodes:
            self.assertEqual(expected_names[i], n.name)
            self.assertEqual(expected_starts[i], n.start)

            i += 1

    def test_node_with_simple_string(self):
        exp_names = ['target', 'title']

        p, raw_nodes = parse_jargon_file("jargon_8.jss")
        window = first(get_raw_nodes(raw_nodes, 'Window'))

        self.assertTrue(2, len(window.nodes))

        i = 0
        for n in window.nodes:
            self.assertEqual(exp_names[i], n.name)
            self.assertIsNotNone(n.start)
            i += 1



if __name__ == '__main__':
    unittest.main()
