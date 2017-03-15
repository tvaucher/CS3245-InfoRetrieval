"""
Module containing NamedTuple to simplify the communication via Pickle
Tuples:
    Entry: an entry of the dictionary, containing the frequency, the offset
            size of the list corresponding inside the postings
"""
from collections import namedtuple

Entry = namedtuple("Entry", ['frequency', 'offset', 'size'])
Term = namedtuple("Term", ['frequency', 'weight'])
