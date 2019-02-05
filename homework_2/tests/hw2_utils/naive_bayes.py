from hw2_utils.constants import OFFSET
from hw2_utils import clf_base, evaluation

import numpy as np
from collections import defaultdict, Counter
from itertools import chain
import math

from tqdm import tqdm

# deliverable 3.1
def get_corpus_counts(x,y,label):
    """
    Compute corpus counts of words for all documents with a given label.

    :param x: list of counts, one per instance
    :param y: list of labels, one per instance
    :param label: desired label for corpus counts
    :returns: defaultdict of corpus counts
    :rtype: defaultdict

    """
    rval = Counter()

    for song,era in zip(x,y):
        if era != label: continue
        rval.update(song)

    return defaultdict(int,rval)


# deliverable 3.2
def estimate_pxy(x,y,label,smoothing,vocab):
    """
    Compute smoothed log-probability P(word | label) for a given label. (eq. 2.30 in Eisenstein, 4.14 in J&M)

    :param x: list of counts, one per instance
    :param y: list of labels, one per instance
    :param label: desired label
    :param smoothing: additive smoothing amount
    :param vocab: list of words in vocabulary
    :returns: defaultdict of log probabilities per word
    :rtype: defaultdict of log probabilities per word

    """
    unigrams = get_corpus_counts(x,y,label)
    rval = defaultdict(float)#(-inf)) # zero in log space
    denominator = sum(unigrams.values())
    denominator += len(vocab) * smoothing
    denominator = np.log(denominator)

    for word,count in unigrams.items():
        rval[word] = np.log(smoothing + count)
        rval[word] -= denominator

    return rval


# deliverable 3.3
def estimate_nb(x,y,smoothing):
    """
    Estimate a naive bayes model

    :param x: list of dictionaries of base feature counts
    :param y: list of labels
    :param smoothing: smoothing constant
    :returns: weights, as a default dict where the keys are (label, word) tuples and values are smoothed log-probs of P(word|label)
    :rtype: defaultdict

    """
    labels = set(y)
    counts = defaultdict(float)#lambda:smoothing)
    doc_counts = defaultdict(float)#lambda: smoothing)
    #priors = defaultdict(float)
    weights = defaultdict(float)

    vocab = set()

    for dct,label in zip(x,y):
        #priors[label] += 1
        for word,count in dct.items():
            counts[label,word] += count
            vocab.add(word)

    for label in labels:
        #priors[label] /= len(y)
        for word in vocab: # summing loop
            counts[label,word] += smoothing
            doc_counts[label] += counts[label,word]
        counts[label,OFFSET] = 1 # offset is not smoothed
        doc_counts[label] += 1
        for word in vocab: # log-likelihood loop
            weights[label,word] = np.log(counts[label,word])
            weights[label,word] -= np.log(doc_counts[label])
            # from assignment: "offset feature will act as the prior"
            weights[label,word] += np.log(counts[label,OFFSET])#priors[label])

    return weights


# deliverable 3.4
def find_best_smoother(x_tr,y_tr,x_dv,y_dv,smoothers):
    """
    Find the smoothing value that gives the best accuracy on the dev data

    :param x_tr: training instances
    :param y_tr: training labels
    :param x_dv: dev instances
    :param y_dv: dev labels
    :param smoothers: list of smoothing values
    :returns: best smoothing value, scores
    :rtype: float, dict mapping smoothing value to score
    """
    scores = dict()
    max = smoothers[0]

    for val in tqdm(smoothers):
        theta_train = estimate_nb(x_tr,y_tr,val)
        predictions = clf_base.predict_all(x_dv,theta_train,y_dv)
        scores[val] = evaluation.acc(predictions, y_dv)
        if scores[val] >= scores[max]:
            max = val

    return max, scores

