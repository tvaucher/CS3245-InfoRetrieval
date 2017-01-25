#!/usr/bin/python

import sys

"""
This program is to compute the accuracy, given a file containing your results
and a file containing the correct results. 
"""

if len(sys.argv) != 3:
    print("usage: " + sys.argv[0] + " file-containing-your-results file-containing-correct-results")
    sys.exit(2)

correct = 0
cnt = 0
fh1 = open(sys.argv[1])
fh2 = open(sys.argv[2])
for line1 in fh1:
    line2 = fh2.readline()
    res1 = line1.split()[0]
    res2 = line2.split()[0]
    cnt += 1
    if res1 == res2:
        correct += 1
fh1.close()
fh2.close()

acc = correct * 100.0 / cnt
print("accuracy: %s / %s (%s%%)" % (correct, cnt, round(acc, 2)))
