from __future__ import print_function

import visitor


class Person(object):
    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        visitor.visit(self)


class Pet(object):
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

    def accept(self, visitor):
        visitor.visit(self)


class DescendantsVisitor(object):
    def __init__(self):
        self.level = 0

    @visitor.on('member')
    def visit(self, member):
        pass

    @visitor.when(Person)
    def visit(self, member):
        print('person')

    @visitor.when(Pet)
    def visit(self, member):
        print('Pet')


v = DescendantsVisitor()

arr = [Pet('abc', 'def'), Person('abc'), Pet('abc', 'def')]

for item in arr:
    item.accept(v)
