import nltk
import sys
import re

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S

NP -> N | Det N | P Det N | AP N | Det Adj N
PP -> P NP
VP -> V | V NP | V NP PP | V PP
AP -> A | A AP

# AP -> A | A AP
# PP -> P NP
# NP -> N | Det NP | Det AP N
# VP -> V | V NP | V NP PP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)

# TEST
"""
test1 = 'Holmes sat in the armchair.'
test2 = 'Holmes sat in the red armchair.'
test3 = 'Holmes sat in the little red armchair.'
"""
def main():

    # # If filename specified, read sentence from file
    # if len(sys.argv) == 2:
    #     with open(sys.argv[1]) as f:
    #         s = f.read()

    # # Otherwise, get sentence as input
    # else:
    #     s = input("Sentence: ")

    with open('sentences/4.txt') as f:
        s = f.read()
    #s = input("Sentence: ")
    print(s)

    # Convert input into list of words
    s = preprocess(s)
    print(s)

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
    nltk.download('punkt_tab')
    word_list = []
    pattern = re.compile(r'[a-zA-Z]+')
    for w in nltk.word_tokenize(sentence):
        w = w.lower()
        result = pattern.search(w)
        if result:
            word_list.append(w)
    #print(word_list)
    return word_list


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    chuncks = []
    print('tree:', tree)
    print('tree.label():', tree.label())
    print('Iterate subtrees:')
    for st in tree.subtrees():
        print('st:', st)
        print('label:', st.label())
        if st.label() == 'NP':
            print('-> FOUND NP')
            # Check if there is label NP in some subtree of st
            np_found = False
            st_subtrees = [st1 for st1 in st.subtrees()]
            print('st_subtrees')
            print(st_subtrees)
            # st is itself subtree of st!
            for st1 in st_subtrees[1:]:
                if st1.label() == 'NP':
                    print('NP found in subtree')
                    np_found = True
            if not np_found:
                chuncks.append(st)
            #print('chuncks so far', chuncks)
        
        
        print('leaves:', st.leaves())
        print('- - - - - - - - - -')
        
    return chuncks


if __name__ == "__main__":
    main()
