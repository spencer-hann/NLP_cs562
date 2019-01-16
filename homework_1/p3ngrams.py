import sys
import dill
import pickle
from collections import defaultdict

# this is necessary because for some reason
# defaultdict(lamda:defaultdict(int)) can't be pickled
def _dd():
    return defaultdict(int)

def get_ngrams(tokens):
    unigrams = defaultdict(int)
    bigrams = defaultdict(_dd)

    for s in tokens:
        unigrams[s[0]] += 1
        for i in range(1, len(s)):
            unigrams[s[i]] += 1
            bigrams[s[i-1]][s[i]] += 1

    #del unigrams[None]
    return unigrams, bigrams

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("ERROR: pass in exactly one txt file to be parsed for token list.")

    with open("p2_output.txt", "rb") as f:
        print("loading pickle from: p2_output.txt", file=sys.stderr)
        tokens = pickle.load(f)

    print("creating n-grams", file=sys.stderr)
    unigrams, bigrams = get_ngrams(tokens)

    print("pickling...", file=sys.stderr)
    with open("p3_unigrams_output.txt", "wb") as f:
        pickle.dump(unigrams, f)
    with open("p3_bigrams_output.txt", "wb") as f:
        pickle.dump(bigrams, f)
