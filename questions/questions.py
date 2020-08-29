import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)
    
    quit = False
    while not quit:
        print("\nOptions:")
        print("1 - quit")
        print("2 - ask question")
        user_choice = input("Choice: ")
        if user_choice == "1":
            quit = True
        elif user_choice == "2":
            # Prompt user for query
            query = set(tokenize(input("\nQuery: ")))
            

            # Determine top file matches according to TF-IDF
            filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

            # Extract sentences from top files
            sentences = dict()
            for filename in filenames:
                for passage in files[filename].split("\n"):
                    for sentence in nltk.sent_tokenize(passage):
                        tokens = tokenize(sentence)
                        if tokens:
                            sentences[sentence] = tokens

            # Compute IDF values across sentences
            idfs = compute_idfs(sentences)
            
            # Determine top sentence matches
            matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
            for match in matches:
                print(match)
                
        


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    # Get files in directory
    files = os.listdir(os.path.join(directory))
    
    # Dictionary of filenames to their contents
    files_dict = dict()

    # Store contents in files dictionary
    for file in files:
        with open(os.path.join(directory, file)) as f:
            files_dict[file] = f.read()
   
    return files_dict



def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # Tokenize document
    tokens = nltk.word_tokenize(document)

    # List of words in document
    words = []

    # Remove punctuation and stopwords 
    for token in tokens:
        token = token.lower()
        if token not in string.punctuation and token not in nltk.corpus.stopwords.words("english"):
            words.append(token)
    
    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    # Get total number of documents
    total_documents = len(documents)
    
    # Store the idfs for each word in documents
    word_idfs = dict()

    # Calculate idf for each word in documents
    for lists in documents.values():
        for word in lists:
            word_appears = 0 
            if word not in word_idfs.keys():
                for lists2 in documents.values():
                    if word in lists2:
                        word_appears += 1
                word_idfs[word] = math.log((total_documents / word_appears))
   
    return word_idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    # Store tf-idf for each filename
    files_tfidfs = {
        name: 0.0
        for name in files.keys()
    }

    # Calculate tf-idf for each filename
    for word in query:
        for filename, list_words in files.items():
            if word in list_words:
                tf = list_words.count(word)
                idf = idfs[word]
                files_tfidfs[filename] += (tf * idf)
    
    # Sort files by tf-idf
    filenames_list = sorted(files_tfidfs, key=files_tfidfs.get, reverse=True)

    # Get n top files
    top_files = []
    for i in range(n):
        top_files.append(filenames_list[i])
    return top_files



def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    # Store IDF and Query density for each sentence
    sentence_rank = {
        sentence: [0.0, 0.0]
        for sentence in sentences.keys()
    }

    # Calculate IDFs for each sentence
    for word in query:
        for sentence, words in sentences.items():
            if word in words:
                idf = idfs[word]
                sentence_rank[sentence][0] += idf

    # Calculate query density for each sentence
    for sentence, words in sentences.items():
        for word in words:
            if word in query:
                sentence_rank[sentence][1] += (1.0 / len(words))

    # Sort sentences by IDFs first, then query density
    sentence_order = sorted(sentence_rank, key=lambda k: (sentence_rank[k][0], sentence_rank[k][1]), reverse=True)
     
    # Get the n top sentences
    top_sentences = []
    for i in range(n):
        top_sentences.append(sentence_order[i])
    return top_sentences
    


if __name__ == "__main__":
    main()
