This is the README file for A0153040Y's submission
Email : E0025146@u.nus.edu

== General Notes about this assignment ==

/!\ Please note that this code is written in Python 3.6 and isn't Python 2.7.X (or below 3.5) compatible
Indexation part:
As the optimization of the indexation part is not a critical point of the application, I decided to simplify my code by using `shelve` as an helping tool for keeping everything on disk (Except a small part cached on memory taken care of by Shelf). After going through all the documents of to index, the dictionary and postings file is written on disk and the temporary Shelf deleted. The postings are stored one list after another using pickle, and we keep track of there offset, size and frequency inside the dictionary that is itself then wrote on disk using pickle.

NOTE: Actually, I left the shelf part in comment and use a simple in-memory dict because of an IVLE post stating that in-memory indexing was perfectily fine. The rest of the process remains the same.

Skip pointers:
I decided not to write my skip pointers on disk for two main reasons:
    - One that means that I would have to have a hand written complex data structure to store them. Which sounds like a bad idea since writting a complex data structre in anything but C sounds very inefficiant (know that we're using cPython and the core datastructure are written in a very efficiant C way)
    - Second is that a skip pointers is nothing else than a concept, that is for some index with index % space_pointer == 0, I have the choice of either index++ or index + space_pointer for getting the next element (in an AND operation)
Therefore, I rather created a SkipList (a list decorator), that implements the idea of Skip pointer while doing the AND operation

Searching:
For each query q in the query file, q is parsed and transformed into an AST using Shunting Yard algorithm. Then the AST is evaluated bottom-up using recursion and the result is written in the output file

Optimization:
While writing the profiling my code using cProfile I came up with two conclusion:
- My supposedly O(1) iterator on SkipList for non AND operation wasn't that fast
- NOT operations are SLOW ! (being O(len(all_doc)))

Hence I made those modifications :
- Use the underlying list iterator of the SkipList decorator wherever we don't need the Skip Pointers
- Reduce the number of NOT operations

The second part is attained by applying De Morgan's law (reduce 2 NOT operation to 1) and supporting AND NOT merge which is O(max(len1, len2)).

== Files included with this submission ==

* index.py The main module for indexing the Reuter's data into a dictionary and a postings Files
* tuple_type.py The module containg the definition of on disk posting entry, used for Pickle
* search.py The main module for searching parse the arguments and executes the queries
* query.py The parsing module, creating a AST representation of a query
* tree.py The AST module, created by query and able to evaluate itself
* skiplist.py The Skip list module, implementing a Skip pointers datastructure
* posting.py The Posting module, implementing a simple interface from the in-memory dictionary and on-disk postings
* dictionary.txt The generated dictionary file
* postings.txt The generated postings file
* ESSAY.txt The file containing the answers for the essay questions
* essay.py The file containing some tests to answers the essay questions
* README.txt This current file, containing the acknowledgment of the guidelines

== Statement of individual work ==

Please initial one of the following statements.

[X] I, A0153040Y, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

== References ==

The lecture slides for AND merge and Skip pointers
Python doc for Python specific points

Shelf usage:
(PyMOTW)[https://pymotw.com/3/shelve/]
(Official doc)[https://docs.python.org/3/library/shelve.html]

Shunting yard alogrithm:
(Wikipedia)[https://en.wikipedia.org/wiki/Shunting-yard_algorithm]
(A Java implementation that inspired me)[https://www.klittlepage.com/2013/12/22/twelve-days-2013-shunting-yard-algorithm/]