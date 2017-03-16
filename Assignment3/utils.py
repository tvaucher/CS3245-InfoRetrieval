"""
Utilitary module implementing the tf-idf logic in 3 separate functions
- tf The term frequency weight function
- idf The inverse document frequency weight function
- normalize That normalize
"""

from math import sqrt, log10 as log


def tf(term_frequency: int) -> float:
    """
    Calculates the term frequency weight

    *params*
        - term_frequency The term frequency for a term
    *return*
        - the weight
    """
    if term_frequency == 0:
        return 0
    return 1 + log(term_frequency)


def idf(amount_doc: int, doc_frequency: int) -> float:
    """
    Calculates the inversed document frequency weight

    *params*
        - amount_doc The number of document
        - doc_frequency The document frequency for a term
    *return*
        - the weight
    """
    if doc_frequency == 0:
        return 0
    return log(float(amount_doc / doc_frequency))


def normalize(list_to_normalize):
    """
    Normalize a given list

    *params*
        - list_to_normalize The list to normalize
    *return*
        - the normalized list
    """
    norm = sqrt(sum([x * x for x in list_to_normalize], 0))
    if norm == 0:
        return list_to_normalize
    return [x / norm for x in list_to_normalize]
