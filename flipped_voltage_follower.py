from sympycore import Matrix
from symnet import *

"""
Circuit:

    +-----+-------------------------+-----+
   -|     |              OUT        |     |
    Gm1   Rds1                      |     |
   +|     |    X                    |     |
    +-----+-----+-- Rin --+ 1       RS    C2
   +|     |     |        +|         |     |
    Gm2   Rds2  C1        Vin       |     |
   -|     |     |        -|         |     |
    +-----+-----+---------+---------+-----+
          0

Controlled Sources:
    u = E(u)    i = F(i)    i = G(u)    u = H(i)
"""

netlist = """
Vin     1   0
Rin     1   X

RC1     X   0
Rds2    X   0
Gm2     X   0   RC2

Gm1     X   OUT RC1
Rds1    X   OUT

RS      OUT 0
RC2     OUT 0
"""
g, ctrl_src = parse_netlist(netlist)

tree = g.tree(['Rds2', 'Vin', 'RC2'])
eqs, x = cut_analysis(g, ctrl_src, tree)
eqs, x, tree = mna(g, ctrl_src)

A, b = create_matrices(eqs, x)
eqstr = pprint_linear(A, x, b)

treebrns = tree.branches()
cobrns = g.branches() - treebrns

print '* Baum', treebrns, ',  Ctrls', ctrl_src, ',  Cobaum', cobrns
print
print eqstr
print

print 'Mathematica:'
print pprint_mathematica(eqs, x)
print

num, denom = solve_linear(Matrix(A), x, Matrix(b), 'VOUT')
num = num.subs('Vin', 1) * 'Vin'  # factor out constant voltage source
subs = {'G_RC1':'s*C1', 'G_RC2':'s*C2'}

print 'Vout := num/denom := V_RC2'
print
print 'num   =', num.subs(subs)
print
print 'denom =', denom.subs(subs)

