from collections import defaultdict
from itertools import count
import torch

BOS_SYM = '<BOS>'
EOS_SYM = '<EOS>'

def build_vocab(corpus):
    """
    Build an exhaustive character inventory for the corpus, and return dictionaries
    that can be used to map characters to indicies and vice-versa.

    Make sure to include BOS_SYM and EOS_SYM!

    :param corpus: a corpus, represented as an iterable of strings
    :returns: two dictionaries, one mapping characters to vocab indicies and another mapping idicies to characters.
    :rtype: dict-like object, dict-li]ke object
    """
    c2i = {BOS_SYM: 0, EOS_SYM: 1}
    i2c = [BOS_SYM, EOS_SYM]

    i = len(i2c)
    for sentence in corpus:
        for char in sentence:
            if char not in c2i:
                i2c.append(char)
                c2i[char] = i
                i += 1

    return c2i, i2c


def sentence_to_vector(s, vocab, pad_with_bos=False):
    """
    Turn a string, s, into a list of indicies in from `vocab`.

    :param s: A string to turn into a vector
    :param vocab: the mapping from characters to indicies
    :param pad_with_bos: Pad the sentence with BOS_SYM/EOS_SYM markers
    :returns: a list of the character indicies found in `s`
    :rtype: list
    """
    if pad_with_bos:
        i = 1
        ret = [None] * (len(s)+2)
        ret[0] = vocab[BOS_SYM]
        ret[-1] = vocab[EOS_SYM]
    else:
        i = 0
        ret = [None] * (len(s))

    for char in s:
        ret[i] = vocab[char]
        i += 1

    return ret


def sentence_to_tensor(s, vocab, pad_with_bos=False):
    """
    :param s: A string to turn into a tensor
    :param vocab: the mapping from characters to indicies
    :param pad_with_bos: Pad the sentence with BOS_SYM/EOS_SYM markers
    :returns: (1, n) tensor where n=len(s) and the values are character indicies
    :rtype: torch.Tensor
    """
    return torch.tensor([sentence_to_vector(s, vocab, pad_with_bos)])


def build_label_vocab(labels):
    """
    Similar to build_vocab()- take a list of observed labels and return a pair of mappings to go from label to numeric index and back.

    The number of label indicies should be equal to the number of *distinct* labels that we see in our dataset.

    :param labels: a list of observed labels ("y" values)
    :returns: two dictionaries, one mapping label to indicies and the other mapping indicies to label
    :rtype: dict-like object, dict-like object
    """
    l2i = dict()
    i2l = dict()

    i = 0
    for label in labels:
        if label not in l2i:
            l2i[label] = i
            i2l[i] = label
            i += 1

    return l2i, i2l
