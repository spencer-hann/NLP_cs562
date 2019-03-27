from tree import Tree
from collections import defaultdict, Iterable
import cython

example_input = "(TOP (NP (DT the) (NN teacher)) (VP (MD will) (VP (VB lecture) (NP (NN today) (PP (IN in) (NP (DT the) (NN lecture) (NN hall)))))) (. .))"

def pcfg(root,transform_tree=True):
    if type(root) is Tree:
        root = [root] # for for loop

    left_to_right = defaultdict(lambda:defaultdict(float))
    right_to_left = defaultdict(set)

    for r in root:
        if transform_tree:
            r = r.collapse_unary().chomsky_normal_form()
        _pcfg(r,left_to_right,right_to_left)

    for dct in left_to_right.values():
        total = 0
        for val in dct.values():
            total += val
        for key in dct:
            dct[key] /= total

    return left_to_right, right_to_left

def _pcfg(root, l_to_r, r_to_l):
    if type(root) is str: return

    rule_right = [dtr.label if type(dtr) is Tree else dtr
                    for dtr in root.daughters]
    rule_right = ' '.join(rule_right)

    l_to_r[root.label][rule_right] += 1
    r_to_l[rule_right].add(root.label)

    for daughter in root.daughters:
        _pcfg(daughter, l_to_r, r_to_l)

def pcfg_from_file(fname="./wsj-normalized.psd"):
    with open(fname) as f:
        return pcfg(Tree.from_stream(f), transform_tree=False)

def display_pcfg(l_to_r):
    for right,dct in l_to_r.items():
        for left,val in dct.items():
            print(right,"->",left,val)

if __name__ == "__main__":
    big_dict = pcfg(Tree.from_string(example_input),transform_tree=False)
    display_pcfg(big_dict[0])

    big_dict = pcfg_from_file()


    print("Count number of rules in wsj-normalized.psd")

    total = 0
    for dct in big_dict[0].values():
        total += len(dct)
    print(total)

# check both to make sure everything worked
    total = 0
    for lst in big_dict[1].values():
        total += len(lst)
    print(total)
