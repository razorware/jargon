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
