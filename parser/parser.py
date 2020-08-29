import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to" | "until"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> SS | CS
SS -> NP VP
CS -> SS Conj SS | SS P SS | SS Conj VP
NP -> N | Det N | Det AP N | Det N PP | Det AP N PP 
AP -> Adj | Adj AP 
VP -> V | V NP | V PP | V NP PP | V Adv | Adv V | V PP Adv | Adv V NP
VP -> Adv V NP PP | Adv V PP | V NP Adv | V NP PP Adv
PP -> P NP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # List of words in sentence
    words = []
    # Split sentence into list of tokens
    tokens = nltk.word_tokenize(sentence)
    # Add the sentence's words to the list
    for token in tokens:
        if any(char.isalpha() for char in token):
            words.append(token.lower())
    
    return words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    # List of NP chunks
    np = []

    # Iterate through all subtrees of tree
    for subtree in tree.subtrees():
        # Get subtrees of the subtree
        sub_subtrees = subtree.subtrees()
        # Checks if subtree contains other NP as subtrees
        has_np_subtree = False
        # Add subtree to list of NP chunks iff it has label "NP"
        # and has no subtrees with label "NP"
        if subtree.label() == "NP":
            for i, child in enumerate(sub_subtrees):
                if i != 0 and child.label() == "NP":
                    has_np_subtree = True
            if not has_np_subtree:
                np.append(subtree)

    return np


if __name__ == "__main__":
    main()
