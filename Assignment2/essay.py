import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from posting import Posting

try:
    import cPickle as pickle
except ImportError:
    import pickle

stemmer = PorterStemmer()
stopwords = {stemmer.stem(i) for i in stopwords.words("english")}
print({stemmer.stem(w.lower()) for w in
                {word for sent in sent_tokenize("government's\nbusiness")  # (re.sub("[-']", " ", file.read()))
                 for word in word_tokenize(sent)}})
with open("dictionary.txt", mode="rb") as dictionary_file,\
     open("postings.txt", mode="rb") as postings_file:
    dictionary = pickle.load(dictionary_file)
    posting = Posting(dictionary, postings_file)
    counter_numbers = 0
    counter_number_disksize = 0
    counter_stopwords = 0
    counter_disksize = 0
    counter_possessive = 0
    counter_dash = 0
    for k in dictionary:
        if re.match(r'[\d.,/]+', k): # Number and dates
            counter_numbers += 1
            counter_number_disksize += dictionary[k].size
        elif re.match(r'.*\'.*', k): # Containing an hypen
            # print(k, posting[k].list)
            counter_possessive += 1
        elif re.match(r'.*-.*', k): # Containing a dash
            # print(k, posting[k].list)
            counter_dash += 1
        elif k in stopwords: # Being a stopword
            counter_stopwords += 1
            counter_disksize += dictionary[k].size
    print("Dictionary Size:", len(dictionary))
    print("Number:", counter_numbers, counter_numbers/len(dictionary)*100.)
    print("Number Disk Space:", counter_number_disksize / 1024, "ko")
    print("Hyphens:", counter_possessive, counter_possessive/len(dictionary)*100.)
    print("Dash:", counter_dash, counter_dash/len(dictionary)*100.)
    print("Stopwords:", counter_stopwords, counter_stopwords/len(dictionary)*100., len(stopwords))
    print("Stopwords diskspace:", counter_disksize / 1024, "ko")

