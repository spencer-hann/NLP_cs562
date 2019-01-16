from p3counting import get_rank_list, count_tokens
from pickle import load as pload
from numpy import log
from p3ngrams import _dd # cant load pickle without this :/
from collections import defaultdict

def load_ngrams():
    with open("p3_unigrams_output.txt", "rb") as f:
        unigrams = pload(f)
    with open("p3_bigrams_output.txt", "rb") as f:
        bigrams = pload(f)
    return unigrams, bigrams

def calc_PMI(unigrams, bigrams, threshold=100):
    pmi = defaultdict(lambda:None)

    # convert unigrams to probabilities, not counts
    total_tokens = 0
    for count in unigrams.values():
        total_tokens += count
    for word in unigrams:
        unigrams[word] /= total_tokens

    # calculate bigram probabilities from bigram 
    # counts while calculating PMIs
    for w1, inner_dict in bigrams.items():
        total = 0
        for count in inner_dict.values():
            total += count
        for w2, count in inner_dict.items():
            if count < threshold: continue
            #pmi[w1,w2] = log(count / total)
            #pmi[w1,w2] -= log(unigrams[w2])
            pmi[w1,w2] = count / total
            pmi[w1,w2] /= unigrams[w2]
    return pmi

def top_n_pmi(pmi, n=10):
    pmi = [(count,bigram) for bigram,count in pmi.items()]
    pmi = sorted(pmi, reverse=True)
    return pmi[:n]

if __name__ == "__main__":
    unigrams, bigrams = load_ngrams()

    pmi = calc_PMI(unigrams, bigrams)
    top_pmis = top_n_pmi(pmi,30)
    for pmi in top_pmis:
        print(pmi)
