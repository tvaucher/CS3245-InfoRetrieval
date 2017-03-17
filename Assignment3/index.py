"""
This module is responsible of indexing a corpus of text inside a folder
The filenames to index must be unique integers
In this case we precompute the lnc weight for each document in order to
save time during search, by trading it for some disk space
"""
#!/usr/bin/python

import argparse
import os
import sys
from collections import defaultdict
from typing import Dict, Iterable, List, Tuple

from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

from tuple_type import Entry, Term
from utils import normalize, tf

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


def generate_token(in_file: str) -> List[Tuple[str, int]]:
    """
    Generate the token and token frequency for a specified file
    to be added in the Dictionary/Postings.
    Reads the file then apply tokenization (sentence, word), case folding and stemming

    *params*:
        - in_file: The file to generate the token for
    *return*:
        - A list of tuple term, frequency for the file
    """
    with open(in_file, encoding="utf8") as file:
        document_terms = [STEMMER.stem(w.lower()) for w in
                                 [word for sent in sent_tokenize(file.read())
                                  for word in word_tokenize(sent)]]
        term_len = defaultdict(int)
        for term in document_terms:
            term_len[term] += 1
        return term_len
        # return [(term, len(list(acc))) for (term, acc) in groupby(document_terms)]


def index(directory: str, dict_file: str, post_file: str):
    """
    Core of the module. Index all the file of a specified directory into a couple
    of Dictionary and Postings. The Dictionary stores the amount of documents
    and of the entries (with their frequency, offset in the postings and size (in bytes))
    Whereas the Postings file stores the list of lists of tuple document, frequency.
    The postings are useless without the Dictonary.

    *params*:
        - directory: The directory containing the file to index
        - dict_file: The file that will contain the Dictionary
        - post_file: The file that will contain the Postings
    """

    dict_builder = defaultdict(dict)
    file_list = get_file_list(directory)  # [:10]
    # Generate Dict
    for in_file in file_list:
        tokens = generate_token(directory + str(in_file))
        weighted_tf = normalize([tf(y) for (x, y) in tokens.items()])
        for ((term, freq), w_tf) in zip(tokens.items(), weighted_tf):
            dict_builder[term][in_file] = Term(freq, w_tf)

    # Write Postings
    dict_term = defaultdict(Entry)
    with open(post_file, mode="wb") as postings_file:
        for key, value in dict_builder.items():
            offset = postings_file.tell()
            size = postings_file.write(pickle.dumps(value))
            dict_term[key] = Entry(len(value), offset, size)

    # Write Dictionary
    with open(dict_file, mode="wb") as dictionary_file:
        pickle.dump(len(file_list), dictionary_file)
        pickle.dump(dict_term, dictionary_file)

def main():
    """
    Main fonction of the module, check the argv and pass them to the index function
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="directory-of-documents", required=True)
    parser.add_argument("-d", help="dictionary-file", required=True)
    parser.add_argument("-p", help="postings-file", required=True)
    args = parser.parse_args()

    directory = args.i
    if not directory.endswith(DELIMITER):
        directory += DELIMITER
    index(directory, args.d, args.p)

if __name__ == '__main__':
    main()
