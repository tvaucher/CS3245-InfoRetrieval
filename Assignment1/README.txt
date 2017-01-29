This is the README file for A0153040Y's submission

== General Notes about this assignment ==

/!\ Please note that this code is written in Python 3.6 and isn't Python 2.7.X (or below 3.5) compatible

Creation of the ngram :
    I decided to go for padding using None, during the creation of the grams (see more in Essay). The grams are created by zipping the list of tokens with itself

LanguageModel :
    The language model is abstracted in a class which allows a user to add a gram for a specified language and retrieve is probability.
    It's basically containing 2 dict. One to keep track of the different language present in the LM and the number of ngrams belonging to it. The other one use the gram as a key and contains the number of occurence of the gram for a given language.
    Actually those are defaultdict to reduce the number of line written in checking whether the key is in or not whatsoever (it'd like to provide my github to show the improvement but I guess it's not feasible :p). But mostly it provides flexibility ! You can decide to feed it any language you want. You're not limited to the 3 languages of this assignment, which makes it Reusable !

On identification :
    As suggested by prof Min, I use log based probability with on-the-fly computation to calculate my predicition.
    As we are summing negative log probability, the least negative (aka biggest) should be selected.
    But we have alien languages, I keep track of the number of ngram we ignored and if the percentage is above a cst (MAX_IGNORE = 60) we consider the language to be one that isn't contained in the LM.

== Files included with this submission ==

* build_test_LM.py contains the core of the assignment, performs the LM training and predicition of the languages
* model.py The file that contains the class LanguageModel that represents a language model with flexible entries and number of supported language
* build_test_LM_adv.py A similar version of the normal one with additional cmd line args for testing
* ESSAY.txt The file containing the answers for the essay questions
* README.txt This current file, containing the acknowledgment of the guidelines

== Statement of individual work ==

Please initial one of the following statements.

[Y] I, A0153040Y, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

== References ==

Prof Min for suggesting to use log probability

Python doc because I always forget some stuff x)

Python talks:
* (Raymond Hettinger - Transforming Code into Beautiful, Idiomatic Python)[https://www.youtube.com/watch?v=OSGv2VnC0go]
* (Raymond Hettinger - Beyond PEP 8 - PyCon 2015)[https://www.youtube.com/watch?v=wf-BqAjZb8M&t=3s]
* (Type Hints - Guido van Rossum - PyCon 2015)[https://www.youtube.com/watch?v=2wDvzy6Hgxg]
For better practice in Python. On how to make code better and more pythonic, more readable and maintainable
Especially the use of defaultdict that simplified the LanguageModel code quite a bit