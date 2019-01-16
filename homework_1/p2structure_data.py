import sys
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from string import punctuation
import pickle


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("ERROR: pass in exactly one txt file to be tokenized.")

    print("opening file: " + sys.argv[1], file=sys.stderr)
    with open(sys.argv[1]) as f:
        print("reading file: " + sys.argv[1], file=sys.stderr)
        f = f.read()

    print("removing newlines", file=sys.stderr)
    f = re.sub(r'\n|\r', ' ', f)

    # set all words to lower-case, because capitalization is 
    # not important and this matches nltk.corpus.stopwords
    print("changing case to lower", file=sys.stderr)
    f = f.lower()

    print("tokenizing sentences", file=sys.stderr)
    tokens = sent_tokenize(f)
    # get rid of empty strings
    print("number of sentences:", len(tokens), file=sys.stderr)

    print("removing punctuation and tokenizing words", file=sys.stderr)
    for i, t in enumerate(tokens):
        tokens[i] = word_tokenize(tokens[i])
        tokens[i] = [t for t in tokens[i] if t[0] not in punctuation] # remove empties


    tokens = [t for t in tokens if t] # remove empties

    with open("p2_output.txt", "wb") as out:
        pickle.dump(tokens, out)
