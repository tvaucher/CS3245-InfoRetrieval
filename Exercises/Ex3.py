from nltk.book import *

print("Ending with ize")
print([w for w in set(text6) if w.endswith("ize")])
print([w for w in set(text6) if w[-3:] == "ize"])
print([w for w in set(text6) if w[len(w)-3:] == "ize"])

print("Containing the letter z")
print([w for w in set(text6) if 'z' in w])

print("Containing the sequence of letters pt")
print([w for w in set(text6) if 'pt' in w])

print("All lowercase letters except for an initial capital")
print([w for w in set(text6) if w.capitalize() == w and w.isalpha()])
