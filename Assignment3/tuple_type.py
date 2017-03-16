"""
Module containing NamedTuple to simplify the communication via Pickle
Tuples:
    Entry: an entry of the dictionary, containing the frequency, the offset
            size of the list corresponding inside the postings
    Term: an entry of the posting, containing the term frequency and weight
            inside a given document
"""
from collections import namedtuple

Entry = namedtuple("Entry", ['frequency', 'offset', 'size'])
Entry.__new__.__defaults__ = (0, 0, 0)
Term = namedtuple("Term", ['frequency', 'weight'])
