"""
    Skiplist module implements a data-structure that mimick a List of DocId with Skip pointers
    Skip pointers are not stored on hardware or even on memory. My implementation of Skip pointers
    is more based on the concept that was presented in class. If you're trying to get the next
    from a position that has a skip pointer, you compare it with the value and if the skip pointer
    is smaller than the given value then skip to the pointer.

    This is mostly based on the fact that the underlying data structure is list (which is actually
    implemented as an array) that allows O(1) access time and insert, that allows to use list[i]
    for access
"""
import math
from typing import Iterator

class Skiplist(object):
    """
    Class Skiplist that represents a list with skip pointers
    """

    def __init__(self, underlying_list):
        """
        Initiates the Skip list, initiating the underlying list and the skip pointer step

        *params*:
            - underlying_list The underlying list of the datastructure
        """
        self.list = underlying_list
        self.frequency = len(underlying_list)
        self.step = int(math.floor(math.sqrt(self.frequency)))
        self.i = 0

    def __len__(self) -> int:
        """
        Returns the length of the underlying list
        """
        return self.frequency

    def __iter__(self) -> Iterator:
        """
        Initialize and return the iterator on the list
        """
        self.i = 0
        return self

    def __next__(self, other: int=None) -> int:
        """
        Returns the next element in the iterator.
        Note: If other is given, try to use skip pointer if node is skip pointer

        *params*:
            - other The value to compare to try to skip
        """
        if self.i >= self.frequency:
            raise StopIteration

        out = self.list[self.i]  # Normal case
        # check for potential skip
        if other and (self.i - 1) % self.step == 0:
            temp_i = self.i + self.step - 1
            if temp_i >= self.frequency:
                temp_i = self.frequency - 1  # If out of bond get the last valid one
            temp_out = self.list[temp_i]  # Get the value of the skip pointer
            if temp_out <= other:
                self.i = temp_i
                out = temp_out

        self.i += 1  # Prepare for next iteration
        return out
