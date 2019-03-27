#!/usr/bin/env python
# model1.py: Model 1 translation table estimation
# Steven Bedrick <bedricks@ohsu.edu> and Kyle Gorman <gormanky@ohsu.edu>

from __future__ import division
import numpy as np
import string
from tqdm import tqdm
from collections import defaultdict

def bitext(source, target):
    """
    Run through the bitext files, yielding one sentence at a time
    """
    for (s, t) in zip(source, target):
        yield ([None] + s.strip().split(), t.strip().split())
        # by convention, only target-side tokens may be aligned to a null
        # symbol (here represented with None) on the source side


default_source_file = "./data/hansards.36.ca.f.tok"
default_target_file = "./data/hansards.36.ca.e.tok"
class Model1(object):
    """
    IBM Model 1 translation table
    """

    def __repr__(self):
        return '{}()'.format(self.__class__.__name__)

    def __init__(self,
            source=default_source_file,
            target=default_target_file,
            ):
        self.source = list()
        self.target = list()
        self.t_words = set()

        null = "null"

        with open(source) as f:
            for line in f:
                self.source.append([null] + line.strip().split())

                for i,word in enumerate(self.source[-1]):
                    if word in string.punctuation:
                        del self.source[-1][i]

        with open(target) as f:
            for line in f:
                self.target.append(line.strip().split())

                for i,word in enumerate(self.target[-1]):
                    if word in string.punctuation:
                        del self.target[-1][i]
                    else:
                        self.t_words.add(word)

        naive_trans_prob = 1 / len(self.t_words)
        self.t = defaultdict(lambda:defaultdict(lambda:naive_trans_prob))

        assert len(self.source) == len(self.target)

        self.n_sentences = len(self.source)

    def train(self, n):
        """
        Perform n iterations of EM training
        """
        t = self.t

        parallel_sentences = list(zip(self.target,self.source))

        for i in range(n):

            count = defaultdict(lambda:defaultdict(int))
            s_total = dict()
            total = defaultdict(int)

            for E,F in parallel_sentences:
                # compute normalization
                for e in E:
                    t_e = t[e]
                    s_total[e] = 0
                    for f in F:
                        s_total[e] += t_e[f]

                # collect counts
                for e in E:
                    count_e = count[e]
                    t_e = t[e]
                    s_total_e = s_total[e]
                    for f in F:
                        tmp = t_e[f] / s_total_e
                        count_e[f] += tmp
                        total[f] += tmp

            # estimate probabilities
            for e in self.t_words:
                t_e = t[e]
                count_e = count[e]
                #for f in self.s_words:
                for f in count_e:
                    #if f not in count[e]: continue
                    t_e[f] = count_e[f] / total[f]

    def translate_word(self, s_word):
        best = 0
        ouput = None

        for t_word in self.t_words:
            if best < self.t[t_word][s_word]:
                best = self.t[t_word][s_word]
                output = t_word

        return output

if __name__ == '__main__':
    import doctest
    m = Model1()
    m.train(5)

    print("\nf words translated:")
    with open("./data/fwords.txt") as f:
        for word in f:
            word = word.strip()
            print(word,'\t',m.translate_word(word))

    doctest.testmod()
