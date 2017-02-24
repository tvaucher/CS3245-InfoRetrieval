import sys
import getopt
from tuple_type import Dictionary, Entry
from posting import Posting
from query import shunting_yard_AST, tokenize
from tree import Tree
from skiplist import Skiplist
import time

try:
    import cPickle as pickle
except:
    import pickle

def search(dict_file, post_file, query_in, query_out):
    with open(dict_file, mode="rb") as dictionary_file,\
    open(post_file, mode="rb") as postings_file,\
    open(query_in, encoding="utf8") as q_in,\
    open(query_out, mode="w", encoding="utf8") as q_out:
        dictionary = pickle.load(dictionary_file)
        posting = Posting(dictionary, postings_file)
        file_list = posting['__all__']
        first = True
        for query in q_in:
            if not first:
                print("\n", end="", file=q_out)
            else:
                first = False
            print(" ".join(map(str, shunting_yard_AST(tokenize(query))
                  .eval(posting, file_list))), end="", file=q_out)
def usage():
    """
    Print the usage of `search`
    """
    print("usage: " +
          sys.argv[0] + " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results")


def main():
    """
    Main fonction of the module, check the argv and pass them to the index function
    """
    t = time.perf_counter()
    dict_file = post_file = query_in = query_out = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
    except getopt.GetoptError as err:
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
    print("read arg time", time.perf_counter() - t, "sec")
    t = time.perf_counter()
    search(dict_file, post_file, query_in, query_out)
    print("search time", time.perf_counter() - t, "sec")

if __name__ == '__main__':
    t = time.perf_counter()
    main()
    print("main time", time.perf_counter() - t, "sec")