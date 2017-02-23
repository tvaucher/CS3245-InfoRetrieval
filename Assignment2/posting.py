import sys
try:
    import cPickle as pickle
except:
    import pickle


class Posting(object):
    def __init__(self, dicionary, post_file):
        self.dictionary = dicionary
        self.post_file = post_file
    
    def __getitem__(self, item):
        if item in self.dictionary:
            value = self.dictionary[item]
            self.post_file.seek(value.offset)
            return pickle.loads(self.post_file.read(value.size))
        else:
            return []
