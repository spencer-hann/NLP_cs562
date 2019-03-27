#!/usr/bin/env python -O
# basic BLEU score implementation
# Kyle Gorman <gormanky@ohsu.edu>

from __future__ import division

import numpy as np
from math import exp, log
from collections import Counter


MAX_GRAM_SIZE = 4


# helpers

def ngrams(tokens, order):
    """
    Generate n-grams of order `order`, with no padding
    """
    for i in range(len(tokens) - order + 1):
        yield tuple(tokens[i:i + order])

def bitext(source, target):
    """
    Run through the bitext files, yielding one sentence at a time
    """
    for (s, t) in zip(source, target):
        yield (s.strip().split(), t.strip().split())
        # this time, we don't want a null symbol


def BLEU(hypothesis, reference, n=MAX_GRAM_SIZE):
    """
    Compute BLEU for a hypothesis/reference sentence pair
    """
    p = np.zeros(n, dtype=np.float64)
    r_ngrams = Counter()
    h_ngrams = Counter()

    for i in range(n):
        for ngram in ngrams(reference, i):
            r_ngrams[ngram] += 1
        for ngram in ngrams(hypothesis, i):
            h_ngrams[ngram] += 1

        count = 0
        clipd = 0
        for ngram in h_ngrams:
            clipd += r_ngrams[ngram]
            count += h_ngrams[ngram]

        p[i] = log(clipd / count)

    bleu = exp(p.mean())

    if len(hypothesis) > len(reference):
        bleu *= exp(1- len(hypothesis) / len(reference))

    return bleu

