import sys
from os import path

__pkg_dir = None

if path.isdir("../jargon_py"):
    __pkg_dir = path.abspath("../jargon_py")
    sys.path.insert(0, __pkg_dir)

    import jargon
    import nodes


FileMap = jargon.FileMap
FSysObj = jargon.FSysObj
Parser = jargon.Parser
RawNode = nodes.RawNode

root_path = "../samples"
