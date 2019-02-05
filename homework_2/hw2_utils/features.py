from  hw2_utils.constants import OFFSET, TTR_ARRAY
import numpy as np

# deliverable 4.1
def get_token_type_ratio(counts):
    """
    Compute the ratio of tokens to types

    :param counts: bag of words feature for a song
    :returns: ratio of tokens to types
    :rtype float
    """
    if OFFSET in counts: del counts[OFFSET]
    if len(counts) < 1: return 0.0
    return sum(counts.values()) / len(counts)

# deliverable 4.2
def concat_ttr_binned_features(data):
    """
    Add binned token-type ratio features to the observation represented by data

    :param data: Bag of words
    :returns: Bag of words, plus binned ttr features
    :rtype: dict
    """
    for ttr in TTR_ARRAY: data[ttr] = 0

    ttr = get_token_type_ratio(data)
    # int() rounds toward 0, ttr always >= 0
    ttr = min(int(ttr), len(TTR_ARRAY)-1)

    data[TTR_ARRAY[ttr]] = 1

    return data
