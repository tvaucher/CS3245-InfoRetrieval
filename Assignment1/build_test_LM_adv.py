#!/usr/bin/python
import getopt
import sys
import string

from model import Model

# "Constants" declaration
MAX_IGNORE = 60  # Max percentage of gram to be ignored for a line to be considered inside the model
# global vars
ngram_size = 4  # Number of tokens per gram
padding_size = 3  # Size of the padding (usually ngram - 1)
invalid_token = '\r\n'  # Token to ignore during the tokenization
transform_line = lambda x: x  # Lambda to transform the text
smoothing = 1.  # Smoothing


def tokenize(line, n):
    """
    Creates a list of tokens (character based) with a padding at the beginning and the end
    ===
    params
        * line the line to tokenize
        * n the size of the padding
    return a list of tokens
    """
    assert n >= 0
    return [None] * n + [c for c in line if c not in invalid_token] + [None] * n

tokenizer = tokenize


def create_grams(tokens, n):
    """
    Creates an iterable of ngram (n in parameter) for a list of tokens.
    ===
    params
        * tokens the list of tokens to transform
        * n the size of the ngram
    return an iterable (zip) of ngrams
    """
    assert n > 0
    return zip(*[tokens[i:] for i in range(n)])


def get_language(result, ignore_percentage):
    """
    Finds the most probable language in a dict of (language, log. probability of the language)
    If the percentage of ignored ngrams was too big,
    the language of the entry is probably not included
    ===
    params
        * result a dict of form (lang, proba)
        * ignore_percentage the percentage of ignored ngrams
    return the most probable language or "other" if not included
    """
    if ignore_percentage > MAX_IGNORE:
        return "other"
    else:
        return max(result, key=(lambda x: result[x]))


def build_LM(in_file):
    """
    build language models for each label
    each line in in_file contains a label and a string separated by a space
    """
    print('building language models...')
    # This is an empty method
    # Pls implement your code in below

    lm = Model(smoothing)

    with open(in_file, encoding="utf8") as in_file_lines:
        for line in in_file_lines:
            (language, l) = line.split(" ", 1)
            for gram in create_grams(tokenizer(transform_line(l), padding_size), ngram_size):
                lm.add_gram(gram, language)

    return lm


def test_LM(in_file, out_file, lm):
    """
    test the language models on new strings
    each line of in_file contains a string
    you should print the most probable label for each string into out_file
    """
    print("testing language models...")
    # This is an empty method
    # Pls implement your code in below

    with open(in_file, encoding="utf8") as in_file_lines, open(out_file, mode="w", encoding="utf8") as out:
        i = 1
        for line in in_file_lines:
            # stores the language and it's log probability
            result = {k: 0 for k in LM.languages.keys()}
            ignored_gram, total_gram = 0, 0  # used to calculate the percentage of ignored gram
            for gram in create_grams(transform_line(tokenizer(transform_line(line), padding_size)), ngram_size):
                for lang in result.keys():
                    proba, ignored = lm.get_log_prob(gram, lang)
                    if not ignored:
                        result[lang] += proba
                    else:
                        ignored_gram += 1
                    total_gram += 1
            ignore_percentage = float(ignored_gram / total_gram * 100)
            print(i, result, ignore_percentage)
            i += 1
            print(get_language(result, ignore_percentage), line, end="", file=out)


def usage():
    print("usage: " + sys.argv[0] + ''' -b input-file-for-building-LM -t input-file-for-testing-LM
          -o output-file [-n gram-size -p padding-size --words
          --lower --rmspchar --inumber -s smoothing]''')

input_file_b = input_file_t = output_file = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'b:t:o:n:p:s:', ["words", "lower", "rmspchar", "inumber"])
except getopt.GetoptError as err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-b':
        input_file_b = a
    elif o == '-t':
        input_file_t = a
    elif o == '-o':
        output_file = a
    elif o == '-n':
        ngram_size = int(a)
        padding_size = ngram_size - 1
    elif o == '-p':
        padding_size = int(a)
    elif o == "--words":
        tokenizer = lambda line, n: [
            None] * n + ''.join(c for c in line if c not in invalid_token).split(" ") + [None] * n
    elif o == "--lower":
        transform_line = lambda x: x.lower()
    elif o == "--rmspchar":
        invalid_token += ".,:\\/!?_-#"
    elif o == "--inumber":
        invalid_token += string.digits
    elif o == "-s":
        smoothing = float(a)
    else:
        assert False, "unhandled option"
if input_file_b is None or input_file_t is None or output_file is None:
    usage()
    sys.exit(2)

LM = build_LM(input_file_b)
test_LM(input_file_t, output_file, LM)
