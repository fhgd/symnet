import symnet
reload(symnet)
from symnet import *

g, ctrl_src = parse_netlist("""
    NR  A   0
    UL  P   A
    R4  P   0
    R2  X   P
    R3  X   A
    R1  I   X
    Vi  I   0
""")


#~ tree = g.tree('Vi NR R3 UL'.split())   # best for cut analysis
tree = g.tree('Vi NR R1 R2'.split())   # best for loop analysis


#~ eqs, x = cut_analysis(g, {}, tree)
#~ eqs, x, tree = mna(g, ctrl_src)
eqs, x = loop_analysis(g, {}, tree)

A, b = create_matrices(eqs, x)
eqstr = pprint_linear(A, x, b)
print eqstr
print

num, denom = solve_linear(Matrix(A), x, Matrix(b), 'V_NR')
num = num.subs('Vi', 1) * 'Vi'  # factor out constant voltage source

num = str(num).replace('G_R', 'G')
denom = str(denom).replace('G_R', 'G')
print num
print '-' * max(len(str(num)), len(str(denom)))
print denom
print

