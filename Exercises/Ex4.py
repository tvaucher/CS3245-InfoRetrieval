from collections import Counter
from nltk.book import text1
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

stemmer = PorterStemmer()
print("Top 5 Stem")
for stem, count in Counter([stemmer.stem(w) for w in text1 if w.isalpha()]).most_common(5):
    print(f"{stem} : {count}")

print("\nTop 5 Words")
for word, count in Counter([w for w in text1 if w.isalpha()]).most_common(5):
    print(f"{word} : {count}")

print("\nLet's remove the stop words !!!\n")
print("Top 5 Stem")
for stem, count in Counter([stemmer.stem(w) for w in text1 if w.isalpha()
                                   and w not in stopwords.words("english")]).most_common(5):
    print(f"{stem} : {count}")

print("\nTop 5 Words")
for word, count in Counter([w for w in text1 if w.isalpha() 
                                   and w not in stopwords.words("english")]).most_common(5):
    print(f"{word} : {count}")
