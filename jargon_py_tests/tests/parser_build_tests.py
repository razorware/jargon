import unittest

from collections import namedtuple

from jargon_py_tests.jargon_test_harness import *

Size = namedtuple("size", "w h")


class ParserBuildTests(unittest.TestCase):

    def test_build_empty_node(self):
        p, raw_nodes = parse_jargon_file("jargon_0.jss")
        root = p.build_nodes(raw_nodes)

        self.assertIsNotNone(root)
        self.assertTrue(isinstance(root, KeyNode))

        window = first(root.nodes['Window'])

        self.assertIsNotNone(window)
        self.assertFalse(len(window.nodes))

    def test_build_with_key_node(self):
        p, raw_nodes = parse_jargon_file("jargon_6.jss")
        root = p.build_nodes(raw_nodes)

        window = first(root.nodes['Window'])
        target = first(window.nodes['target'])

        self.assertTrue(len(target.nodes) == 0)
        self.assertEqual('sample.Sample', target.value)

    def test_build_node_with_escaped_string_value(self):
        p, raw_nodes = parse_jargon_file("jargon_8.jss")
        root = p.build_nodes(raw_nodes)

        window = first(root.nodes['Window'])

        self.assertEqual(2, len(window.nodes))

        title = first(window.nodes['title'])

        self.assertEqual("Memo: \"Lorem Ipsum\"", title.value)

    def test_build_node_with_multi_line_string_value(self):
        exp_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam a molestie ante. " \
                   "...Praesent sed sollicitudin enim, commodo interdum massa.\r\n" \
                   "Phasellus ullamcorper dolor in elit ultrices placerat. " \
                   "Etiam commodo mauris ut urna facucibus sagittis."

        p, raw_nodes = parse_jargon_file("jargon_9.jss")
        root = p.build_nodes(raw_nodes)

        window = first(root.nodes['Window'])
        memo = first(window.nodes['memo'])

        self.assertEqual(len(exp_text), len(memo.value))

        i = 0
        while i < len(exp_text):
            self.assertEqual(exp_text[i],
                             memo.value[i],
                             i)

            i += 1

    def test_build_with_packed_node_values(self):
        expected = Size(500, 300)

        p, raw_nodes = parse_jargon_file("jargon_10.jss")
        root = p.build_nodes(raw_nodes)

        # example:
        #   Window {
        #     target: sample.Sample;
        #     title:  "Memo: \"Lorem Ipsum\"";
        #     size:   w:500 h:300;
        #   }
        window = first(root.nodes['Window'])
        target = first(window.nodes['target'])
        title = first(window.nodes['title'])
        size = first(window.nodes['size'])

        self.assertIsNotNone(target)
        self.assertIsNotNone(title)
        self.assertIsNotNone(size)
        self.assertEqual(expected.w, size.value['w'])
        self.assertEqual(expected.h, size.value['h'])

    def test_node_not_exist(self):
        p, raw_nodes = parse_jargon_file("jargon_10.jss")
        root = p.build_nodes(raw_nodes)

        foo = first(root.nodes['foo'])
        window = first(root.nodes['Window'])

        self.assertIsNone(foo)
        self.assertIsNotNone(window)
        self.assertTrue('Window' in [n.name for n in root.nodes])

    def test_functional(self):
        p, raw_nodes = parse_jargon_file("jargon_11.jss")
        root = p.build_nodes(raw_nodes)

        # Window {
        #   target: sample.Sample;
        #   title:  "Sample 3: Basic Quick Start";
        #   size:   w:500 h:300;
        #   border: f:red b:black hf:red bd:0 th:1;
        #
        #   Grid {
        #     Label {
        #       text: "Hello, World!";
        #     }
        #   }
        # }
        window = first(root.nodes['Window'])
        title = first(window.nodes['title'])

        self.assertIsNotNone(title)

        grid = first(window.nodes['Grid'])
        label = first(grid.nodes['Label'])
        text = first(label.nodes['text']).value

        self.assertEqual("Hello, World!", text)


if __name__ == '__main__':
    unittest.main()
