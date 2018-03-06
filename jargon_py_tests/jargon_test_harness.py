# import sys
from os import path
#
# __pkg_dir = None
#
# if path.isdir("../jargon_py"):
#     __pkg_dir = path.abspath("../jargon_py")
#     sys.path.insert(0, __pkg_dir)

from jargon_py.jargon import FileMap as fmap
from jargon_py.jargon import FSysObj as fso
from jargon_py.jargon import Parser as parser
from jargon_py.nodes import RawNode as raw_node

FileMap = fmap
FSysObj = fso
Parser = parser
RawNode = raw_node

root_path = "../samples"


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
