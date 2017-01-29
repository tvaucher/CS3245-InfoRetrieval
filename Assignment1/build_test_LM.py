#!/usr/bin/python
import getopt
import sys
from typing import Dict, Iterable, List

from model import LanguageModel

# "Constants" declaration
NGRAM_SIZE = 4  # Number of tokens per gram
MAX_IGNORE = 60  # Max percentage of gram to be ignored for a line to be considered inside the model
INVALID_TOKEN = '\r\n'  # Token to ignore during the tokenization


def tokenize(line: str, n: int) -> List[str]:
    """
    Creates a list of tokens (character based) with a padding at the beginning and the end
    ===
    params
        * line the line to tokenize
        * n the size of the padding
    return a list of tokens
    """
    assert n >= 0
    return [None] * n + [c for c in line if c not in INVALID_TOKEN] + [None] * n


def create_grams(tokens: Iterable[str], n: int) -> Iterable[str]:
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


def get_language(result: Dict[str, int], ignore_percentage: float) -> str:
    """
    Finds the most probable language in a dict of (language, log. probability of the language)
    If the percentage of ignored ngrams was too big, the language of the entry is probably not included
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


def build_LM(in_file: str) -> LanguageModel:
    """
    build language models for each label
    each line in in_file contains a label and a string separated by a space
    """
    print('building language models...')
    # This is an empty method
    # Pls implement your code in below

    lm = LanguageModel()

    with open(in_file, encoding="utf8") as in_file_lines:
        for line in in_file_lines:
            (language, l) = line.split(" ", 1)
            for gram in create_grams(tokenize(l, NGRAM_SIZE - 1), NGRAM_SIZE):
                lm.add_gram(gram, language)

    return lm


def test_LM(in_file: str, out_file: str, lm: LanguageModel):
    """
    test the language models on new strings
    each line of in_file contains a string
    you should print the most probable label for each string into out_file
    """
    print("testing language models...")
    # This is an empty method
    # Pls implement your code in below

    with open(in_file, encoding="utf8") as in_file_lines, \
            open(out_file, mode="w", encoding="utf8") as out:
        for line in in_file_lines:
            # stores the language and it's log probability
            result = {k: 0 for k in lm.languages.keys()}
            ignored_gram, total_gram = 0, 0  # used to calculate the percentage of ignored gram
            for gram in create_grams(tokenize(line, NGRAM_SIZE - 1), NGRAM_SIZE):
                for lang in result.keys():
                    proba, ignored = lm.get_log_prob(gram, lang)
                    if not ignored:
                        result[lang] += proba
                    else:
                        ignored_gram += 1
                    total_gram += 1
            print(get_language(result, float(ignored_gram /
                                             total_gram * 100)), line, end="", file=out)


def usage():
    print("usage: " +
          sys.argv[0] + " -b input-file-for-building-LM -t input-file-for-testing-LM -o output-file")

input_file_b = input_file_t = output_file = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'b:t:o:')
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
    else:
        assert False, "unhandled option"
if input_file_b is None or input_file_t is None or output_file is None:
    usage()
    sys.exit(2)

LM = build_LM(input_file_b)
test_LM(input_file_t, output_file, LM)
