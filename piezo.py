from sympycore import Matrix

import symnet
reload(symnet)
from symnet import *

"""
Modell Piezogenerator:
         1     2
    +----+     +----+----+
    A    V     A    |    |
    RM   EM    FP   RP   IQ oder VQ
    |    |     |    |    |
    +----+-----+----+----+
            0

Gesteuerte Quellen:
    u = E(u)    i = F(i)    i = G(u)    u = H(i)
"""

gsrc = Graph()
gsrc.add_branch('RM', '0', '1')
gsrc.add_branch('EM', '1', '0')
gsrc.add_branch('RP', '2', '0')
gsrc.add_branch('FP', '0', '2')
gsrc.add_branch('Q', '0', '2')
ctrl_src = {'EM': 'RP', 'FP': 'RM'}
trees = [gsrc.tree(tree_branches) for tree_branches in
    ('RM', 'FP'),
    ('RM', 'RP'),
    ('RM', 'Q'),
    ('EM', 'FP'),
    ('EM', 'RP'),
    ('EM', 'Q'),
]
g = gsrc
for src in 'I', 'V':
    for tree in trees:
        treebrns = tree.branches()
        cobrns = g.branches() - treebrns
        for analysis in cut_analysis, loop_analysis:
            eqs, vars = analysis(g, ctrl_src, tree, {'Q': src})
            A, b = create_matrices(eqs, vars)
            # pretty print of the matrix equation
            eqs_str = [str(Matrix(M)).split('\n') for M in A, vars, b]
            lines = ['  [%s] [%s]   =  %s' % (e, v, r) for e, v, r in zip(*eqs_str)]
            lines = '\n'.join(lines)
            print '* Baum', treebrns, ',  Ctrls', ctrl_src, ',  Cobaum', cobrns
            print lines
            print
