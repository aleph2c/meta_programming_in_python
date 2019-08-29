# Tree sitter example
from tree_sitter import Language, Parser
import pprint
def pp(item):
  pprint.pprint(item)

Language.build_library(
  # store the library in the `build` directory
  'build/my-languages.so',

  # Include one or more languages
  [
    'vendor/tree-sitter-python',
  ]
)

PY_LANGUAGE = Language('build/my-languages.so', 'python')
parser = Parser()
parser.set_language(PY_LANGUAGE)

tree = parser.parse(bytes("""
def foo():
  if bar:
    baz()
""", "utf-8"))

root_node = tree.root_node
assert root_node.type == 'module'
assert root_node.start_point == (1, 0)
assert root_node.end_point == (4, 0)
function_name_node = root_node.children[0]
# print(dir(function_name_node))
assert function_name_node.type == 'function_definition'
function_name_node = function_name_node.children[1]
assert function_name_node.type == 'identifier'
assert function_name_node.start_point == (1, 4)
assert function_name_node.end_point == (1, 7)

pp( root_node.sexp()) 


cursor = tree.walk()
assert cursor.node.type == 'module'
assert cursor.goto_first_child()
assert cursor.node.type == 'function_definition'
assert cursor.goto_first_child()
assert cursor.node.type == 'def'




