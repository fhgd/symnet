from sympycore import Matrix
from symnet import *

"""
Circuit:

       A
+------+------+
|      |      |
|      R1     R3
|      |      |
V1   L +--Rm--+ R
|      |      |
|      R2     R4
|      |      |
+------+------+
       0

Controlled Sources:
    u = E(u)    i = F(i)    i = G(u)    u = H(i)
"""

g, ctrl_src = parse_netlist("""
    V1  A   0
    R1  A   L
    R2  L   0
    R3  A   R
    R4  R   0
    Rm  L   R
""")
tree = g.tree(['V1', 'R2', 'R4'])

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
det = A.det().expand()

idx = vars.index('V_R2')    # position of desired variable in vars
_A = Matrix(A)
_A[:, idx] = b      # put the rhs vector into the idx-column of the lhs matrix
src = 'V1'
det_idx = _A.det().expand().subs(src, 1) * src

print
print det_idx
print '-' * max(len(str(det_idx)), len(str(det)))
print det

if 0:
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

