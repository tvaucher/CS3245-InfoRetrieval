"""
This module is the core of the second part of the assignment and allows to perform
the queries contained in a files using a dictionary and a postings file as well
as the lnc.ltc tf-idf logic for ranking
"""

import argparse
import sys
from collections import Counter, defaultdict
from typing import DefaultDict, List

from nltk.stem import PorterStemmer

from posting import Posting
from tuple_type import Entry, Term
from utils import *

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
    query_terms = [STEMMER.stem(token.lower()) for token in q.split()]
    term_len = defaultdict(int)
    for term in query_terms:
        term_len[term] += 1
    query_weight = normalize([tf(freq) * idf(n, dictionary[term].frequency)
                              for (term, freq) in term_len.items()])
    score = Counter()
    for ((term, _), q_weight) in zip(term_len.items(), query_weight):
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
            print(*query(q, dict_term, posting, amount_doc),
                  end='\n', file=q_out)


def main():
    """
    Main fonction of the module, check the argv and pass them to the index function
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", metavar="dictionary-file",
                        help="Filename path of the dictionary", required=True)
    parser.add_argument("-p", metavar="postings-file",
                        help="Filename path of the postings", required=True)
    parser.add_argument("-q", metavar="file-of-queries",
                        help="Filename path of the queries", required=True)
    parser.add_argument("-o", metavar="out-file-results",
                        help="Filename path for the output file", required=True)
    args = parser.parse_args()

    search(args.d, args.p, args.q, args.o)

if __name__ == '__main__':
    main()
