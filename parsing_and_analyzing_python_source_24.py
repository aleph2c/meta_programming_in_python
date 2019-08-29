# resources:
# https://www.mattlayman.com/blog/2018/decipher-python-ast/

# What you should recall while thinking about the ast library and Python (when
# you do your review, delete the answers under the numbers, then re-read the
# contents, then re-write the answers under the numbers):
# 1) You should be able to parse a string of code with the ast
import ast
tree = ast.parse('2 + 3 + 4 + x', mode='eval')
print(tree)
# 2) You should be able to look at the parsed result
import ast
tree = ast.parse('2 + 3 + 4 + x', mode='eval')
print(ast.dump(tree))
# 3) You should be able to load a file into the ast and build a tree
with open("parsing_and_analyzing_python_source_24.py", "r") as source:
  tree = ast.parse(source.read())
# 4) You should be able to describe the visitor pattern (this is new stuff)
# see example below.  The visitor pattern is applied when you want to use
# polymorphism in a class structure that doesn't support it.  I seem to remember
# a better way of doing this in this meta programming tutorial.  The class which
# will permit visitors needs to provide a method which can be generalized by
# another ancestral heirachy.  I don't like it, but that is mostly because I
# don't like inheritance and polymorphism.  The AST library uses the visitor
# word, but it may not be using the visitor pattern.

# 5) Know what search terms to use to find grammar elements required to use the
#    ast.NodeVisitor (read the greentreesnakes docs again)
# https://greentreesnakes.readthedocs.io/en/latest/nodes.html

# 6) You should be able to build your own class using the ast.NodeVisitor
class CodeAnalyzer(ast.NodeVisitor):

  def __init__(self):
    self.loaded = set()
    self.stored = set()
    self.deleted = set()

  def visit_Name(self, node):
    if isinstance(node.ctx, ast.Load):
      self.loaded.add(node.id)
    elif isinstance(node.ctx, ast.Store):
      self.stored.add(node.id)
    elif isinstance(node.ctx, ast.Del):
      self.deleted.add(node.id)

# 7) Do a small demo where you use the AST to re-write code

# 8) Compile an AST

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

# you can use the AST to hack code:
import ast
import inspect

# Node visitor that lowers globally accessed names into the function body as
# local variables to speed up execution time by 20 percent.  We want to be able
# to turn:
#   INCR = 1
#   @lower_names('INCR')
#   def countdown(n):
#     while n > 0:
#       n -= INCR
# into:
#   def countdown(n):
#     __global = globals()
#     INCR = __globals['INCR']
#     while n > 0:
#       n -= INCR

class NameLower(ast.NodeVisitor):
  def __init__(self, lowered_names):
    self.lowered_names = lowered_names

  def visit_FunctionDef(self, node):
    # compile some assignments to lower the constants
    code = '__globals = globals()\n'
    code += '\n'.join("{0} = __globals['{0}']".format(name)
                for name in self.lowered_names)
    code_ast = ast.parse(code, mode='exec')

    # inject the new statements into the function body
    node.body[:0] = code_ast.body

    # save the function object
    self.func = node

# Decorator (this code will get you fired) that turns global names into locals
def lower_names(*namelist):
  def lower(func):
    srclines = inspect.getsource(func).splitlines()
    # Skip source lines prior to the @lower_names decorator
    for n, line in enumerate(srclines):
      if '@lower_names' in line:
        break
    src = '\n'.join(srclines[n+1:])
    # Hack to deal with indented code
    if src.startwith((' ', '\t')):
      src = 'if 1:\n' + src
    top = ast.parse(src, mode='exec')

    # Transform the AST
    cl = NameLower(namelist)
    cl.visit(top)

    # Execute the modified AST 
    temp = {}
    exec(compile(top, "", "exec"), temp, temp)

    # Pull out the modified code object
    func.__code__ = temp[func.__name__].__code__
    return func



# Visitor pattern:
# Provide a method which can be used by an alien ancestry tree, so they can
# change the behavior of your class through polymorphism without affecting your
# class.
import random

# The Flower hierarchy cannot be changed (the visitor pattern is fixated on
# polymorphism)  We want to have "clean" polymorphic methods which are reliant
# upon inheritance.  I think the key insight why the ast uses this is because it
# can't affect the source of the ast... I honestly don't understand how this
# patten applies to the AST, but I understand (and dislike) the pattern.
class Flower:
  # this is the key to the pattern, accept is where you apply your alien methods
  def accept(self, visitor):  visitor.visit(self)
  def pollinate(self, pollinator): print(self, "pollinated by", pollinator)
  def eat(self, eater): print(self, "eaten by", eater)
  def __str__(self): return self.__class__.__name__

class Gladiolus(Flower): pass
class Runuculus(Flower): pass
class Chrysanthemum(Flower): pass

class Visitor:
  def __str__(self):
    return self.__class__.__name__

class Bug(Visitor): pass
class Pollinator(Visitor): pass
class Predator(Visitor): pass

# Add the ability to do "Bee" activities:
class Bee(Pollinator):
  def visit(self, flower):
    flower.pollinate(self)

# Add the ability to do "Fly" activities:
class Fly(Pollinator):
  def visit(self, flower):
    flower.pollinate(self)

# Add the ability to do "Worm" activities:
class Worm(Predator):
  def visit(self, flower):
    flower.eat(self)

def flowerGen(n):
  flowers = Flower.__subclasses__()
  for i in range(n):
    yield random.choice(flowers)()  # this is weird

# hacking the AST this doesn't work, fix it during a later review
# INCR = 1
# @lower_names('INCR')
# def countdown(n):
#   while n > 0:
#     n -= INCR
# 
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

  # It's almost as if I had a method to perform various "bug" operations on all
  # flowers.
  bee = Bee()
  fly = Fly()
  worm = Worm()
  for flower in flowerGen(10):
    flower.accept(bee)
    flower.accept(fly)
    flower.accept(worm)


  countdown(1000000)




