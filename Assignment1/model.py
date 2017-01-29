#!/usr/bin/python
import math
from collections import defaultdict


class LanguageModel:
    """
    Class that implements the Language Model.
    Allows to flexibly add a new language and new grams
    Supports smoothing (default: add 1 smoothing)
    """

    def __init__(self, smoothing: float=1):
        """
        Creates the Language Model
        ===
        opt. params
            * smoothing the smoothing to apply. Must be bigger than 0
        """
        assert smoothing > 0
        self.languages = defaultdict(int)
        self.grams = defaultdict(lambda: defaultdict(int))
        self.smoothing = smoothing

    def add_gram(self, gram: str, lang: str):
        """
        Add a gram entry in the Language model
        Increment the specified gram count
        Also increment the language gram count
        ===
        params
            * gram the gram to add
            * lang the language to which the gram belongs
        """
        self.grams[gram][lang] += 1
        self.languages[lang] += 1

    def get_log_prob(self, gram: str, lang: str) -> float:
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
            return math.log((self.grams[gram][lang] + self.smoothing)
                            / (self.languages[lang] + len(self.grams) * self.smoothing)), False
