#!/usr/bin/python
import math


class Model:
    """
    Class that implements the Language Model.
    Allows to flexibly add a new language and new grams
    Supports smoothing (default: add 1 smoothing)
    """

    def __init__(self, smoothing=1):
        """
        Creates the Language Model
        ===
        opt. params
            * smoothing the smoothing to apply. Must be bigger than 0
        """
        assert smoothing > 0
        self.languages = dict()
        self.grams = dict()
        self.smoothing = smoothing

    def add_language(self, lang):
        """
        Add a new language to the model if it's not included yet
        ===
        params
            * lang the language to add
        """
        if lang not in self.languages:
            self.languages[lang] = 0

    def add_gram(self, gram, lang):
        """
        Add a gram entry in the Language model
        Increment the specified gram count
        Also increment the language gram count
        ===
        params
            * gram the gram to add
            * lang the language to which the gram belongs
        """
        if gram not in self.grams:
            self.grams[gram] = {lang: 1}
        elif lang not in self.grams[gram]:
            self.grams[gram][lang] = 1
        else:
            self.grams[gram][lang] += 1
        self.languages[lang] += 1

    def get_log_prob(self, gram, lang):
        """
        Get the logarithmitic probability for a specified gram in a specified language
        ===
        params
            * gram the gram to look for
            * lang the language to look for
        returns
            * the log probability (or 0 if not included)
            * a bool to tell if the gram has been ignored
        """
        if gram not in self.grams:
            return 0, True
        else:
            return math.log((self.grams[gram].get(lang, 0) + self.smoothing) / (self.languages[lang] + len(self.grams))), False
