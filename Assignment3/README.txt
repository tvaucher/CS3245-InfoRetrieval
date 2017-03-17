This is the README file for A0153040Y's submission
Email : E0025146@u.nus.edu

== General Notes about this assignment ==

/!\ Please note that this code is written in Python 3.6 and isn't Python 2.7.X (or below 3.5) compatible
Indexation part:
The indexation part is almost directly taken from assignment 2, that is in memory indexing using Pickle for on disk persistence.
I decided to compute the tf-idf for each term in each document (using lnc) in order to speed up the querying part (which is the critical part of the application)

Search part:
This one is a bit different than assignment 2. As we're doing full text search, I just split the query into tokens, compute the tf-idf (ltc) for the query term
and then apply cosine similarity, storing the intermediate results in Counter in order to retrieve easily the top K in the end

== Files included with this submission ==

* index.py The main module for indexing the Reuter's data into a dictionary and a postings Files
* tuple_type.py The module containg the definition of named tuples used by Pickle
* search.py The main module for searching parse the arguments and executes the queries
* posting.py The Posting module, implementing a simple interface from the in-memory dictionary and on-disk postings
* utils.py The module containing the function to compute tf-idf
* dictionary.txt The generated dictionary file
* postings.txt The generated postings file
* ESSAY.txt The file containing the answers for the essay questions
* README.txt This current file, containing the acknowledgment of the guidelines

== Statement of individual work ==

Please initial one of the following statements.

[X] I, A0153040Y, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

== References ==

Python doc for Python specific points
