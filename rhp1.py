from symnet import *

"""
Controlled Sources:
    u = E(u)    i = F(i)    i = G(u)    u = H(i)
"""

netlist = """
C5 Vout1 Uin
C12 net12 0 
C11 net13 0 
C10 net14 0 
R7 0 Vout1 
R16 net12 net13 
R19 net13 net14 
R18 net14 Uin 
R17 Vout1 net12 
V5 Uin 0 

"""
g, ctrl_src = parse_netlist(netlist)
eqs, x, tree = mna(g, ctrl_src)

A, b = create_matrices(eqs, x)
eqstr = pprint_linear(A, x, b)
print eqstr
print

print 'Mathematica:'
print pprint_mathematica(eqs, x)

