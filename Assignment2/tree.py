from posting import Posting
from itertools import islice

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

def and_merge(l1, l2, step1=1, step2=1):
    # print("AND", l1, l2)
    out = []
    if (len(l1) == 0 or len(l2) == 0):
        return out
    #skip1 = islice(l1, step1, None, step1)
    #skip2 = islice(l2, step2, None, step2)
    i1, i2 = iter(l1), iter(l2)
    e1, e2 = next(i1, False), next(i2, False)
    #s1, s2 = next(skip1, l1[-1]), next(skip2, l2[-1])
    while e1 and e2:
        if e1 == e2:
            out.append(e1)
            #if e1 == s1:
            #    s1 = next(skip1, l1[-1])
            #if e2 == s2:
            #    s2 = next(skip2, l2[-1])
            e1, e2 = next(i1, False),next(i2, False)
        elif e1 < e2:
            #if (s1 <= e2):
            #    while (e1 < s1):
            #        print(f"l1 : skipping {e1} to {s1}")
            #        e1 = next(i1)
            #    s1 = next(skip1, l1[-1])
            e1 = next(i1, False)
        else:
            #if (s2 <= e1):
            #    while (e2 < s2):
            #        print(f"l2 : skipping {e2} to {s2}")
            #        e2 = next(i2)
            #    s2 = next(skip2, l2[-1])
            e2 = next(i2, False)
    return out

def or_merge(l1, l2):
    print("OR", l1, l2)
    out = []
    i1, i2 = iter(l1), iter(l2)
    e1, e2 = next(i1, False), next(i2, False)
    while e1 and e2:
        if e1 == e2:
            out.append(e1)
            e1, e2 = next(i1, False),next(i2, False)
        elif e1 < e2:
            out.append(e1)
            e1 = next(i1, False)
        else:
            out.append(e2)
            e2 = next(i2, False)
    if e1 :
        out.append(e1)
        for e in i1:
            out.append(e)
    elif e2:
        out.append(e2)
        for e in i2:
            out.append(e)

    return out

def not_merge(l1, l2):
    # print("NOT", l1)
    out = []
    i1, i2 = iter(l1), iter(l2)
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
    return out