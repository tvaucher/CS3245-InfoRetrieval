import math

class Skiplist(object):
    def __init__(self, underlying_list):
        self.list = underlying_list
        self.frequency = len(underlying_list)
        self.step = int(math.floor(math.sqrt(self.frequency)))
        self.i = 0
    
    def __len__(self):
        return self.frequency

    def __iter__(self):
        self.i = 0
        return self
    
    def __next__(self, other=None):
        if self.i >= self.frequency:
            raise StopIteration
        
        out = self.list[self.i] # Normal case
        # check for potential skip
        if other and (self.i - 1) % self.step == 0:
            temp_i = self.i + self.step - 1
            if temp_i >= self.frequency: temp_i = self.frequency - 1 # If out of bond get the last valid one
            temp_out = self.list[temp_i] # Get the value of the skip pointer
            if temp_out <= other:
                # print(f"skipped to {temp_i + 1}")
                self.i = temp_i
                out = temp_out

        self.i += 1 # Prepare for next iteration
        return out
