# IR-Project
A generalized vector space model using Karl Pearson's correlation coefficient. A project by Tanmaya Shekhar Dabral, Amala Deshmukh, Bhargav Kanuparthi and Naman Bajaj.

**Introduction:**

 The search-engine developed uses a modified form of the classic TF-IDF model. It was trained on the Cranfield dataset, which is a collection of abstracts of paper on aerodynamics and fluid dynamics. To run it, one must have the libraries “datrie” and “nltk”, which can be easily pip-installed. The yet_new_corpus1.tar.gz archive should be unpacked. To run, the shell3.2.py must be run from the same directory. The *.data files included have the various indexes stored in them, serialized via python pickling. The program comes with a simple command line interface, which prompts the user as required. “Exit” command exits the program. The scripts used and intermediate data has also been provided. 
****************************************************************
**Processing of files:** First the documents were tokenized using the nltk.word_tokenize() function to obtain a list of words for each document along with the term frequency. A filter was then applied to this list to remove all the punctuation marks. The words were then stripped of apostrophes and forward slashes as it was observed that they occurred frequently in the documents. Hyphenated words were dealt with separately as follows: Each hyphenated word was split into its components and each component was individually stored. The original word was also stored after removing the hyphens. The commas were removed from words given by the following regular expression [0-9]*,[0-9]*.  For abbreviations like m.i.t, the word was split and stored using ‘.’ as the delimiter along with the entire abbreviation. This was done to ensure if the surname of the author was given it would retrieve all the articles written by that person. 
The tokenized words were given as an input to the lemmatizer function.  If the word is of the form given by the regular expression ‘o\’ ([1-9]|[a-z])* then it is stored as a single term without the apostrophe. This was done to handle the case where the name of the author is of the form O’Brian.  The nltk.word_tokenize() function splits words of the form [a-z]*n’t as two separate words with the second one begin n’t. This word is a normalized to not and stored in the dictionary. The other general words were normalized using the PorterStemmer().stem_word() function of nltk.
When a query in a string format is passed on to the query handler it is tokenized and normalized using the same rules and above.
****************************************************************
**Query Processing:** The command line interface first asks the number of results the user is expecting then accepts a query and classifies as two types – A wildcard query or a normal free text query. Based on the presence of the wildcard character * the given query was handled with the respective function and the top results were displayed. The query is processed (tokenized, lemmatized) and converted into a vector with terms as basis. This is stored as a sparse scipy CSR matrix. This matrix is then multiplied with the matrix KP2, which is described in the next section.
****************************************************************
**The TF-IDF Model:** The TF-IDF model used is a partial implementation of the paper “Generalized Vector Space Model” by Wong et. al., which aims to do away with the presumption of orthogonality of terms that the Vector Space Model makes. To do so, the paper introduces a G matrix which has the term by term matrix, which is to be multiplied with the Term Frequency matrix. However, algorithm that the paper suggested used to calculate the similarity seemed too computationally intense. Therefore, to do so, a thresholded Karl-Pearson correlation between distributions of the terms among the documents was used. Owing to lack of computational power and time, the threshold was chosen so that the final matrix remained fairly sparse.
	The query and the TF matrix is represented as a scipy sparse matrix, so as to preserve space. As there was no predefined function to calculate Karl-Pearson coefficients of a sparse matrix, it had to be implemented from scratch. The CSR sparse matrix provides efficient multiplication of matrices, therefore, the entire score calculation process was converted into a series of matrix multiplications:
		S=q*G*T
Where q is the query row-vector (with idf included), G is the similarity matrix, and T is the final matrix of 1+log(tf). S then gives a vector having the similarity of all the documents with the given query. This can then be sorted and results be provided.
****************************************************************
**Wildcard queries:** The wildcard queries are handled by forming a Trie, which provides an efficient way to implement prefix queries. For this purpose the “datrie” library is used. A wrapper around it is made in the form of the class “wchandler” which handles prefix, postfix and midfix queries by maintaining two different tries, one having normal words, and one having reverse words.
	To handle query explosion due to the wildcards, we do the following:
1)	Allow only one wildcard per query
2)	If the total new queries (by taking each term returned by the trie) is less than some threshold, we run every query and merge the final lists.
3)	Else, we add all the terms to one query and search for it. (This might give less accurate results)
