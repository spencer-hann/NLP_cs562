import sys
from matplotlib import pyplot
from pickle import load as pload
from collections import defaultdict
from nltk.corpus import stopwords
stopwords = set(stopwords.words("english"))

def get_rank_list(unigrams):
    rank_list = [(entry[1], entry[0]) for entry in unigrams.items()]
    return sorted(rank_list, reverse=True)

def make_rank_freq_plot(rank_list, title):
    total = len(rank_list)
    freq_list = [count[0] / total for count in rank_list]

    pyplot.plot(freq_list, "r+")

    pyplot.xscale("log")
    pyplot.yscale("log")

    pyplot.xlabel("log(rank)")
    pyplot.ylabel("log(frequency)")

    pyplot.title(title)

    pyplot.show()

def get_top_20(rank_list):
    top_20 = [None] * 20
    i = 0
    for item in rank_list:
        if item[1] not in stopwords:
            top_20[i] = item
            i += 1
        else: continue
        if i == 20: break
    return top_20

def count_tokens(rank_list):
    num_tokens = 0
    for count,_ in rank_list:
        num_tokens += count
    return num_tokens

if __name__ == "__main__":
    with open("p3_unigrams_output.txt", "rb") as f:
        print("loading pickle from: p3_unigrams_output.txt", file=sys.stderr)
        unigrams = pload(f)

    print("creating/sorting rank_list", file=sys.stderr)
    rank_list = get_rank_list(unigrams)

    make_rank_freq_plot(rank_list,
            "Full Corpus Rank-Frequency Plot")
    print("\nIncluding stopwords: ")
    print("Number of types:  ", len(rank_list))
    print("Number of tokens: ", count_tokens(rank_list))

    top_20 = rank_list[:20]
    make_rank_freq_plot(rank_list[:20],
            "Top 20 Rank-Frequency Plot")

    #remove stopwords for rank list
    rank_list = [item for item in rank_list if item[1] not in stopwords]

    make_rank_freq_plot(rank_list,
            "Full Corpus Rank-Frequency Plot (excl. stopwords)")
    print("\nExcluding stopwords: ")
    print("Number of types:  ", len(rank_list))
    print("Number of tokens: ", count_tokens(rank_list))

    top_20_exlc_sw = get_top_20(rank_list)
    make_rank_freq_plot(top_20_exlc_sw,
            "Top 20  Rank-Frequency Plot (excl. stopwords)")

    print("\nTop 20 words:")
    print("\tincl.\texcl. stopwords")
    for i in range(20):
        print(str(i+1) + '\t' +
                top_20[i][1] + '\t' +
                top_20_exlc_sw[i][1]
            )
