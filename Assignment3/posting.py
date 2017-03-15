"""
Module containing a datastructure based on a dictionary (Decorator pattern)
in order to get the value of the dictionary from the disk as you would do it
for a normal dictionary.
"""

from typing import Dict

from tuple_type import Entry

try:
    import cPickle as pickle
except ImportError:
    import pickle


class Posting(object):
    """
    Class representing the Posting dictionary
    can access the postings on disk for a given entry
    """

    def __init__(self, dictionary: Dict[str, Entry], post_file):
        """
        Initialize the datastructure given the dictionary and the postings file

        *params*
        - dictionary The dictionary mapping the key to a disk Entry
        - post_file The file (already open) containing the postings
        """
        self.dictionary = dictionary
        self.post_file = post_file

    def __getitem__(self, item: str):
        """
        Return the associated Skiplist to a key or an empty Skiplist
        if there's no mapping in the dictionary
        """
        if item in self.dictionary:
            value = self.dictionary[item]
            self.post_file.seek(value.offset)
            return pickle.loads(self.post_file.read(value.size))
        else:
            return dict()
