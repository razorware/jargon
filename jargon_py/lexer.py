# from jargon_py import *
# from jargon_py.operator import OrOp
#
#
# __grammar_file = 'jargon.grm'
#
#
# class Lexer:
#
#     @property
#     def definitions(self):
#         return self.__definitions
#
#     @property
#     def grammars(self):
#         return self.__grammars
#
#     def __init__(self, grammar_file):
#         with open(grammar_file, 'rb') as file:
#             self.__bytes = file.read()
#
#         self.__definitions = {}
#         self.__grammars = {}
#         self.__parse_grammar_file()
#
#     def __parse_grammar_file(self):
#         buffer = self.__bytes
#         idx = 0
#         length = len(buffer)
#
#         while idx < length:
#             tag, idx = self.__get_tag(idx)
#
#             while buffer[idx] == TAG_DELIM or is_whitespace(buffer[idx]):
#                 idx += 1
#
#             # if tag == b'CHARACTER':
#             #     pause = True
#
#             definition, idx = self.__get_definition(idx)
#
#             if idx < length:
#                 while (buffer[idx] == TAG_DELIM or
#                        buffer[idx] == LINE_TERM or
#                        buffer[idx] in WHITESPACE):
#                     idx += 1
#
#                     if idx >= length:
#                         break
#
#             self.__definitions.update({tag: definition})
#
#             # idx += 1
#
#     def __get_definition(self, idx):
#         line, end = self.__read_line(idx)
#         idx = 0
#         length = len(line)
#
#         func = None
#         while idx < length:
#             b = line[idx]
#             idx += 1
#
#             if idx < length and line[idx] == b'|'[0]:
#                 if not func:
#                     func = OrOp()
#                     func.left = lambda x: x == b
#                 else:
#                     func.right = func.execute
#
#         return func, end
#
#     def __read_line(self, idx):
#         line = bytearray()
#         buffer = self.__bytes
#         length = len(buffer)
#
#         while idx < length and buffer[idx] != LINE_TERM:
#             if buffer[idx] in WHITESPACE:
#                 idx += 1
#                 continue
#
#             line.append(buffer[idx])
#             idx += 1
#
#         return line, idx
#
#
# def __load_grammar():
#     from os import path
#
#     file_path = path.abspath(path.dirname(__file__))
#     file_path = path.join(file_path, __grammar_file)
#     lexer = Lexer(file_path)
#
#     return lexer.definitions
#
#
# Grammar = __load_grammar()
