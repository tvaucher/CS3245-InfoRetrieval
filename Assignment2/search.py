"""
This module is the core of the second part of the assignment and allows to perform
the queries contained in a files using a dictionary and a postings file as well
as a AST logic in order to evaluate the queries
"""

import getopt
import sys
# import time

from posting import Posting
from query import shunting_yard_AST, tokenize

try:
    import cPickle as pickle
except ImportError:
    import pickle

def search(dict_file: str, post_file: str, query_in: str, query_out: str):
    """
    Open all the file and the load the dictionary and the list of all the documents id
    Then, parse each query and create the respective AST that can evaluate itself
    Finally, print the query result in the out file

    *params*
        - dict_file The filename of the dictionary file
        - post_file The filename of the postings file
        - query_in The filename of the query file
        - query_out The filename of the output file
    """
    with open(dict_file, mode="rb") as dictionary_file,\
    open(post_file, mode="rb") as postings_file,\
    open(query_in, encoding="utf8") as q_in,\
    open(query_out, mode="w", encoding="utf8") as q_out:
        dictionary = pickle.load(dictionary_file)
        posting = Posting(dictionary, postings_file)
        file_list = posting['__all__']
        for query in q_in:
            print(" ".join(map(str, shunting_yard_AST(tokenize(query))
                               .eval(posting, file_list).list)), end='\n', file=q_out)
def usage():
    """
    Print the usage of `search`
    """
    print("usage: " + sys.argv[0] +
          " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results")


def main():
    """
    Main fonction of the module, check the argv and pass them to the index function
    """

    dict_file = post_file = query_in = query_out = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for o, a in opts:
        if o == '-d':
            dict_file = a
        elif o == '-p':
            post_file = a
        elif o == '-q':
            query_in = a
        elif o == '-o':
            query_out = a
        else:
            assert False, "unhandled option"
    if dict_file is None or post_file is None or query_in is None or query_out is None:
        usage()
        sys.exit(2)

    # t = time.perf_counter()
    search(dict_file, post_file, query_in, query_out)
    # print("search time", time.perf_counter() - t, "sec")

if __name__ == '__main__':
    main()
