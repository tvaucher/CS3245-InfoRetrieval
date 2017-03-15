"""
This module is responsible of indexing a corpus of text inside a folder
The filenames to index must be unique integers
"""
#!/usr/bin/python

import getopt
import os
import shelve
import sys
import time
import re
from tuple_type import Entry
from typing import Dict, Iterable, List, Set, Union
from itertools import groupby
from collections import defaultdict

from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

try:
    import cPickle as pickle
except ImportError:
    import pickle

DELIMITER = '/'
STEMMER = PorterStemmer()


def get_file_list(directory: str) -> Iterable[int]:
    """
    Create a sorted list of the files inside a directory

    *params*:
        - directory: The directory to list the FileExistsError
    *return*:
        - A sorted Iterable[int] containing the namefiles
    """
    return sorted(map(int, os.listdir(directory)))


def generate_token(in_file: str) -> Set[str]:
    """
    Generate the token for a specified file to be added in the Dictionary/Postings.
    Reads the file then apply tokenization (sentence, word), case folding and stemming

    *params*:
        - in_file: The file to generate the token for
    *return*:
        - A Set[str] of the unique element to be added
    """
    with open(in_file, encoding="utf8") as file:
        document_terms = sorted([STEMMER.stem(w.lower()) for w in
                [word for sent in sent_tokenize(file.read())  # (re.sub("[-']", " ", file.read()))
                 for word in word_tokenize(sent)]])
        document_length = len(document_terms)
        return document_length, map(lambda x: (x[0], len(list(x[1]))), groupby(document_terms))


def add_token(dictionary: Dict[str, Dict[int, int]], token, in_file: int):
    """
    Add a specified token from a specified file in the in-memory dictionary

    *params*:
        - dictionary: The in-memory to add into
        - token: The token to add into the dictionary
        - in_file: The file to which belong the token
    """
    (term, frequency) = token[0], token[1]
    dictionary[term][in_file] = frequency

def index(directory: str, dict_file: str, post_file: str):
    """
    Core of the module. Index all the file of a specified directory into a couple
    of Dictionary and Postings. The Dictionary stores the list of all the document
    and of the entries (with their frequency, offset in the postings and size (in bytes))
    Whereas the Postings file stores the list of lists of documents. The postings are useless
    without the Dictonary.

    *params*:
        - directory: The directory containing the file to index
        - dict_file: The file that will contain the Dictionary
        - post_file: The file that will contain the Postings
    """

    dict_builder = defaultdict(dict)
    dict_length = dict()
    file_list = get_file_list(directory)# [:10]
    # Generate Dict
    for in_file in file_list:
        (doc_len, tokens) = generate_token(directory + str(in_file))
        dict_length[in_file] = doc_len
        for token in tokens:
            add_token(dict_builder, token, in_file)

    # Write Postings
    dict_term = dict()
    with open(post_file, mode="wb") as postings_file:
        for key, value in dict_builder.items():
            offset = postings_file.tell()
            size = postings_file.write(pickle.dumps(value))
            dict_term[key] = Entry(len(value), offset, size)

    # Write Dictionary
    with open(dict_file, mode="wb") as dictionary_file:
        pickle.dump(len(file_list), dictionary_file)
        pickle.dump(dict_length, dictionary_file)
        pickle.dump(dict_term, dictionary_file)

def usage():
    """
    Print the usage of `index`
    """
    print("usage: " +
          sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file")


def main():
    """
    Main fonction of the module, check the argv and pass them to the index function
    """
    directory = dict_file = post_file = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
    except getopt.GetoptError as err:
        usage()
        sys.exit(2)
    for o, a in opts:
        if o == '-i':
            directory = a
        elif o == '-d':
            dict_file = a
        elif o == '-p':
            post_file = a
        else:
            assert False, "unhandled option"
    if directory is None or dict_file is None or post_file is None:
        usage()
        sys.exit(2)

    if not directory.endswith(DELIMITER):
        directory += DELIMITER
    index(directory, dict_file, post_file)

if __name__ == '__main__':
    main()
