import unittest

from jargon_py_tests.jargon_test_harness import *


class ParserBuildTests(unittest.TestCase):

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
