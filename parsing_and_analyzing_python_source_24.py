# resources:
# https://www.mattlayman.com/blog/2018/decipher-python-ast/

import pprint
def pp(item):
  pprint.pprint(item)
# you want to write programs that parse and analyze Python source code
# most programmers know that Python can evaluate and execute code provided in
# the form of a string.
x = 42
print(eval('2 + 3*4 + x'))

exec('for i in range(10): print(i)')

# however the AST module can be used to compile Python source code into an
# abstract syntax tree (AST) that can be analyzed.  For example:
import ast
ex = ast.parse('2 + 3+4 + x', mode='eval')
print(ex)
pp(ast.dump(ex))

top = ast.parse('for i in range(10): print(i)', mode='exec')
print(top)
pp(ast.dump(top))

# The easiest way to work with these nodes is to define a visitor class that
# implemtns various vist_NodeName() methods where NodeName() matches the node of
# interest.  Here is an example of such a class that records information about
# which names are loaded, stored, and deleted.
import ast

class CodeAnalyzer(ast.NodeVisitor):

  def __init__(self):
    '''This will create an ast visitor, or something that will run over each
       node in the AST.
    '''
    self.loaded = set()
    self.stored = set()
    self.deleted = set()

  def visit_Name(self, node):
    '''
    visit_<node type> method will run when the <node type> is seen by the
    visitor.  In this case we look at the Name and query the instance type of
    the name then add it to our sets
    '''
    if isinstance(node.ctx, ast.Load):
      self.loaded.add(node.id)
    elif isinstance(node.ctx, ast.Store):
      self.stored.add(node.id)
    elif isinstance(node.ctx, ast.Del):
      self.deleted.add(node.id)

if __name__ == '__main__':
  code = '''
for i in range(10):
  print(i)
del i
'''
  # Parse into an AST
  top = ast.parse(code, mode='exec')

  # Feed the AST to analyze name usage
  c = CodeAnalyzer()
  c.visit(top)
  print('Loaded: ', c.loaded)
  print('Stored: ', c.stored)
  print('Deleted: ', c.deleted)

