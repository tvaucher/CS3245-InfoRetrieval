from math import sqrt, log10 as log

def tf(term_frequency):
    if term_frequency == 0:
        return 0
    return 1 + log(term_frequency)

def idf(amount_doc, doc_frequency):
    if doc_frequency == 0:
        return 0
    return log(float(amount_doc/doc_frequency))

def normalize(l):
    norm = sqrt(sum([x*x for x in l], 0))
    if norm == 0:
        return l
    return [x/norm for x in l]
    
def normal_product(l1, l2):
    return sum([x*y for x, y in zip(l1, l2)], 0)