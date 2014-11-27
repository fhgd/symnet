from symnet import *

g, ctrl_src = parse_netlist("""
    Vi  P   0
    U1  P   N
    N1  A   0
    R1  A   N
    R2  N   0
""")


#~ tree = g.tree('Vi U1 N1'.split())   # best for cut analysis
tree = g.tree('Vi R2 R1'.split())   # best for loop analysis

#~ tree = g.tree('Vi R2 R1'.split())
#~ tree = g.tree('Vi R2 N1'.split())
#~ tree = g.tree('Vi U1 R1'.split())
#~ tree = g.tree('U1 R2 R1'.split())
#~ tree = g.tree('U1 N1 R2'.split())

#~ eqs, x = cut_analysis(g, {}, tree)
#~ eqs, x, tree = mna(g, ctrl_src)
eqs, x = loop_analysis(g, {}, tree)

A, b = create_matrices(eqs, x)
eqstr = pprint_linear(A, x, b)
print eqstr
print

num, denom = solve_linear(Matrix(A), x, Matrix(b), 'V_N1')
num = num.subs('Vi', 1) * 'Vi'  # factor out constant voltage source

num = str(num).replace('G_R', 'G')
denom = str(denom).replace('G_R', 'G')
print num
print '-' * max(len(str(num)), len(str(denom)))
print denom
print
