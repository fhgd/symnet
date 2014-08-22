from sympycore import Matrix
import symnet
reload(symnet)
from symnet import *

"""
Circuit:

    1           2
    +     +-----+-----+
   +|    -|     |    +|
    Vin   Gm    Rds   R1
   -|    +|     |    -|
    +-----+-----+-----+
          0

Controlled Sources:
    u = E(u)    i = F(i)    i = G(u)    u = H(i)
"""

g = Graph()
g.add_branch('Vin', '0', '1')
g.add_branch('Gm',  '0', '2')
g.add_branch('Rds', '2', '0')
g.add_branch('R1',  '2', '0')
ctrl_src = {'Gm': 'Vin'}
tree = g.tree(['Vin', 'R1'])

#g.add_branch('Vin', '0', '1')
#tree = g.tree(['Rin', 'R1'])


eqs, vars = cut_analysis(g, ctrl_src, tree)
A, b = create_matrices(eqs, vars)
# pretty print of the matrix equation
eqs_str = [str(Matrix(M)).split('\n') for M in A, vars, b]
lines = ['  [%s] [%s]   =  %s' % (e, v, r) for e, v, r in zip(*eqs_str)]
lines = '\n'.join(lines)
treebrns = tree.branches()
cobrns = g.branches() - treebrns
print '* Baum', treebrns, ',  Ctrls', ctrl_src, ',  Cobaum', cobrns
print
print lines

A = Matrix(A)
b = Matrix(b)
x = A.solve(b)
x_str = str(x).split('\n')
lines = ['  %s  =  %s' % (xk, rk.strip()) for xk, rk in zip(vars, x_str)]
lines = '\n'.join(lines)
print
print lines
print
