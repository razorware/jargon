import unittest

from jargon_py_tests.jargon_test_harness import *


def parse_jargon_file(file):
    file_map = FileMap(root_path)
    file_map.load(file)
    p = Parser()

    return p, p.parse(file_map.fso)


def get_key_nodes(collection, key):
    results = filter(lambda k: k[0] == key, collection)

    for k, n in results:
        yield n


def get_raw_nodes(collection, key):
    results = filter(lambda r: r.name == key, collection)

    for n in results:
        yield n


def first(iterator):
    item = None

    for i in iterator:
        item = i
        break

    return item


class ParserTests(unittest.TestCase):

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

    def test_build_empty_node(self):
        p, raw_nodes = parse_jargon_file("jargon_0.jss")
        nodes = p.build_nodes(raw_nodes)

        self.assertIsNotNone(nodes)
        self.assertTrue(isinstance(nodes, list))

        window = first(get_key_nodes(nodes, 'Window'))

        self.assertIsNotNone(window)
        self.assertTrue(window.value is None)

    def test_build_with_key_node(self):
        p, raw_nodes = parse_jargon_file("jargon_6.jss")
        nodes = p.build_nodes(raw_nodes)

        window = first(get_key_nodes(nodes, 'Window'))
        target = first(get_key_nodes(window.value, 'target'))

        self.assertEqual('sample.Sample', target.value)

    def test_build_node_with_escaped_string_value(self):
        p, raw_nodes = parse_jargon_file("jargon_8.jss")
        nodes = p.build_nodes(raw_nodes)

        window = first(get_key_nodes(nodes, 'Window'))

        self.assertEqual(2, len(window.value))

        title = first(get_key_nodes(window.value, 'title'))

        self.assertEqual("Memo: \"Lorem Ipsum\"", title.value)

    def test_build_node_with_multi_line_string_value(self):
        exp_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam a molestie ante. " \
                   "...Praesent sed sollicitudin enim, commodo interdum massa.\r\n" \
                   "Phasellus ullamcorper dolor in elit ultrices placerat. " \
                   "Etiam commodo mauris ut urna facucibus sagittis."

        p, raw_nodes = parse_jargon_file("jargon_9.jss")
        nodes = p.build_nodes(raw_nodes)

        window = first(get_key_nodes(nodes, 'Window'))
        memo = first(get_key_nodes(window.value, 'memo'))

        i = 0
        while i < len(exp_text):
            self.assertEqual(exp_text[i],
                             memo.value[i],
                             i)

            i += 1

if __name__ == '__main__':
    unittest.main()
