import sys
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from string import punctuation


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("ERROR: pass in exactly one txt file to be tokenized.")

    print("opening file: " + sys.argv[1], file=sys.stderr)
    with open(sys.argv[1]) as f:
        print("reading file: " + sys.argv[1], file=sys.stderr)
        f = f.read()

        print("removing newlines", file=sys.stderr)
        f = re.sub(r'\n|\r', ' ', f)

        print("tokenizing sentences", file=sys.stderr)
        tokens = sent_tokenize(f)
        print("number of sentences: " + str(len(tokens)), file=sys.stderr)

        print("removing punctuation and tokenizing words", file=sys.stderr)
        table = str.maketrans(dict.fromkeys(punctuation))
        for i, t in enumerate(tokens):
            tokens[i] = t.translate(table) # remove punctuation
            tokens[i] = word_tokenize(tokens[i])

        for token in tokens: print(token)
