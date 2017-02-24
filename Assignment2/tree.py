"""
Module implementing a Abstract Syntax Tree in order to evaluate the constructed queries

Implements merges for the different type of boolean operator
"""
from posting import Posting
from skiplist import Skiplist


class Tree(object):
    """
    Tree class, superclass of Node and Leaf, a Tree represents a query
    Allow for evaluation of the queries in order to find the id that matches the query
    """

    def __init__(self, left: 'Tree', right: 'Tree', value: str):
        """
        Initialize a Tree with two children and a value

        *params*
            - left The left subtree
            - right The right subtree
            - value The current value, aka an operand or an operator
        """
        self.left = left
        self.right = right
        self.value = value

    def eval(self, dictionary: Posting, all_entry: Skiplist) -> Skiplist:
        """
        Recursively evaluate the Tree to return the list of document that results from the operation

        **Note**: NOT is by far the most expensive operation (on average) then I try to reduce
                  as much as possible it's usage
        Optimization:
            - De Morgan for NOT a AND NOT b or NOT a OR NOT b (one less NOT)
            - Support AND NOT without effectuing the NOT (a AND NOT b and NOT a AND b)

        *params*
            - dictionary The dict containing the entries and metadata of the postings
            - all_entry The list of all the doc identifiers

        *return*
            - a Skiplist containing the result of the operation
        """
        # the closest I (easly) get to lazy val (Scala) in python
        left = lambda: self.left.eval(dictionary, all_entry)
        right = lambda: self.right.eval(dictionary, all_entry)
        sub_left = lambda: self.left.left.eval(dictionary, all_entry)
        sub_right = lambda: self.right.left.eval(dictionary, all_entry)

        if self.value == 'AND':
            if self.left.value == 'NOT' and self.right.value == 'NOT':
                # NOT a AND NOT b => De Morgan's law NOT (a OR b)
                return not_merge(or_merge(sub_left(), sub_right()), all_entry)
            elif self.left.value == 'NOT':  # NOT a AND b
                return and_not_merge(right(), sub_left())
            elif self.right.value == 'NOT':  # a AND NOT b
                return and_not_merge(left(), sub_right())
            return and_merge(left(), right())
        elif self.value == 'OR':
            if self.left.value == 'NOT' and self.right.value == 'NOT':
                # NOT a OR NOT b => De Morgan's law NOT (a AND b)
                return not_merge(and_merge(sub_left(), sub_right()), all_entry)
            return or_merge(left(), right())
        else:
            return not_merge(left(), all_entry)

    def __str__(self) -> str:
        """ return a string representation of the Tree"""
        return '[T ' + self.left.__str__() + ', ' + self.right.__str__() + ', ' + self.value + ']'


class Node(Tree):
    """Subclass of Tree, made to contain an operator as value and 2 subtrees"""

    def __init__(self, left: Tree, right: Tree, value: str):
        """See parent"""
        Tree.__init__(self, left, right, value)

    def __str__(self) -> str:
        """See parent"""
        return '[N ' + self.left.__str__() + ', ' + self.right.__str__() + ', ' + self.value + ']'


class Leaf(Tree):
    """Subclass of Tree, made to contain an operand doesn't have subtree"""

    def __init__(self, value: str):
        """See parent"""
        Tree.__init__(self, None, None, value)

    def eval(self, dictionary: Posting, all_entry: Skiplist) -> Skiplist:
        """Override of parent, bottom of recursion returns the base doc id list"""
        return dictionary[self.value]

    def __str__(self) -> str:
        """See parent"""
        return '[L ' + self.value + ']'


def and_merge(l1: Skiplist, l2: Skiplist) -> Skiplist:
    """
    Merge 2 Skiplists based on the AND boolean operator logic
    using Skip pointers whenever possible

    *params*
        - l1 The first Skiplist
        - l2 The second Skiplist
    *return*
        - The merged Skiplist
    """
    out = []
    i1, i2 = iter(l1), iter(l2)
    try:
        e1, e2 = next(i1, False), next(i2, False)
        while e1 and e2:
            if e1 == e2:
                out.append(e1)
                e1, e2 = next(i1, False), next(i2, False)
            elif e1 < e2:
                e1 = i1.__next__(e2)
            else:
                e2 = i2.__next__(e1)
    except StopIteration:
        pass

    return Skiplist(out)


def and_not_merge(l1: Skiplist, l2: Skiplist) -> Skiplist:
    """
    Merge 2 Skiplists based on the AND NOT logic: l1 AND **NOT** l2

    *params*
        - l1 The first Skiplist
        - l2 The second Skiplist (being *negated*)
    *return*
        - The merged Skiplist
    """
    out = []
    i1, i2 = iter(l1.list), iter(l2.list)
    e1, e2 = next(i1, False), next(i2, False)
    while e1 and e2:
        if e1 == e2:
            e1, e2 = next(i1, False), next(i2, False)
        elif e1 < e2:
            out.append(e1)
            e1 = next(i1, False)
        else:
            e2 = next(i2, False)

    if e1:
        out.append(e1)
        for e in i1:
            out.append(e)

    return Skiplist(out)


def or_merge(l1: Skiplist, l2: Skiplist) -> Skiplist:
    """
    Merge 2 Skiplists based on the OR boolean operator logic
    Note: use the underlying list for performances

    *params*
        - l1 The first Skiplist
        - l2 The second Skiplist
    *return*
        - The merged Skiplist
    """
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


def not_merge(l1: Skiplist, l2: Skiplist) -> Skiplist:
    """
    Negated the l1 list given the total list of existing doc ids l2
    Note: use the underlying list for performances

    *params*
        - l1 The first Skiplist
        - l2 The list of all of the doc ids
    *return*
        - The negated Skiplist l1 based on l2
    """
    out = []
    i1, i2 = iter(l1.list), iter(l2.list)
    e1, e2 = next(i1, False), next(i2, False)
    while e1 and e2:
        if e1 == e2:
            e1, e2 = next(i1, False), next(i2, False)
        elif e1 < e2:
            e1 = next(i1, False)
        else:
            out.append(e2)
            e2 = next(i2, False)
    if e2:
        out.append(e2)
        for e in i2:
            out.append(e)

    return Skiplist(out)
