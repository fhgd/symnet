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

eqs, x = cut_analysis(g, ctrl_src, tree)
A, b = create_matrices(eqs, x)
eqstr = pprint_linear(A, x, b)

treebrns = tree.branches()
cobrns = g.branches() - treebrns

print '* Baum', treebrns, ',  Ctrls', ctrl_src, ',  Cobaum', cobrns
print
print eqstr
print

num, denom = solve_linear(Matrix(A), x, Matrix(b), 'V_R2')
num = num.subs('V1', 1) * 'V1'  # factor out constant voltage source

num = str(num).replace('G_R', 'G')
denom = str(denom).replace('G_R', 'G')
print num
print '-' * max(len(str(num)), len(str(denom)))
print denom

