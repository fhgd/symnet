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
eqs, x, tree = mna(g, ctrl_src)

A, b = create_matrices(eqs, x)
eqstr = pprint_linear(A, x, b)
print eqstr
print

print 'Mathematica:'
print pprint_mathematica(eqs, x)

