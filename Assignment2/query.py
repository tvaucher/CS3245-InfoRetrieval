"""
Module responsible of transforming an *input* query into a *Abstract Syntax Tree*
that can be used for further evaluation.

It separates the query terms (operands) from the operators (boolean logic)
and builds a AST based on Shunting Yard algorithm
"""
import re
from typing import Iterable

from nltk.stem import PorterStemmer

from tree import Leaf, Node, Tree

OPERATORS = {'(': 0, ')': 0, 'AND': 2, 'OR': 1, 'NOT': 3}
STEM = PorterStemmer()


def process_token(token: str) -> str:
    """
    Returns a lowercase stemmed version of an operand or the operator itself
    """
    if token not in OPERATORS:
        return STEM.stem(token.lower())
    else:
        return token


def tokenize(query: str) -> Iterable[str]:
    """
    Returns an Iterable of the tokens present inside the query
    """
    return list(map(process_token, re.sub(r'\(', ' ( ', re.sub(r'\)', ' ) ', query)).split()))


def add_node(output: Iterable[str], operator: str):
    """
    Adds a Tree node into the output stack and adds the previous Node as the operands
    """
    if operator != 'NOT':
        right, left = output.pop(), output.pop()
        output.append(Node(left, right, operator))
    else:
        output.append(Node(output.pop(), None, operator))


def shunting_yard_AST(tokens: Iterable[str]) -> Tree:
    """
    Takes a list of tokens and produces a Tree of operators with the query terms at the Leaf

    *Description of the algorithm*:
    1. read token
    - if operands => queue
    - if not op. o1 take o2 from op stack while op1 <= op2 and put o2 in out, then put o1 in stack
    - if ( put it on stack
    - if ) empty the stack in the queue until you find a ( (or error)
    2. when no more token
    - if still some tokens (but parenthesis => error) => queue
    """
    if len(tokens) == 0: # Support empty query
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
            while len(stack) != 0 and pop != '(':
                pop = stack.pop()
                if pop != '(':
                    add_node(output, pop)
            if pop != '(':
                raise Exception("Mismatching parenthesis", pop, stack)
        else:
            while len(stack) != 0:
                pop = stack.pop()
                if OPERATORS[token] <= OPERATORS[pop]:
                    add_node(output, pop)
                else:
                    stack.append(pop)
                    break
            stack.append(token)

    while len(stack) > 0:
        if stack[-1] in "()":
            raise Exception("Unexpected ( )")
        else:
            add_node(output, stack.pop())
    return output.pop()
