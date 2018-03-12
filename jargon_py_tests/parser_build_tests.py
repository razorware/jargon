import unittest

from collections import namedtuple

from jargon_py_tests.jargon_test_harness import *

Size = namedtuple("size", "w h")


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
        nodes = p.build_nodes(raw_nodes)

        # example:
        #   Window {
        #     target: sample.Sample;
        #     title:  "Memo: \"Lorem Ipsum\"";
        #     size:   w:500 h:300;
        #   }
        window = first(get_key_nodes(nodes, 'Window'))
        target = first(get_key_nodes(window.value, 'target'))
        title = first(get_key_nodes(window.value, 'title'))
        size = first(get_key_nodes(window.value, 'size'))

        self.assertIsNotNone(target)
        self.assertIsNotNone(title)
        self.assertIsNotNone(size)
        self.assertEqual(expected.w, size.value.w)
        self.assertEqual(expected.h, size.value.h)

    def test_functional(self):
        p, raw_nodes = parse_jargon_file("jargon_11.jss")
        nodes = p.build_nodes(raw_nodes)

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
        window = first(get_key_nodes(nodes, 'Window'))
        title = first(window['title'])

        self.assertIsNotNone(title)

        grid = first(window['Grid'])
        label = first(grid['Label'])
        text = first(label['text']).value

        self.assertEqual("Hello, World!", text)

    def test_tuple_builder(self):
        from collections import namedtuple

        name = "Foo"
        attribs = "bar baz goo tar taz"
        values = [100, "Hello", -1, "World", "1968"]

        tpl_cls = namedtuple(name, attribs)

        foo = tpl_cls(*values)

        self.assertEqual(values[0], foo.bar)
        self.assertEqual(values[1], foo.baz)
        self.assertEqual(values[2], foo.goo)
        self.assertEqual(values[3], foo.tar)
        self.assertEqual(values[4], foo.taz)

        print("\nWe always use '{baz}, {tar}' as an example.".format(baz=foo.baz, tar=foo.tar))


if __name__ == '__main__':
    unittest.main()
