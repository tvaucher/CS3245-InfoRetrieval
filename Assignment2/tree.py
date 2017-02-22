class Tree(object):
    def __init__(self, left, right, value):
        self.left = left
        self.right = right
        self.value = value

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

    def __str__(self):
        return '[L ' + self.value + ']'
