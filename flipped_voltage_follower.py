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
lines = '\n\n'.join(lines)
print
print lines
print
print 'Vout := zout/nout := V_RC2'
print

Vout = x[1,0].subs({'G_RC1':'s*C1', 'G_RC2':'s*C2'})
zout, nout = Vout.as_numer_denom()

print 'zout =', zout
print
print 'nout =', nout

