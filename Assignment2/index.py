"""
This module is responsible of indexing a corpus of text inside a folder
The filenames to index must be unique integers

It relies on the `shelve` module to provide a on-disk persistent dictionary
Largely facilitating the indexing of the documents. As it's on disk, it only
use a very limited (and raisonnable) amount of memory. Once the computing of
the index is done, the `shelf` is reduce using (c)Pickle to specified file:
one for the dicitonary and one for the postings
"""
#!/usr/bin/python

import getopt
import os
import shelve
import sys
import time
import re
from tuple_type import Dictionary, Entry
from typing import Dict, Iterable, List, Set

from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

try:
    import cPickle as pickle
except:
    import pickle

DELIMITER = '/'
STEMMER = PorterStemmer()

def get_file_list(directory: str) -> Iterable[str]:
    """
    Create a sorted list of the files inside a directory
    ===
    params:
        directory: The directory to list the FileExistsError
    return:
        A sorted Iterable[str] containing the namefiles
    """
    return sorted(os.listdir(directory), key=int)


def generate_token(in_file: str) -> Set[str]:
    """
    Generate the token for a specified file to be added in the Dictionary/Postings.
    Reads the file then apply tokenization (sentence, word), case folding and stemming
    ===
    params:
        in_file: The file to generate the token for
    return:
        A Set[str] of the unique element to be added
    """
    with open(in_file, encoding="utf8") as file:
        return {STEMMER.stem(w.lower()) for w in
                {word for sent in sent_tokenize(re.sub("[-']", " ", file.read()))
                 for word in word_tokenize(sent)}}


def add_token(shelf: shelve.Shelf, token: str, in_file: int):
    """
    Add a specified token from a specified file in the temporary shelf
    ===
    params:
        shelf: The temporary shelf to add into
        token: The token to add into the shelf
        in_file: The file to which belong the token
    """
    if token not in shelf:
        shelf[token] = [in_file]
    else:
        temp = shelf[token]
        temp.append(in_file)
        shelf[token] = temp


def cleanup(tempFilename: str):
    """
    cleanup the temporary shelf
    ===
    params:
        tempFilename: The filename of the shelf
    """
    try:
        os.remove(tempFilename + ".bak")
        os.remove(tempFilename + ".dat")
        os.remove(tempFilename + ".dir")
    except:
        print("ERROR: Couldn't remove all Shelf files")


def index(directory: str, dict_file: str, post_file: str):
    """
    Core of the module. Index all the file of a specified directory into a couple
    of Dictionary and Postings. The Dictionary stores the list of all the document
    and of the entries (with their frequency, offset in the postings and size (in bytes))
    Whereas the Postings file stores the list of lists of documents. The postings are useless
    without the Dictonary.
    ===
    params:
        directory: The directory containing the file to index
        dict_file: The file that will contain the Dictionary
        post_file: The file that will contain the Postings
    """
    tempFilename = 'tmp' + str(int(time.time()))
    with shelve.open(tempFilename, flag="n") as shelf:
        file_list = get_file_list(directory)#[:10]
        shelf['__all__'] = file_list
        # Generate Dict
        for in_file in file_list:
            for token in generate_token(directory + in_file):
                add_token(shelf, token, int(in_file))

        # Write Postings
        dictionary = dict()
        with open(post_file, mode="wb") as postings_file:
            for key, value in shelf.items():
                offset = postings_file.tell()
                size = postings_file.write(pickle.dumps(value))
                dictionary[key] = Entry(len(value), offset, size)

        # Write Dictionary
        with open(dict_file, mode="wb") as dictionary_file:
            pickle.dump(dictionary, dictionary_file)

    cleanup(tempFilename)


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
