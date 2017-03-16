"""
This module is the core of the second part of the assignment and allows to perform
the queries contained in a files using a dictionary and a postings file as well
as the lnc.ltc tf-idf logic for ranking
"""

import getopt
import sys
from collections import Counter
# import time
from itertools import groupby

from nltk.stem import PorterStemmer

from posting import Posting
from utils import *
from typing import Dict, DefaultDict, List
from tuple_type import Entry, Term

try:
    import cPickle as pickle
except ImportError:
    import pickle

STEMMER = PorterStemmer()
BEST_OF = 10


def query(q: str, dictionary: DefaultDict[int, Entry], posting: Posting, n: int) -> List[int]:
    """
    Split a given query, transform it into a document with tuple (term, frequency).
    Then, compute the lnc tf-idf for those tuples.
    Then, compute the score for each document containing one of those terms.
    Finally, return at most the BEST_OF best document id by score

    *params*
        - q The query string
        - dictionary The dictionary containing the document frequency of a term
        - posting The Postings dictionary containing a mapping of doc_id => weight for a given term
        - n The amount of document indexed

    *return*
        - A list with at most BEST_OF best document
    """
    tokens_freq = [(term, len(list(acc))) for (term, acc) in
                   groupby(sorted([STEMMER.stem(token.lower()) for token in q.split()]))]
    query_weight = normalize([tf(freq) * idf(n, dictionary[term].frequency)
                              for (term, freq) in tokens_freq])
    score = Counter()
    for ((term, _), q_weight) in zip(tokens_freq, query_weight):
        if q_weight > 0:
            for doc_id, (_, d_weight) in posting[term].items():
                score[doc_id] += q_weight * d_weight
    # score.most_common(BEST_OF)
    return [doc_id for (doc_id, _) in score.most_common(BEST_OF)]


def search(dict_file: str, post_file: str, query_in: str, query_out: str):
    """
    Open all the file and the load the dictionary and the amount of documents
    Then, call query function to calculate cos similarity
    Finally, print the query top results in the out file

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
        amount_doc = pickle.load(dictionary_file)
        dict_term = pickle.load(dictionary_file)
        posting = Posting(dict_term, postings_file)
        for q in q_in:
            print(" ".join(map(str, query(q, dict_term, posting, amount_doc))),
                  end='\n', file=q_out)


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
