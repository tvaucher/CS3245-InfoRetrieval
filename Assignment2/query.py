import sys
import re
from typing import Iterable, List
from nltk.stem import PorterStemmer
from tree import Tree, Node, Leaf

OPERATORS = {'(': 0, ')': 0, 'AND': 2, 'OR': 1, 'NOT': 3}
STEM = PorterStemmer()

def process_token(token: str) -> str:
    if token not in OPERATORS:
        return STEM.stem(token.lower())
    else:
        return token

def tokenize(query: str) -> Iterable[str]:
    return list(map(process_token, re.sub("\(", " ( ", re.sub("\)", " ) ", query)).split()))

def addNode(output, operator):
    if operator != 'NOT':
        right, left = output.pop(), output.pop()
        output.append(Node(left, right, operator))
    else:
        output.append(Node(output.pop(), None, operator))

def shunting_yard_AST(tokens: Iterable[str]) -> Tree:
    """
    1. read token
    - if operands => queue
    - if not op. o1 take o2 from op stack while op1 <= op2 and put o2 in out, then put o1 in stack
    - if ( put it on stack
    - if ) empty the stack in the queue until you find a ( (or error)
    2. when no more token
    - if still some tokens (but parenthesis => error) => queue
    """
    if len(tokens) == 0:
        return Leaf('__Empty__')
    output = []
    stack = []
    for token in tokens:
        if token not in OPERATORS:
            output.append(Leaf(token))
        elif token == '(':
            stack.append(token)
        elif token == ')':
            pop = ''
            while(len(stack) != 0 and pop != '('):
                pop = stack.pop()
                if pop != '(':
                    addNode(output, pop)
            if pop != '(':
                raise Exception("Mismatching parenthesis", pop, stack)
        else:
            while len(stack) != 0:
                pop = stack.pop()
                if OPERATORS[token] <= OPERATORS[pop]:
                    addNode(output, pop)
                else:
                    stack.append(pop)
                    break
            stack.append(token)

    while(len(stack) > 0):
        if stack[-1] in "()":
            raise Exception("Unexpected ( )")
        else:
            addNode(output, stack.pop())
    return output.pop()
