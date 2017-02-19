"""
Module containing NamedTuple to simplify the communication via Pickle
Tuples:
    Entry: an entry of the dictionary, containing the frequency, the offset
            size of the list corresponding inside the postings
    Dictionary: a tuple containing the list of file and the real dictionary
"""
from collections import namedtuple

Entry = namedtuple("Entry", ['frequency', 'offset', 'size'])
Dictionary = namedtuple("Dictionary", ['file_list', 'dict'])
