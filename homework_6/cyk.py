import numpy as np
from tree import Tree
from pcfg import pcfg, display_pcfg
from collections import defaultdict

def init_cyk_matrix(n,factory):
    cyk_matrix = np.empty((n,n), dtype=defaultdict)

    for i in range(n):
        for j in range(n):
            cyk_matrix[i,j] = defaultdict(factory)

    return cyk_matrix

def cyk(words, l_to_r, r_to_l):
    display_pcfg(l_to_r)
    n = len(words)
    table = init_cyk_matrix(n,float)
    back = init_cyk_matrix(n,tuple)

    for j in range(1,n):

        for A in r_to_l[words[j]]:
            table[j-1,j][A] = l_to_r[A][words[j]]

        for i in range(j-2,0,-1):
            for k in range(i+1,j-1):
                for BC in r_to_l:
                    B = BC.split(' ')
                    if len(B) == 1: continue # teminal rule
                    B,C = B

                    for A in r_to_l[BC]:

                        #if not (table[i,k][B] > 0 and table[k,j][C] > 0):
                        #    continue

                        tmp = l_to_r[A][BC] * table[i,k][B] * table[k,j][C]
                        if table[i,j][A] < tmp:
                            table[i,j][A] = tmp
                            back[i,j][A] = (k,B,C)

    print(table);print('=' * 20);print(back)

    return build_tree(back[0,n-1,"TOP"]), table[0,n-1,"TOP"]

def cyk2(words, l_to_r, r_to_l):
    n = len(words)
    pi = init_cyk_matrix(n,float)
    bp = init_cyk_matrix(n,tuple)

    print(r_to_l)
    display_pcfg(l_to_r)

    for i in range(n):
        for X in l_to_r:
            if words[i] in l_to_r[X]:
                pi[i,i][X] = l_to_r[X][words[i]]
            else:
                pi[i,i][X] = 0.0

    for l in range(n-1):
        for i in range(n-l):
            j = i + l
            for X,dct in l_to_r.items():
                for YZ in dct:
                    Y = YZ.split(' ')
                    if len(Y) != 2: continue
                    Y,Z = Y
                    mx = -1
                    argmx = None
                    for s in range(j-1):
                        tmp = l_to_r[X][YZ] * pi[i,s][Y] * pi[s+1,j][Z]
                        if mx < tmp:
                            mx = tmp
                            pi[i,j][X] = tmp
                            bp[i,j][X] = (s,YZ)

    print(pi);print('=' * 20);print(bp)




example_input = "(TOP (NP (DT the) (NN teacher)) (VP (MD will) (VP (VB lecture) (NP (NN today) (PP (IN in) (NP (DT the) (NN lecture) (NN hall)))))) (. .))"

cyk_example_input = "the teacher will lecture today in the lecture hall.".split(' ')

cyk(cyk_example_input, *pcfg(Tree.from_string(example_input)))
