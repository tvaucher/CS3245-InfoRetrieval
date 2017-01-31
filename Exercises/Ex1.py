import string
import sys
import re
from collections import Counter

with open(sys.argv[1], encoding="utf8") as in_file:
    for word, occurence in Counter(sorted(re.sub('[' + string.punctuation + string.digits + ']', '', in_file.read().lower()).split())).most_common():
        print(f"{word} : {occurence}")
