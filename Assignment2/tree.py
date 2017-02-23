from posting import Posting
from skiplist import Skiplist

class Tree(object):
    def __init__(self, left, right, value):
        self.left = left
        self.right = right
        self.value = value
    
    def eval(self, dictionary, all_entry):
        left = self.left.eval(dictionary, all_entry)
        if self.right: right = self.right.eval(dictionary, all_entry)
        if self.value == 'AND':
            return and_merge(left, right)
        elif self.value == 'OR':
            return or_merge(left, right)
        else:
            return not_merge(left, all_entry)

    def __str__(self):
        return '[T ' + self.left.__str__() + ', ' + self.right.__str__() + ', ' + self.value + ']'

class Node(Tree):
    def __init__(self, left, right, value):
        Tree.__init__(self, left, right, value)

    def __str__(self):
        return '[N ' + self.left.__str__() + ', ' + self.right.__str__() + ', ' + self.value + ']'

class Leaf(Tree):
    def __init__(self, value):
        Tree.__init__(self, None, None, value)

    def eval(self, dictionary, all_entry):
        return dictionary[self.value]

    def __str__(self):
        return '[L ' + self.value + ']'

def and_merge(l1, l2):
    out = []
    if (len(l1) == 0 or len(l2) == 0):
        return Skiplist(out)
    i1, i2 = iter(l1), iter(l2)
    try:
        e1, e2 = next(i1, False), next(i2, False)
        while e1 and e2:
            if e1 == e2:
                out.append(e1)
                e1, e2 = next(i1, False),next(i2, False)
            elif e1 < e2:
                e1 = i1.__next__(e2)
            else:
                e2 = i2.__next__(e1)
    except StopIteration:
        print("StopIteration")
    
    return Skiplist(out)

def or_merge(l1: Skiplist, l2: Skiplist):
    out = []
    i1, i2 = iter(l1.list), iter(l2.list)
    e1, e2 = next(i1, False), next(i2, False)
    while e1 and e2:
        if e1 == e2:
            out.append(e1)
            e1, e2 = next(i1, False), next(i2, False)
        elif e1 < e2:
            out.append(e1)
            e1 = next(i1, False)
        else:
            out.append(e2)
            e2 = next(i2, False)
    if e1:
        out.append(e1)
        for e in i1:
            out.append(e)
    elif e2:
        out.append(e2)
        for e in i2:
            out.append(e)

    return Skiplist(out)

def not_merge(l1: Skiplist, l2: Skiplist):
    out = []
    i1, i2 = iter(l1.list), iter(l2.list)
    e1, e2 = next(i1, False), next(i2, False)
    while e1 and e2:
        if e1 == int(e2):
            e1, e2 = next(i1, False),next(i2, False)
        elif e1 < int(e2):
            e1 = next(i1, False)
        else:
            out.append(int(e2))
            e2 = next(i2, False)
    if e2:
        out.append(int(e2))
        for e in i2:
            out.append(int(e))

    return Skiplist(out)