import unittest

from jargon_py_tests.jargon_test_harness import *

from jargon_py.jargon import one, \
    child_tags

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

p, raw_nodes = parse_jargon_file("jargon_11.jss")
root = p.build_nodes(raw_nodes)


class NodeQueryTests(unittest.TestCase):

    def test_node_query_one(self):
        window = one(root['Window'])

        self.assertTrue(isinstance(window, KeyNode))

    def test_node_query_keys(self):
        children = child_tags(root)

        self.assertTrue(isinstance(children, list))
        self.assertTrue('Window' in children)

    def test_node_query_subkeys(self):
        children = ['target', 'title', 'size', 'border', 'Grid']
        elements = child_tags(root['Window'])

        self.assertEqual(len(children), len(elements))

    #   TODO: data queries
    # def test_node_query_many(self):
    #     p_temp, rn_temp = parse_jargon_file("jargon_data.jss")
    #     database = p_temp.build_nodes(rn_temp)
    #
    #     people = database['People']
    #     persons = query(people['person'], 'surname')


if __name__ == '__main__':
    unittest.main()
